#!/usr/bin/env python3
"""
SCF Context Cache Manager
=========================

Automatic context caching lifecycle management to reduce AI API costs.

Features:
- Multi-provider support (Gemini, Claude, OpenAI)
- Automatic cache invalidation on BUILDSTATE changes
- Cost savings tracking and reporting
- Session-aware cache lifecycle (create/reuse/cleanup)
- Strategic caching decisions (only cache when cost-effective)

Cost Optimization Strategy:
- Cache content > 4096 tokens (minimum for cost benefit)
- Track BUILDSTATE hash to invalidate on changes
- Set TTL to session length (avoid storage costs)
- Report savings: cached reads vs full-price writes

Usage:
    from scf_cache_manager import CacheManager
    
    manager = CacheManager(project_path)
    cache_id = manager.create_cache_if_worthwhile()
    
    # Use cache across multiple queries
    savings = manager.get_session_savings()
    
    # Cleanup at session end
    manager.cleanup()
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


# ============================================================================
# COST MODELS (Update these as provider pricing changes)
# ============================================================================

@dataclass
class ProviderPricing:
    """Pricing per 1M tokens in USD"""
    cached_input: float  # Cost for cached tokens (discounted)
    regular_input: float  # Cost for regular input tokens
    output: float  # Cost for output tokens
    cache_storage_per_hour: float  # Cost to store cache per hour
    min_cache_tokens: int  # Minimum tokens for cache to be worthwhile


PRICING = {
    "gemini-2.0-flash-exp": ProviderPricing(
        cached_input=0.01875,
        regular_input=0.075,
        output=0.30,
        cache_storage_per_hour=0.00001,  # Negligible
        min_cache_tokens=4096
    ),
    "claude-3-5-sonnet-20241022": ProviderPricing(
        cached_input=0.30,
        regular_input=3.00,
        output=15.00,
        cache_storage_per_hour=0.000375,  # $0.375 per 1M tokens per hour
        min_cache_tokens=4096
    ),
    "gpt-4o": ProviderPricing(
        cached_input=2.50,  # Placeholder - OpenAI doesn't have caching yet
        regular_input=5.00,
        output=15.00,
        cache_storage_per_hour=0.00001,
        min_cache_tokens=4096
    )
}


# ============================================================================
# CACHE METADATA TRACKING
# ============================================================================

@dataclass
class CacheMetadata:
    """Track cache state and savings"""
    cache_id: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    buildstate_hash: Optional[str] = None
    token_count: int = 0
    query_count: int = 0
    cached_tokens_used: int = 0
    regular_tokens_used: int = 0
    cost_savings_usd: float = 0.0
    last_invalidation_reason: Optional[str] = None


# ============================================================================
# PROVIDER ADAPTERS
# ============================================================================

class CacheProvider(ABC):
    """Abstract base for provider-specific caching implementations"""
    
    @abstractmethod
    def create_cache(self, content: str, ttl_seconds: int, model: str) -> Optional[str]:
        """Create cache, return cache_id"""
        pass
    
    @abstractmethod
    def delete_cache(self, cache_id: str) -> bool:
        """Delete cache, return success"""
        pass
    
    @abstractmethod
    def get_cache_info(self, cache_id: str) -> Optional[Dict[str, Any]]:
        """Get cache metadata"""
        pass


class GeminiCacheProvider(CacheProvider):
    """Gemini-specific caching implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        try:
            from google import genai
            from google.genai.types import CreateCachedContentConfig, Content
            self.client = genai.Client(api_key=self.api_key)
            self.Content = Content
            self.CreateCachedContentConfig = CreateCachedContentConfig
        except ImportError:
            raise ImportError("google-genai package required for Gemini caching")
    
    def create_cache(self, content: str, ttl_seconds: int, model: str) -> Optional[str]:
        """Create Gemini cache"""
        try:
            contents = [self.Content(parts=[{'text': content}])]
            
            cache = self.client.caches.create(
                model=model,
                config=self.CreateCachedContentConfig(
                    display_name=f"SCF_Cache_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    system_instruction="You are an expert assistant with access to project context.",
                    contents=contents,
                    ttl=f"{ttl_seconds}s",
                ),
            )
            return cache.name
        except Exception as e:
            print(f"❌ Gemini cache creation failed: {e}")
            return None
    
    def delete_cache(self, cache_id: str) -> bool:
        """Delete Gemini cache"""
        try:
            self.client.caches.delete(name=cache_id)
            return True
        except Exception as e:
            print(f"⚠️ Cache deletion failed: {e}")
            return False
    
    def get_cache_info(self, cache_id: str) -> Optional[Dict[str, Any]]:
        """Get Gemini cache info"""
        try:
            cache = self.client.caches.get(name=cache_id)
            return {
                "name": cache.name,
                "token_count": cache.usage_metadata.total_token_count,
                "expires_at": cache.expire_time
            }
        except Exception:
            return None


