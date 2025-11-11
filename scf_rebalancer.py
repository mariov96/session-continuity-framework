#!/usr/bin/env python3
"""
SCF Buildstate Rebalancer
========================

Intelligently rebalances data between .md and .json files to ensure optimal
information placement according to SCF principles:

JSON File (buildstate.json):
- Technical specifications and structured data
- Current implementation status and tracking
- Quantifiable metrics and configurations
- Machine-readable information for AI tools

Markdown File (buildstate.md):
- Ideation and conceptual thinking
- Human-readable context and rationale
- Documentation and explanations
- Strategic vision and user stories

This rebalancing happens during:
1. Ecosystem learning and pattern discovery
2. Inheritance system updates
3. Manual rebalancing operations
4. Project leveling up processes

Usage:
    python scf_rebalancer.py rebalance /path/to/project
    python scf_rebalancer.py analyze /path/to/project --suggest-moves
    python scf_rebalancer.py batch-rebalance /path/to/projects/*
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
import argparse
from collections import defaultdict

@dataclass
class ContentItem:
    """Represents a piece of content with placement analysis"""
    key: str
    value: Any
    current_location: str  # 'json' or 'md'
    optimal_location: str  # 'json' or 'md'
    confidence: float  # 0.0-1.0 confidence in optimal placement
    reason: str
    content_type: str  # 'technical', 'ideation', 'tracking', 'documentation'
    move_required: bool = False

@dataclass
class RebalanceAnalysis:
    """Analysis results for a buildstate pair"""
    json_path: Path
    md_path: Path
    items_to_move_to_json: List[ContentItem] = field(default_factory=list)
    items_to_move_to_md: List[ContentItem] = field(default_factory=list)
    items_well_placed: List[ContentItem] = field(default_factory=list)
    missing_files: List[str] = field(default_factory=list)
    rebalance_score: float = 0.0  # 0.0 = needs major rebalancing, 1.0 = perfectly balanced

class SCFContentAnalyzer:
    """Analyzes content to determine optimal placement"""
    
    def __init__(self):
        # Define content classification rules
        self.json_indicators = {
            # Technical and structured data
            'technical': [
                'version', 'status', 'priority', 'score', 'config', 'settings',
                'api_url', 'proxy', 'environment', 'stack', 'dependencies',
                'bugs', 'issues', 'tasks', 'features', 'success_metrics'
            ],
            # Tracking and quantifiable data
            'tracking': [
                'change_log', 'recent', 'completed', 'in_progress', 'next_steps',
                'decisions', 'roadmap', 'timeline', 'metrics', 'performance'
            ],
            # AI collaboration and machine-readable
            'ai_structured': [
                'ai_rules', 'ai_context', 'coding_standards', 'structure',
                'models', 'api_docs', 'testing', 'deployment'
            ]
        }
        
        self.md_indicators = {
            # Ideation and conceptual content
            'ideation': [
                'vision', 'concept', 'idea', 'brainstorm', 'approach', 'strategy',
                'philosophy', 'rationale', 'thinking', 'exploration'
            ],
            # Human-readable context
            'context': [
                'background', 'motivation', 'purpose', 'why', 'context',
                'explanation', 'description', 'overview', 'summary'
            ],
            # User-focused content
            'user_focused': [
                'user_stories', 'personas', 'user_experience', 'journey',
                'scenarios', 'use_cases', 'requirements', 'needs'
            ],
            # Documentation and narrative
            'documentation': [
                'notes', 'documentation', 'guide', 'tutorial', 'examples',
                'lessons_learned', 'retrospective', 'reflection'
            ]
        }
        
    def analyze_content_placement(self, key: str, value: Any, current_location: str) -> ContentItem:
        """Analyze where content should optimally be placed"""
        
        # Convert value to string for analysis
        value_str = self._value_to_string(value).lower()
        key_lower = key.lower()
        
        # Calculate placement scores
        json_score = self._calculate_json_score(key_lower, value_str, value)
        md_score = self._calculate_md_score(key_lower, value_str, value)
        
        # Determine optimal location
        if json_score > md_score:
            optimal_location = 'json'
            confidence = json_score / (json_score + md_score) if (json_score + md_score) > 0 else 0.5
            content_type = self._get_json_content_type(key_lower, value_str)
        else:
            optimal_location = 'md'
            confidence = md_score / (json_score + md_score) if (json_score + md_score) > 0 else 0.5
            content_type = self._get_md_content_type(key_lower, value_str)
            
        # Generate reason
        reason = self._generate_placement_reason(key, value, optimal_location, content_type)
        
        # Determine if move is required
        move_required = (current_location != optimal_location and confidence > 0.6)
        
        return ContentItem(
            key=key,
            value=value,
            current_location=current_location,
            optimal_location=optimal_location,
            confidence=confidence,
            reason=reason,
            content_type=content_type,
            move_required=move_required
        )
        
    def _value_to_string(self, value: Any) -> str:
        """Convert any value to string for analysis"""
        if isinstance(value, str):
            return value
        elif isinstance(value, dict):
            return ' '.join(str(v) for v in value.values())
        elif isinstance(value, list):
            return ' '.join(str(item) for item in value)
        else:
            return str(value)
            
    def _calculate_json_score(self, key: str, value_str: str, original_value: Any) -> float:
        """Calculate how well content fits in JSON file"""
        score = 0.0
        
        # Check key indicators
        for category, indicators in self.json_indicators.items():
            for indicator in indicators:
                if indicator in key:
                    score += 2.0
                if indicator in value_str:
                    score += 1.0
                    
        # Structural indicators
        if isinstance(original_value, dict) and len(original_value) > 1:
            score += 2.0  # Structured data belongs in JSON
        if isinstance(original_value, list):
            score += 1.5  # Arrays generally belong in JSON
        if key in ['status', 'priority', 'version', 'config']:
            score += 3.0  # Core technical fields
            
        # Check for quantifiable content
        if any(word in value_str for word in ['score', 'count', 'number', 'percent', 'rate']):
            score += 1.5
            
        # AI rules and technical specs
        if 'ai_' in key or 'coding_' in key or 'api_' in key:
            score += 2.5
            
        return score
        
    def _calculate_md_score(self, key: str, value_str: str, original_value: Any) -> float:
        """Calculate how well content fits in Markdown file"""
        score = 0.0
        
        # Check key indicators
        for category, indicators in self.md_indicators.items():
            for indicator in indicators:
                if indicator in key:
                    score += 2.0
                if indicator in value_str:
                    score += 1.0
                    
        # Narrative content indicators
        if isinstance(original_value, str) and len(original_value) > 100:
            score += 2.0  # Long text belongs in MD
        if any(word in value_str for word in ['why', 'how', 'because', 'should', 'could', 'would']):
            score += 1.5
            
        # Human-readable content
        if any(word in key for word in ['description', 'notes', 'vision', 'story', 'concept']):
            score += 3.0
            
        # Check for narrative patterns
        narrative_patterns = [r'\b(user|customer|client)\b', r'\b(should|could|would|might)\b', 
                            r'\b(vision|goal|objective|purpose)\b']
        for pattern in narrative_patterns:
            if re.search(pattern, value_str, re.IGNORECASE):
                score += 1.0
                
        return score
        
    def _get_json_content_type(self, key: str, value_str: str) -> str:
        """Determine JSON content type"""
        if any(ind in key for ind in self.json_indicators['technical']):
            return 'technical'
        elif any(ind in key for ind in self.json_indicators['tracking']):
            return 'tracking'  
        elif any(ind in key for ind in self.json_indicators['ai_structured']):
            return 'ai_structured'
        else:
            return 'technical'
            
    def _get_md_content_type(self, key: str, value_str: str) -> str:
        """Determine Markdown content type"""
        if any(ind in key for ind in self.md_indicators['ideation']):
            return 'ideation'
        elif any(ind in key for ind in self.md_indicators['context']):
            return 'context'
        elif any(ind in key for ind in self.md_indicators['user_focused']):
            return 'user_focused'
        elif any(ind in key for ind in self.md_indicators['documentation']):
            return 'documentation'
        else:
            return 'context'
            
    def _generate_placement_reason(self, key: str, value: Any, optimal_location: str, content_type: str) -> str:
        """Generate human-readable reason for placement"""
        if optimal_location == 'json':
            reasons = {
                'technical': f"Technical data like '{key}' belongs in structured JSON",
                'tracking': f"Tracking information '{key}' is best maintained in JSON for AI processing",
                'ai_structured': f"AI collaboration field '{key}' should be in JSON for tool integration"
            }
            return reasons.get(content_type, f"Structured data '{key}' is optimal in JSON format")
        else:
            reasons = {
                'ideation': f"Conceptual content '{key}' belongs in human-readable Markdown",
                'context': f"Contextual information '{key}' is better explained in Markdown",
                'user_focused': f"User-focused content '{key}' should be documented in Markdown",
                'documentation': f"Documentation '{key}' belongs in narrative Markdown format"
            }
            return reasons.get(content_type, f"Narrative content '{key}' is better suited for Markdown")

class SCFBuildstateRebalancer:
    """Rebalances buildstate content between JSON and MD files"""
    
    def __init__(self):
        self.analyzer = SCFContentAnalyzer()
        
    def analyze_buildstate_pair(self, project_path: Path) -> RebalanceAnalysis:
        """Analyze a buildstate.json/buildstate.md pair for rebalancing"""
        
        json_path = project_path / "buildstate.json"
        md_path = project_path / "buildstate.md"
        
        analysis = RebalanceAnalysis(json_path=json_path, md_path=md_path)
        
        # Check file existence
        if not json_path.exists():
            analysis.missing_files.append("buildstate.json")
        if not md_path.exists():
            analysis.missing_files.append("buildstate.md")
            
        if analysis.missing_files:
            return analysis
            
        # Load and analyze JSON content
        try:
            json_content = json.loads(json_path.read_text(encoding='utf-8'))
            self._analyze_json_content(json_content, analysis)
        except Exception as e:
            print(f"⚠️  Error loading JSON file: {e}")
            
        # Load and analyze MD content  
        try:
            md_content = md_path.read_text(encoding='utf-8')
            self._analyze_md_content(md_content, analysis)
        except Exception as e:
            print(f"⚠️  Error loading MD file: {e}")
            
        # Calculate rebalance score
        analysis.rebalance_score = self._calculate_rebalance_score(analysis)
        
        return analysis
        
    def _analyze_json_content(self, json_content: Dict[str, Any], analysis: RebalanceAnalysis):
        """Analyze JSON content for optimal placement"""
        
        def analyze_nested(obj: Any, prefix: str = ""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    
                    if isinstance(value, (dict, list)) and len(str(value)) > 500:
                        # Large nested structures - analyze for MD candidacy
                        item = self.analyzer.analyze_content_placement(full_key, value, 'json')
                        if item.optimal_location == 'md' and item.confidence > 0.6:
                            analysis.items_to_move_to_md.append(item)
                        else:
                            analysis.items_well_placed.append(item)
                    else:
                        item = self.analyzer.analyze_content_placement(full_key, value, 'json')
                        if item.move_required:
                            analysis.items_to_move_to_md.append(item)
                        else:
                            analysis.items_well_placed.append(item)
                            
                    # Recurse into nested objects
                    if isinstance(value, dict):
                        analyze_nested(value, full_key)
                        
        analyze_nested(json_content)
        
    def _analyze_md_content(self, md_content: str, analysis: RebalanceAnalysis):
        """Analyze Markdown content for structured data that should be in JSON"""
        
        # Look for structured data patterns in markdown
        patterns = [
            (r'##\s+Features?\s*\n(.*?)(?=##|\Z)', 'features'),
            (r'##\s+Tasks?\s*\n(.*?)(?=##|\Z)', 'tasks'),
            (r'##\s+Bugs?\s*\n(.*?)(?=##|\Z)', 'bugs'),
            (r'##\s+Decisions?\s*\n(.*?)(?=##|\Z)', 'decisions'),
            (r'##\s+Next Steps?\s*\n(.*?)(?=##|\Z)', 'next_steps'),
            (r'##\s+Configuration\s*\n(.*?)(?=##|\Z)', 'configuration'),
            (r'##\s+API\s*\n(.*?)(?=##|\Z)', 'api_docs'),
        ]
        
        for pattern, key in patterns:
            matches = re.findall(pattern, md_content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Analyze if this structured content should move to JSON
                item = self.analyzer.analyze_content_placement(key, match.strip(), 'md')
                if item.optimal_location == 'json' and item.confidence > 0.6:
                    # Check if it's structured enough to warrant JSON placement
                    if self._is_structured_content(match):
                        analysis.items_to_move_to_json.append(item)
                    else:
                        analysis.items_well_placed.append(item)
                else:
                    analysis.items_well_placed.append(item)
                    
    def _is_structured_content(self, content: str) -> bool:
        """Determine if markdown content is structured enough for JSON"""
        
        # Look for list patterns that could be JSON arrays
        list_patterns = [
            r'^\s*[-*+]\s+.*$',  # Bullet lists
            r'^\s*\d+\.\s+.*$',   # Numbered lists
            r'^\s*\[[ x]\]\s+.*$', # Checkboxes
        ]
        
        lines = content.strip().split('\n')
        structured_lines = 0
        
        for line in lines:
            if any(re.match(pattern, line) for pattern in list_patterns):
                structured_lines += 1
                
        # If >50% of lines are structured, consider for JSON
        return structured_lines > len(lines) * 0.5
        
    def _calculate_rebalance_score(self, analysis: RebalanceAnalysis) -> float:
        """Calculate how well balanced the current state is"""
        
        total_items = (len(analysis.items_to_move_to_json) + 
                      len(analysis.items_to_move_to_md) + 
                      len(analysis.items_well_placed))
        
        if total_items == 0:
            return 1.0
            
        well_placed_ratio = len(analysis.items_well_placed) / total_items
        
        # Penalize high-confidence moves more heavily
        move_penalty = 0
        for item in analysis.items_to_move_to_json + analysis.items_to_move_to_md:
            move_penalty += item.confidence
            
        move_penalty = move_penalty / total_items if total_items > 0 else 0
        
        score = well_placed_ratio - (move_penalty * 0.5)
        return max(0.0, min(1.0, score))
        
    def perform_rebalancing(self, analysis: RebalanceAnalysis, dry_run: bool = False) -> bool:
        """Perform the actual rebalancing based on analysis"""
        
        if analysis.missing_files:
            print(f"❌ Cannot rebalance - missing files: {', '.join(analysis.missing_files)}")
            return False
            
        if not (analysis.items_to_move_to_json or analysis.items_to_move_to_md):
            print("✅ Files are already well balanced - no changes needed")
            return True
            
        print(f"🔄 {'[DRY RUN] ' if dry_run else ''}Rebalancing buildstate files...")
        print(f"   📊 Current balance score: {analysis.rebalance_score:.2f}")
        print(f"   🔀 Items to move to JSON: {len(analysis.items_to_move_to_json)}")
        print(f"   🔀 Items to move to MD: {len(analysis.items_to_move_to_md)}")
        
        if not dry_run:
            # Create backups
            self._create_backups(analysis)
            
            # Perform moves
            success = True
            success &= self._move_items_to_json(analysis)
            success &= self._move_items_to_md(analysis)
            
            # Update change logs
            self._update_change_logs(analysis)
            
            return success
        else:
            # Show what would be moved
            self._show_planned_moves(analysis)
            return True
            
    def _create_backups(self, analysis: RebalanceAnalysis):
        """Create backup files before rebalancing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_backup = analysis.json_path.with_suffix(f".json.backup.{timestamp}")
        md_backup = analysis.md_path.with_suffix(f".md.backup.{timestamp}")
        
        import shutil
        shutil.copy2(analysis.json_path, json_backup)
        shutil.copy2(analysis.md_path, md_backup)
        
        print(f"📦 Backups created:")
        print(f"   📄 {json_backup}")
        print(f"   📄 {md_backup}")
        
    def _move_items_to_json(self, analysis: RebalanceAnalysis) -> bool:
        """Move structured content from MD to JSON"""
        
        if not analysis.items_to_move_to_json:
            return True
            
        try:
            # Load current JSON
            json_content = json.loads(analysis.json_path.read_text(encoding='utf-8'))
            
            # Add items from MD
            for item in analysis.items_to_move_to_json:
                # Convert MD content to JSON structure
                json_structure = self._convert_md_to_json_structure(item.value)
                json_content[item.key] = json_structure
                
            # Write updated JSON
            with open(analysis.json_path, 'w', encoding='utf-8') as f:
                json.dump(json_content, f, indent=2)
                
            print(f"✅ Moved {len(analysis.items_to_move_to_json)} items to JSON")
            return True
            
        except Exception as e:
            print(f"❌ Error moving items to JSON: {e}")
            return False
            
    def _move_items_to_md(self, analysis: RebalanceAnalysis) -> bool:
        """Move narrative content from JSON to MD"""
        
        if not analysis.items_to_move_to_md:
            return True
            
        try:
            # Load current files
            json_content = json.loads(analysis.json_path.read_text(encoding='utf-8'))
            md_content = analysis.md_path.read_text(encoding='utf-8')
            
            # Add items to MD
            md_additions = []
            for item in analysis.items_to_move_to_md:
                md_section = self._convert_json_to_md_section(item.key, item.value)
                md_additions.append(md_section)
                
                # Remove from JSON (only top-level keys for now)
                if '.' not in item.key and item.key in json_content:
                    del json_content[item.key]
                    
            # Append to MD file
            if md_additions:
                md_content += "\n\n" + "\n\n".join(md_additions)
                
            # Write updated files
            with open(analysis.json_path, 'w', encoding='utf-8') as f:
                json.dump(json_content, f, indent=2)
                
            with open(analysis.md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            print(f"✅ Moved {len(analysis.items_to_move_to_md)} items to MD")
            return True
            
        except Exception as e:
            print(f"❌ Error moving items to MD: {e}")
            return False
            
    def _convert_md_to_json_structure(self, md_content: str) -> Any:
        """Convert markdown content to appropriate JSON structure"""
        
        lines = md_content.strip().split('\n')
        
        # Try to detect structure
        if all(re.match(r'^\s*[-*+]\s+', line.strip()) for line in lines if line.strip()):
            # Bullet list -> JSON array
            return [re.sub(r'^\s*[-*+]\s+', '', line.strip()) for line in lines if line.strip()]
        elif all(re.match(r'^\s*\d+\.\s+', line.strip()) for line in lines if line.strip()):
            # Numbered list -> JSON array
            return [re.sub(r'^\s*\d+\.\s+', '', line.strip()) for line in lines if line.strip()]
        else:
            # Plain text
            return md_content.strip()
            
    def _convert_json_to_md_section(self, key: str, value: Any) -> str:
        """Convert JSON content to markdown section"""
        
        title = key.replace('_', ' ').title()
        section = f"## {title}\n\n"
        
        if isinstance(value, list):
            for item in value:
                section += f"- {item}\n"
        elif isinstance(value, dict):
            for k, v in value.items():
                section += f"**{k.replace('_', ' ').title()}**: {v}\n\n"
        else:
            section += str(value)
            
        return section
        
    def _show_planned_moves(self, analysis: RebalanceAnalysis):
        """Show what would be moved in dry run"""
        
        if analysis.items_to_move_to_json:
            print(f"\n📄 Would move to JSON:")
            for item in analysis.items_to_move_to_json:
                print(f"   • {item.key} ({item.confidence:.2f} confidence)")
                print(f"     💭 {item.reason}")
                
        if analysis.items_to_move_to_md:
            print(f"\n📝 Would move to Markdown:")
            for item in analysis.items_to_move_to_md:
                print(f"   • {item.key} ({item.confidence:.2f} confidence)")
                print(f"     💭 {item.reason}")
                
    def _update_change_logs(self, analysis: RebalanceAnalysis):
        """Update change logs in both files"""
        
        try:
            # Update JSON change log
            json_content = json.loads(analysis.json_path.read_text(encoding='utf-8'))
            
            if 'change_log' not in json_content:
                json_content['change_log'] = []
                
            json_content['change_log'].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "version": "rebalanced",
                "desc": f"SCF rebalancing: moved {len(analysis.items_to_move_to_md)} items to MD, {len(analysis.items_to_move_to_json)} items from MD",
                "source": "scf_rebalancer",
                "balance_score": f"{analysis.rebalance_score:.2f}"
            })
            
            with open(analysis.json_path, 'w', encoding='utf-8') as f:
                json.dump(json_content, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Could not update change log: {e}")

def main():
    parser = argparse.ArgumentParser(description="SCF Buildstate Rebalancer")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Rebalance command
    rebalance_parser = subparsers.add_parser('rebalance', help='Rebalance buildstate files')
    rebalance_parser.add_argument('project_path', type=Path, help='Path to project directory')
    rebalance_parser.add_argument('--dry-run', action='store_true', help='Show what would be changed')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze buildstate balance')
    analyze_parser.add_argument('project_path', type=Path, help='Path to project directory')
    analyze_parser.add_argument('--suggest-moves', action='store_true', help='Show suggested moves')
    
    # Batch rebalance command
    batch_parser = subparsers.add_parser('batch-rebalance', help='Rebalance multiple projects')
    batch_parser.add_argument('projects_pattern', help='Glob pattern for project directories')
    batch_parser.add_argument('--dry-run', action='store_true', help='Show what would be changed')
    batch_parser.add_argument('--min-score', type=float, default=0.5, 
                            help='Only rebalance projects below this score')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    rebalancer = SCFBuildstateRebalancer()
    
    if args.command == 'rebalance':
        analysis = rebalancer.analyze_buildstate_pair(args.project_path)
        
        print(f"🔍 Analyzing: {args.project_path.name}")
        print(f"📊 Balance Score: {analysis.rebalance_score:.2f}")
        
        success = rebalancer.perform_rebalancing(analysis, args.dry_run)
        if success:
            print("✅ Rebalancing completed successfully")
        else:
            print("❌ Rebalancing failed")
            
    elif args.command == 'analyze':
        analysis = rebalancer.analyze_buildstate_pair(args.project_path)
        
        print(f"📊 Balance Analysis for: {args.project_path.name}")
        print(f"   Score: {analysis.rebalance_score:.2f}")
        print(f"   Well Placed: {len(analysis.items_well_placed)} items")
        print(f"   Needs Moving: {len(analysis.items_to_move_to_json + analysis.items_to_move_to_md)} items")
        
        if args.suggest_moves:
            rebalancer._show_planned_moves(analysis)
            
    elif args.command == 'batch-rebalance':
        from glob import glob
        project_paths = [Path(p) for p in glob(args.projects_pattern)]
        
        print(f"🔄 Batch rebalancing {len(project_paths)} projects...")
        
        for project_path in project_paths:
            if not project_path.is_dir():
                continue
                
            analysis = rebalancer.analyze_buildstate_pair(project_path)
            
            if analysis.rebalance_score < args.min_score:
                print(f"\n📁 {project_path.name} (score: {analysis.rebalance_score:.2f})")
                rebalancer.perform_rebalancing(analysis, args.dry_run)
            else:
                print(f"✅ {project_path.name} is well balanced ({analysis.rebalance_score:.2f})")

if __name__ == "__main__":
    main()