class ClaudeCacheProvider(CacheProvider):
    """Claude-specific caching implementation (Anthropic prompt caching)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        
        # Claude uses prompt caching via system messages
        # Cache is implicit - we track it via BUILDSTATE hash
    
    def create_cache(self, content: str, ttl_seconds: int, model: str) -> Optional[str]:
        """Claude uses implicit caching - return hash as cache_id"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def delete_cache(self, cache_id: str) -> bool:
        """Claude cache auto-expires - nothing to delete"""
        return True
    
    def get_cache_info(self, cache_id: str) -> Optional[Dict[str, Any]]:
        """Claude doesn't expose cache info - return placeholder"""
        return {"name": cache_id, "provider": "claude"}


# ============================================================================
# CACHE MANAGER
# ============================================================================

class CacheManager:
    """Manage context caching lifecycle for SCF projects"""
    
    def __init__(self, project_path: Path, provider: str = "gemini", model: Optional[str] = None):
        self.project_path = Path(project_path)
        self.provider = provider
        self.model = model or self._default_model(provider)
        
        # Initialize provider adapter
        self.cache_provider = self._init_provider(provider)
        
        # Load metadata
        self.metadata_file = self.project_path / ".scf" / "cache_metadata.json"
        self.metadata = self._load_metadata()
    
    def _default_model(self, provider: str) -> str:
        """Get default model for provider"""
        defaults = {
            "gemini": "gemini-2.0-flash-exp",
            "claude": "claude-3-5-sonnet-20241022",
            "openai": "gpt-4o"
        }
        return defaults.get(provider, "gemini-2.0-flash-exp")
    
    def _init_provider(self, provider: str) -> CacheProvider:
        """Initialize provider-specific adapter"""
        if provider == "gemini":
            return GeminiCacheProvider()
        elif provider == "claude":
            return ClaudeCacheProvider()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _load_metadata(self) -> CacheMetadata:
        """Load cache metadata from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                return CacheMetadata(**data)
            except Exception:
                pass
        return CacheMetadata()
    
    def _save_metadata(self):
        """Save cache metadata to disk"""
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(asdict(self.metadata), f, indent=2)
    
    def _get_buildstate_hash(self) -> str:
        """Compute hash of BUILDSTATE files to detect changes"""
        buildstate_json = self.project_path / ".scf" / "BUILDSTATE.json"
        buildstate_md = self.project_path / ".scf" / "BUILDSTATE.md"
        
        hasher = hashlib.sha256()
        
        if buildstate_json.exists():
            hasher.update(buildstate_json.read_bytes())
        if buildstate_md.exists():
            hasher.update(buildstate_md.read_bytes())
        
        return hasher.hexdigest()[:16]
    
    def _get_buildstate_content(self) -> str:
        """Get combined BUILDSTATE content for caching"""
        buildstate_json = self.project_path / ".scf" / "BUILDSTATE.json"
        buildstate_md = self.project_path / ".scf" / "BUILDSTATE.md"
        
        content = "# Project Context for AI Assistant\n\n"
        
        if buildstate_json.exists():
            content += "## BUILDSTATE.json\n```json\n"
            content += buildstate_json.read_text()
            content += "\n```\n\n"
        
        if buildstate_md.exists():
            content += "## BUILDSTATE.md\n"
            content += buildstate_md.read_text()
            content += "\n"
        
        return content
    
    def _estimate_tokens(self, content: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars)"""
        return len(content) // 4
    
    def is_cache_valid(self) -> bool:
        """Check if current cache is still valid"""
        if not self.metadata.cache_id:
            return False
        
        # Check if BUILDSTATE changed
        current_hash = self._get_buildstate_hash()
        if current_hash != self.metadata.buildstate_hash:
            self.metadata.last_invalidation_reason = "buildstate_changed"
            return False
        
        # Check if cache expired
        if self.metadata.expires_at:
            try:
                expires = datetime.fromisoformat(self.metadata.expires_at)
                if datetime.now() > expires:
                    self.metadata.last_invalidation_reason = "ttl_expired"
                    return False
            except Exception:
                pass
        
        return True
    
    def should_create_cache(self) -> tuple[bool, str]:
        """Determine if creating a cache is cost-effective"""
        content = self._get_buildstate_content()
        token_count = self._estimate_tokens(content)
        
        pricing = PRICING.get(self.model)
        if not pricing:
            return False, f"Unknown model pricing: {self.model}"
        
        if token_count < pricing.min_cache_tokens:
            return False, f"Content too small ({token_count} < {pricing.min_cache_tokens} tokens)"
        
        # Cost benefit: cache becomes worthwhile after ~3-4 queries
        # Break-even: cache_create_cost < (regular_cost - cached_cost) * num_queries
        savings_per_query = (pricing.regular_input - pricing.cached_input) * (token_count / 1_000_000)
        queries_to_break_even = 3
        
        if savings_per_query * queries_to_break_even > 0.001:  # At least 0.1 cent savings
            return True, f"Worthwhile: {token_count} tokens, savings after {queries_to_break_even} queries"
        else:
            return False, "Content too small for meaningful savings"
    
    def create_cache_if_worthwhile(self, ttl_hours: int = 4) -> Optional[str]:
        """Create cache if it makes financial sense"""
        
        # Check if we already have valid cache
        if self.is_cache_valid():
            print(f"✅ Using existing cache: {self.metadata.cache_id}")
            return self.metadata.cache_id
        
        # Check if caching is worthwhile
        should_cache, reason = self.should_create_cache()
        if not should_cache:
            print(f"⏭️  Skipping cache: {reason}")
            return None
        
        print(f"💰 Creating cache: {reason}")
        
        # Get content
        content = self._get_buildstate_content()
        token_count = self._estimate_tokens(content)
        
        # Create cache
        cache_id = self.cache_provider.create_cache(
            content=content,
            ttl_seconds=ttl_hours * 3600,
            model=self.model
        )
        
        if cache_id:
            # Update metadata
            self.metadata.cache_id = cache_id
            self.metadata.provider = self.provider
            self.metadata.model = self.model
            self.metadata.created_at = datetime.now().isoformat()
            self.metadata.expires_at = (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
            self.metadata.buildstate_hash = self._get_buildstate_hash()
            self.metadata.token_count = token_count
            self.metadata.query_count = 0
            self.metadata.cached_tokens_used = 0
            self.metadata.regular_tokens_used = 0
            
            self._save_metadata()
            print(f"✅ Cache created: {cache_id} ({token_count} tokens)")
            return cache_id
        
        return None
    
    def record_query(self, cached_tokens: int, regular_tokens: int):
        """Record a query using the cache"""
        self.metadata.query_count += 1
        self.metadata.cached_tokens_used += cached_tokens
        self.metadata.regular_tokens_used += regular_tokens
        
        # Calculate savings
        pricing = PRICING.get(self.model)
        if pricing:
            cached_cost = (cached_tokens / 1_000_000) * pricing.cached_input
            regular_cost_if_no_cache = (cached_tokens / 1_000_000) * pricing.regular_input
            self.metadata.cost_savings_usd += (regular_cost_if_no_cache - cached_cost)
        
        self._save_metadata()
    
    def get_session_report(self) -> Dict[str, Any]:
        """Get cost savings report"""
        pricing = PRICING.get(self.model)
        
        return {
            "cache_id": self.metadata.cache_id,
            "provider": self.metadata.provider,
            "model": self.metadata.model,
            "queries": self.metadata.query_count,
            "cached_tokens": self.metadata.cached_tokens_used,
            "savings_usd": round(self.metadata.cost_savings_usd, 4),
            "valid": self.is_cache_valid(),
            "pricing": asdict(pricing) if pricing else None
        }
    
    def cleanup(self, force: bool = False):
        """Delete cache and clean up"""
        if self.metadata.cache_id:
            print(f"🧹 Cleaning up cache: {self.metadata.cache_id}")
            
            # Show final report
            report = self.get_session_report()
            if report["savings_usd"] > 0:
                print(f"💰 Session savings: ${report['savings_usd']:.4f} ({report['queries']} queries)")
            
            # Delete cache
            self.cache_provider.delete_cache(self.metadata.cache_id)
            
            # Clear metadata
            self.metadata.cache_id = None
            self._save_metadata()


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI for cache management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SCF Context Cache Manager")
    parser.add_argument("project_path", type=Path, help="Path to SCF project")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "claude"], help="AI provider")
    parser.add_argument("--model", help="Model to use (optional)")
    parser.add_argument("--action", default="status", choices=["create", "status", "cleanup"], help="Action")
    parser.add_argument("--ttl", type=int, default=4, help="Cache TTL in hours")
    
    args = parser.parse_args()
    
    manager = CacheManager(args.project_path, provider=args.provider, model=args.model)
    
    if args.action == "create":
        cache_id = manager.create_cache_if_worthwhile(ttl_hours=args.ttl)
        if cache_id:
            print(f"\n✅ Cache ready: {cache_id}")
    
    elif args.action == "status":
        report = manager.get_session_report()
        print("\n📊 Cache Status:")
        print(f"   Valid: {report['valid']}")
        print(f"   Cache ID: {report['cache_id']}")
        print(f"   Model: {report['model']}")
        print(f"   Queries: {report['queries']}")
        print(f"   Savings: ${report['savings_usd']:.4f}")
    
    elif args.action == "cleanup":
        manager.cleanup()


if __name__ == "__main__":
    main()
