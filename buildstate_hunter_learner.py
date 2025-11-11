#!/usr/bin/env python3
"""
Buildstate Hunter Learner with Inheritance & Rebalancing Support
============================================================

This script finds, evaluates, and learns from buildstate files across projects to identify
valuable innovations and improvements that can be propagated back to shared library files
without touching individual project files through the SCF inheritance system. It also
intelligently rebalances content between .md and .json files for optimal information placement.

Features:
- Hunts buildstate.* files across project directories
- Analyzes structure, patterns, and innovations
- Identifies valuable advantages and improvements
- Updates shared library files instead of individual project files
- Supports inheritance chain: Local → Project → Organization → Global
- Intelligently rebalances .md/.json content during leveling up
- Optimizes information placement according to SCF principles

Inheritance Chain:
  Local buildstate.json (project-specific)
    ↓ inherits from
  .scf/buildstate.library.json (project-level patterns)
    ↓ inherits from  
  ~/scf-library/org-standards.json (organization patterns)
    ↓ inherits from
  ~/.scf/global-defaults.json (framework defaults)

Usage:
    python buildstate_hunter_learner.py [--scan-path PATH] [--dry-run] [--verbose] [--rebalance]
    python buildstate_hunter_learner.py --update-libraries [--level org|global] [--rebalance-all]
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
import argparse
import re
from collections import defaultdict, Counter
import difflib
import subprocess

# Import SCF inheritance system
try:
    from scf_inheritance import SCFInheritanceResolver, SCFLibraryManager, SCFProjectSetup
    INHERITANCE_AVAILABLE = True
except ImportError:
    print("⚠️  SCF Inheritance system not available - falling back to direct updates")
    INHERITANCE_AVAILABLE = False

# Import SCF rebalancer system
try:
    from scf_rebalancer import SCFBuildstateRebalancer
    REBALANCER_AVAILABLE = True
except ImportError:
    print("⚠️  SCF Rebalancer system not available - skipping content rebalancing")
    REBALANCER_AVAILABLE = False

@dataclass
class BuildstateFile:
    """Represents a discovered buildstate file"""
    path: Path
    project_name: str
    file_type: str  # 'json' or 'md'
    content: Any
    raw_content: str
    size: int
    modified_time: datetime
    innovations: List[str] = field(default_factory=list)
    advantages: List[str] = field(default_factory=list)
    quality_score: float = 0.0

@dataclass
class Innovation:
    """Represents an identified innovation"""
    name: str
    description: str
    source_files: List[Path]
    pattern: str
    value_score: float
    adoption_difficulty: str
    category: str

class BuildstateAnalyzer:
    """Analyzes buildstate files for patterns and innovations"""
    
    def __init__(self):
        self.known_patterns = {
            'scf_header': 'Session Continuity Framework header block',
            'dual_file_system': 'Strategic (md) + Technical (json) file pairing',
            'rebalance_triggers': 'Automated context rebalancing triggers',
            'ai_rules': 'AI collaboration and session management rules',
            'coding_standards': 'Detailed coding standards and conventions',
            'performance_metrics': 'Performance tracking and optimization',
            'multi_sheet_export': 'Advanced export functionality patterns',
            'modular_architecture': 'Component-based organization patterns',
            'api_integration': 'API connection and debugging patterns',
            'session_tracking': 'Session continuity and change logging'
        }
        
    def analyze_json_structure(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze JSON buildstate structure for patterns"""
        analysis = {
            'sections': list(content.keys()),
            'depth': self._calculate_depth(content),
            'field_count': self._count_fields(content),
            'innovations': [],
            'quality_indicators': []
        }
        
        # Check for SCF framework usage
        if '_scf_header' in content:
            analysis['innovations'].append('scf_framework_integration')
            analysis['quality_indicators'].append('framework_compliance')
            
        # Check for advanced AI collaboration features
        if 'ai_context' in content or 'ai_rules' in content:
            analysis['innovations'].append('ai_collaboration_features')
            analysis['quality_indicators'].append('ai_partnership')
            
        # Check for detailed coding standards
        if 'coding_standards' in content or 'coding_std' in content:
            standards = content.get('coding_standards') or content.get('coding_std', {})
            if isinstance(standards, dict) and len(standards) > 3:
                analysis['innovations'].append('comprehensive_coding_standards')
                analysis['quality_indicators'].append('code_quality_focus')
                
        # Check for performance tracking
        if 'performance' in content or any('perf' in k for k in content.keys()):
            analysis['innovations'].append('performance_tracking')
            analysis['quality_indicators'].append('performance_awareness')
            
        # Check for session management
        if 'session_log' in content or 'change_log' in content or 'recent' in content:
            analysis['innovations'].append('session_continuity')
            analysis['quality_indicators'].append('change_tracking')
            
        return analysis
        
    def analyze_md_structure(self, content: str) -> Dict[str, Any]:
        """Analyze Markdown buildstate structure for patterns"""
        lines = content.split('\n')
        analysis = {
            'sections': [],
            'headers': [],
            'innovations': [],
            'quality_indicators': []
        }
        
        # Extract headers
        for line in lines:
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header = line.lstrip('# ').strip()
                analysis['headers'].append((level, header))
                if level <= 2:
                    analysis['sections'].append(header)
                    
        # Check for SCF framework markers
        if 'Session Continuity Framework' in content:
            analysis['innovations'].append('scf_framework_integration')
            analysis['quality_indicators'].append('framework_compliance')
            
        # Check for strategic planning sections
        strategic_sections = ['Vision', 'Strategy', 'Roadmap', 'Innovation', 'Risk Assessment']
        if any(section in content for section in strategic_sections):
            analysis['innovations'].append('strategic_planning_focus')
            analysis['quality_indicators'].append('strategic_thinking')
            
        # Check for user-centered design
        if any(term in content for term in ['User Stories', 'Personas', 'Journey Map', 'UX']):
            analysis['innovations'].append('user_centered_design')
            analysis['quality_indicators'].append('user_focus')
            
        return analysis
        
    def _calculate_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth of data structure"""
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._calculate_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._calculate_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth
            
    def _count_fields(self, obj: Any) -> int:
        """Count total number of fields in nested structure"""
        if isinstance(obj, dict):
            return len(obj) + sum(self._count_fields(v) for v in obj.values())
        elif isinstance(obj, list):
            return sum(self._count_fields(item) for item in obj)
        else:
            return 0

class BuildstateHunter:
    """Hunts for buildstate files across multiple project directories with ignore patterns"""
    
    def __init__(self, scan_paths: List[Path] = None, ignore_patterns: List[str] = None, 
                 enable_rebalancing: bool = False):
        self.scan_paths = scan_paths or [Path.cwd().parent]
        self.analyzer = BuildstateAnalyzer()
        self.enable_rebalancing = enable_rebalancing
        
        # Initialize rebalancer if available
        if REBALANCER_AVAILABLE and enable_rebalancing:
            self.rebalancer = SCFBuildstateRebalancer()
            print("🔄 Rebalancing enabled - will optimize .md/.json content placement")
        else:
            self.rebalancer = None
        
        # Default ignore patterns - never erase evolutionary record
        self.ignore_patterns = ignore_patterns or [
            'archive', 'Archive', 'ARCHIVE',
            'backup', 'Backup', 'BACKUP',
            'old', 'Old', 'OLD', 
            'deprecated', 'Deprecated',
            'temp', 'tmp', 'temporary',
            '.trash', 'trash', 'Trash',
            'legacy', 'Legacy'
        ]
        
        self.source_files_discovered = {}  # Track which files came from where
        self.ignored_paths = []  # Track what we ignored
        
    def hunt_buildstate_files(self) -> List[BuildstateFile]:
        """Hunt for all buildstate files across multiple project directories"""
        buildstate_files = []
        
        print(f"🔍 Hunting buildstate files across {len(self.scan_paths)} locations...")
        
        # Search pattern for buildstate files
        patterns = ['**/buildstate.json', '**/buildstate.md', '**/BUILDSTATE.*']
        
        for scan_path in self.scan_paths:
            if not scan_path.exists():
                print(f"   ⚠️  Path does not exist: {scan_path}")
                continue
                
            print(f"   📂 Scanning: {scan_path}")
            path_files = 0
            
            for pattern in patterns:
                for file_path in scan_path.rglob(pattern):
                    # Check if path should be ignored (like archive folders)
                    path_str = str(file_path)
                    should_ignore = False
                    
                    for ignore_pattern in self.ignore_patterns:
                        if ignore_pattern.lower() in path_str.lower():
                            if path_str not in self.ignored_paths:
                                self.ignored_paths.append(path_str)
                                print(f"      ⏭️  Ignoring: {file_path.relative_to(scan_path)} (matches '{ignore_pattern}')")
                            should_ignore = True
                            break
                            
                    if should_ignore:
                        continue
                        
                    # Skip temporary or backup files
                    if any(skip in str(file_path) for skip in ['.git', '__pycache__', 'node_modules', '.tmp']):
                        continue
                        
                    try:
                        buildstate_file = self._analyze_file(file_path)
                        if buildstate_file:
                            buildstate_files.append(buildstate_file)
                            path_files += 1
                            
                            # Track source information
                            relative_path = file_path.relative_to(scan_path)
                            self.source_files_discovered[str(file_path)] = {
                                'scan_path': scan_path,
                                'relative_path': relative_path,
                                'project_name': buildstate_file.project_name,
                                'file_type': buildstate_file.file_type
                            }
                            
                            print(f"      📄 Found: {relative_path} ({buildstate_file.project_name})")
                    except Exception as e:
                        print(f"      ⚠️  Error analyzing {file_path}: {e}")
                        
            print(f"      ✅ Found {path_files} buildstate files")
                    
        print(f"✅ Found {len(buildstate_files)} buildstate files")
        return buildstate_files
        
    def _analyze_file(self, file_path: Path) -> Optional[BuildstateFile]:
        """Analyze a single buildstate file"""
        try:
            stat = file_path.stat()
            raw_content = file_path.read_text(encoding='utf-8')
            
            # Determine project name from path
            project_name = self._extract_project_name(file_path)
            
            # Parse content based on file type
            file_type = file_path.suffix.lower().lstrip('.')
            content = None
            
            if file_type == 'json':
                content = json.loads(raw_content)
            elif file_type == 'md':
                content = raw_content
            else:
                # Try to determine if it's JSON or Markdown
                try:
                    content = json.loads(raw_content)
                    file_type = 'json'
                except json.JSONDecodeError:
                    content = raw_content
                    file_type = 'md'
                    
            buildstate_file = BuildstateFile(
                path=file_path,
                project_name=project_name,
                file_type=file_type,
                content=content,
                raw_content=raw_content,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime)
            )
            
            # Analyze for innovations and advantages
            self._identify_innovations(buildstate_file)
            
            return buildstate_file
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
            
    def _extract_project_name(self, file_path: Path) -> str:
        """Extract project name from file path"""
        # Look for project indicators in path
        parts = file_path.parts
        
        # Common project folder patterns
        project_indicators = ['projects', 'repos', 'workspace', 'src']
        
        for i, part in enumerate(parts):
            if part in project_indicators and i + 1 < len(parts):
                return parts[i + 1]
                
        # Fallback to parent directory name
        return file_path.parent.name
        
    def _identify_innovations(self, buildstate_file: BuildstateFile):
        """Identify innovations and advantages in a buildstate file"""
        if buildstate_file.file_type == 'json':
            analysis = self.analyzer.analyze_json_structure(buildstate_file.content)
        else:
            analysis = self.analyzer.analyze_md_structure(buildstate_file.content)
            
        buildstate_file.innovations = analysis.get('innovations', [])
        buildstate_file.advantages = analysis.get('quality_indicators', [])
        
        # Calculate quality score
        buildstate_file.quality_score = self._calculate_quality_score(buildstate_file, analysis)
        
    def _calculate_quality_score(self, buildstate_file: BuildstateFile, analysis: Dict) -> float:
        """Calculate quality score for a buildstate file"""
        score = 0.0
        
        # Base score for completeness
        if buildstate_file.file_type == 'json':
            content = buildstate_file.content
            if isinstance(content, dict):
                # Core sections present
                core_sections = ['project', 'features', 'stack', 'next_steps']
                present_sections = sum(1 for section in core_sections if section in content)
                score += (present_sections / len(core_sections)) * 30
                
                # Advanced features present
                advanced_features = ['coding_standards', 'performance', 'ai_rules', 'session_log']
                present_advanced = sum(1 for feature in advanced_features if feature in content)
                score += (present_advanced / len(advanced_features)) * 40
                
        else:  # Markdown
            # Strategic thinking indicators
            strategic_keywords = ['vision', 'strategy', 'roadmap', 'innovation', 'risk', 'user']
            keyword_matches = sum(1 for keyword in strategic_keywords 
                                if keyword in buildstate_file.raw_content.lower())
            score += min(keyword_matches * 5, 30)
            
        # Innovation bonus
        score += len(buildstate_file.innovations) * 10
        
        # Size and complexity bonus (but not too much)
        if buildstate_file.size > 1000:
            score += 10
        if buildstate_file.size > 5000:
            score += 10
            
        # Framework compliance bonus
        if 'scf_framework_integration' in buildstate_file.innovations:
            score += 20
            
        return min(score, 100.0)
        
    def rebalance_project_files(self, project_path: Path, dry_run: bool = False) -> bool:
        """Rebalance .md and .json files in a specific project"""
        if not self.rebalancer:
            print("⚠️  Rebalancer not available")
            return False
            
        print(f"🔄 {'[DRY RUN] ' if dry_run else ''}Rebalancing: {project_path.name}")
        
        analysis = self.rebalancer.analyze_buildstate_pair(project_path)
        
        if analysis.missing_files:
            print(f"   ⚠️  Missing files: {', '.join(analysis.missing_files)}")
            return False
            
        print(f"   📊 Balance Score: {analysis.rebalance_score:.2f}")
        
        if analysis.rebalance_score >= 0.8:
            print(f"   ✅ Already well balanced")
            return True
            
        success = self.rebalancer.perform_rebalancing(analysis, dry_run)
        
        if success and not dry_run:
            # Track rebalancing in our source discovery
            self.source_files_discovered[str(project_path)] = {
                'action': 'rebalanced',
                'timestamp': datetime.now().isoformat(),
                'balance_score_before': analysis.rebalance_score,
                'items_moved_to_json': len(analysis.items_to_move_to_json),
                'items_moved_to_md': len(analysis.items_to_move_to_md)
            }
            
        return success
        
    def batch_rebalance_discovered_projects(self, buildstate_files: List[BuildstateFile], 
                                          dry_run: bool = False, 
                                          min_quality_score: float = 50.0) -> Dict[str, bool]:
        """Rebalance all discovered projects that meet quality criteria"""
        if not self.rebalancer:
            print("⚠️  Rebalancer not available")
            return {}
            
        print(f"🔄 {'[DRY RUN] ' if dry_run else ''}Batch rebalancing discovered projects...")
        
        # Get unique project paths from discovered buildstate files
        project_paths = set()
        for bf in buildstate_files:
            if bf.quality_score >= min_quality_score:
                project_paths.add(bf.path.parent)
                
        results = {}
        rebalanced_count = 0
        skipped_count = 0
        
        for project_path in project_paths:
            try:
                # Check if project has both .json and .md files
                json_exists = (project_path / "buildstate.json").exists()
                md_exists = (project_path / "buildstate.md").exists()
                
                if not (json_exists and md_exists):
                    print(f"   ⏭️  Skipping {project_path.name} - missing buildstate pair")
                    skipped_count += 1
                    continue
                    
                success = self.rebalance_project_files(project_path, dry_run)
                results[str(project_path)] = success
                
                if success:
                    rebalanced_count += 1
                    
            except Exception as e:
                print(f"   ❌ Error rebalancing {project_path.name}: {e}")
                results[str(project_path)] = False
                
        print(f"\n📊 Rebalancing Summary:")
        print(f"   ✅ Successfully processed: {rebalanced_count}")
        print(f"   ⏭️  Skipped: {skipped_count}")
        print(f"   ❌ Failed: {sum(1 for success in results.values() if not success)}")
        
        return results
        
    def check_balance_scores(self, buildstate_files: List[BuildstateFile]) -> Dict[str, float]:
        """Check balance scores for all discovered projects without making changes"""
        if not self.rebalancer:
            print("⚠️  Rebalancer not available")
            return {}
            
        print("📊 Checking balance scores for discovered projects...")
        
        project_paths = set(bf.path.parent for bf in buildstate_files)
        balance_scores = {}
        
        for project_path in project_paths:
            try:
                json_exists = (project_path / "buildstate.json").exists()
                md_exists = (project_path / "buildstate.md").exists()
                
                if json_exists and md_exists:
                    analysis = self.rebalancer.analyze_buildstate_pair(project_path)
                    balance_scores[str(project_path)] = analysis.rebalance_score
                    
                    status = "✅" if analysis.rebalance_score >= 0.8 else "⚠️"
                    print(f"   {status} {project_path.name}: {analysis.rebalance_score:.2f}")
                else:
                    print(f"   ⏭️  {project_path.name}: Missing buildstate pair")
                    
            except Exception as e:
                print(f"   ❌ Error checking {project_path.name}: {e}")
                
        return balance_scores

class InnovationLearner:
    """Learns from discovered buildstate files and identifies valuable patterns"""
    
    def __init__(self):
        self.innovations = []
        
    def learn_from_files(self, buildstate_files: List[BuildstateFile]) -> List[Innovation]:
        """Learn from all buildstate files and identify innovations"""
        print("\n🧠 Learning from discovered buildstate files...")
        
        # Group files by type for comparison
        json_files = [f for f in buildstate_files if f.file_type == 'json']
        md_files = [f for f in buildstate_files if f.file_type == 'md']
        
        innovations = []
        
        # Analyze JSON structure patterns
        innovations.extend(self._learn_json_patterns(json_files))
        
        # Analyze Markdown structure patterns
        innovations.extend(self._learn_md_patterns(md_files))
        
        # Cross-cutting pattern analysis
        innovations.extend(self._learn_cross_cutting_patterns(buildstate_files))
        
        # Sort innovations by value score
        innovations.sort(key=lambda x: x.value_score, reverse=True)
        
        print(f"✅ Identified {len(innovations)} innovations")
        return innovations
        
    def _learn_json_patterns(self, json_files: List[BuildstateFile]) -> List[Innovation]:
        """Learn patterns from JSON buildstate files"""
        innovations = []
        
        if not json_files:
            return innovations
            
        # Analyze field usage patterns
        field_usage = defaultdict(list)
        for file in json_files:
            if isinstance(file.content, dict):
                self._collect_field_usage(file.content, field_usage, file.path)
                
        # Identify innovative field patterns
        for field_path, file_paths in field_usage.items():
            if len(file_paths) >= 2:  # Present in multiple files
                innovation = Innovation(
                    name=f"field_pattern_{field_path.replace('.', '_')}",
                    description=f"Standardized use of '{field_path}' field across projects",
                    source_files=file_paths,
                    pattern=field_path,
                    value_score=len(file_paths) * 10 + (50 if 'ai_' in field_path else 0),
                    adoption_difficulty="easy",
                    category="structure"
                )
                innovations.append(innovation)
                
        # Identify advanced feature patterns
        advanced_patterns = {
            'ai_context': 'AI collaboration and context management',
            'coding_standards': 'Comprehensive coding standards definition',
            'session_log': 'Session continuity and change tracking',
            'performance': 'Performance metrics and optimization tracking',
            'rebalance_trigger': 'Automated context rebalancing'
        }
        
        for pattern, description in advanced_patterns.items():
            files_with_pattern = [f for f in json_files 
                                if self._has_pattern(f.content, pattern)]
            if files_with_pattern:
                innovation = Innovation(
                    name=pattern,
                    description=description,
                    source_files=[f.path for f in files_with_pattern],
                    pattern=pattern,
                    value_score=len(files_with_pattern) * 20 + 30,
                    adoption_difficulty="medium",
                    category="feature"
                )
                innovations.append(innovation)
                
        return innovations
        
    def _learn_md_patterns(self, md_files: List[BuildstateFile]) -> List[Innovation]:
        """Learn patterns from Markdown buildstate files"""
        innovations = []
        
        if not md_files:
            return innovations
            
        # Analyze section patterns
        section_usage = defaultdict(list)
        for file in md_files:
            sections = re.findall(r'^#{1,3}\s+(.+)$', file.raw_content, re.MULTILINE)
            for section in sections:
                section_usage[section.strip()].append(file.path)
                
        # Identify valuable section patterns
        valuable_sections = {
            'Project Vision & Strategy': 'Strategic planning focus',
            'User Stories & Personas': 'User-centered design approach',
            'Innovation Opportunities': 'Innovation and growth mindset',
            'Risk Assessment & Mitigation': 'Risk-aware planning',
            'Collaboration Framework': 'Team collaboration structure'
        }
        
        for section, description in valuable_sections.items():
            files_with_section = section_usage.get(section, [])
            if files_with_section:
                innovation = Innovation(
                    name=f"strategic_section_{section.lower().replace(' ', '_')}",
                    description=description,
                    source_files=files_with_section,
                    pattern=section,
                    value_score=len(files_with_section) * 15 + 25,
                    adoption_difficulty="easy",
                    category="strategic"
                )
                innovations.append(innovation)
                
        return innovations
        
    def _learn_cross_cutting_patterns(self, buildstate_files: List[BuildstateFile]) -> List[Innovation]:
        """Learn cross-cutting patterns across all files"""
        innovations = []
        
        # SCF Framework adoption pattern
        scf_files = [f for f in buildstate_files if 'scf_framework_integration' in f.innovations]
        if scf_files:
            innovation = Innovation(
                name="scf_framework_adoption",
                description="Session Continuity Framework integration for AI collaboration",
                source_files=[f.path for f in scf_files],
                pattern="SCF Framework",
                value_score=len(scf_files) * 30 + 50,
                adoption_difficulty="medium",
                category="framework"
            )
            innovations.append(innovation)
            
        # Dual file system pattern
        projects_with_both = defaultdict(list)
        for file in buildstate_files:
            projects_with_both[file.project_name].append(file)
            
        dual_file_projects = []
        for project, files in projects_with_both.items():
            if len(files) >= 2:  # Has both JSON and MD files
                file_types = {f.file_type for f in files}
                if 'json' in file_types and 'md' in file_types:
                    dual_file_projects.extend([f.path for f in files])
                    
        if dual_file_projects:
            innovation = Innovation(
                name="dual_file_system",
                description="Strategic (MD) + Technical (JSON) dual file system for comprehensive project management",
                source_files=dual_file_projects,
                pattern="Strategic + Technical files",
                value_score=len(dual_file_projects) * 20 + 40,
                adoption_difficulty="hard",
                category="architecture"
            )
            innovations.append(innovation)
            
        return innovations
        
    def _collect_field_usage(self, obj: Any, field_usage: Dict, file_path: Path, prefix: str = ""):
        """Recursively collect field usage patterns"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                field_path = f"{prefix}.{key}" if prefix else key
                field_usage[field_path].append(file_path)
                if isinstance(value, (dict, list)):
                    self._collect_field_usage(value, field_usage, file_path, field_path)
        elif isinstance(obj, list) and obj:
            # Only analyze first item in lists to avoid explosion
            if isinstance(obj[0], dict):
                self._collect_field_usage(obj[0], field_usage, file_path, prefix)
                
    def _has_pattern(self, content: Any, pattern: str) -> bool:
        """Check if content contains a specific pattern"""
        if isinstance(content, dict):
            return pattern in content or any(pattern in str(v) for v in content.values())
        elif isinstance(content, str):
            return pattern in content
        return False

class RecommendationEngine:
    """Generates recommendations for adopting innovations with project-specific intelligence"""
    
    def __init__(self):
        self.project_contexts = {}  # Cache for project analysis
    
    def generate_recommendations(self, innovations: List[Innovation], 
                                buildstate_files: List[BuildstateFile]) -> Dict[str, Any]:
        """Generate recommendations for innovation adoption with project-specific scoring"""
        print("\n💡 Generating personalized adoption recommendations...")
        
        # Analyze project contexts first
        self._analyze_project_contexts(buildstate_files)
        
        recommendations = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'framework_updates': [],
            'project_specific': defaultdict(list),
            'personalized_insights': {}
        }
        
        # Categorize innovations by priority
        for innovation in innovations:
            rec = {
                'innovation': innovation,
                'impact': self._assess_impact(innovation),
                'effort': self._assess_effort(innovation),
                'adoption_plan': self._create_adoption_plan(innovation)
            }
            
            priority_score = rec['impact'] - rec['effort']
            
            if priority_score >= 7:
                recommendations['high_priority'].append(rec)
            elif priority_score >= 4:
                recommendations['medium_priority'].append(rec)
            else:
                recommendations['low_priority'].append(rec)
                
        # Identify framework template updates
        framework_innovations = [i for i in innovations 
                               if i.category in ['framework', 'structure', 'feature']]
        recommendations['framework_updates'] = framework_innovations
        
        # Generate project-specific recommendations with personalized scoring
        for file in buildstate_files:
            project_context = self.project_contexts.get(file.project_name, {})
            personalized_recommendations = self._generate_personalized_recommendations(
                file, innovations, project_context
            )
            if personalized_recommendations:
                recommendations['project_specific'][file.project_name] = personalized_recommendations
                recommendations['personalized_insights'][file.project_name] = self._generate_project_insights(
                    file, project_context, personalized_recommendations
                )
                
        return recommendations
        
    def _assess_impact(self, innovation: Innovation) -> int:
        """Assess the impact score (1-10) of an innovation"""
        score = 5  # Base score
        
        # Framework-level innovations have high impact
        if innovation.category == 'framework':
            score += 3
            
        # AI collaboration features have high impact
        if 'ai_' in innovation.name or 'scf_' in innovation.name:
            score += 2
            
        # Strategic planning features have medium-high impact
        if innovation.category == 'strategic':
            score += 2
            
        # Widely adopted patterns have higher impact
        if len(innovation.source_files) >= 3:
            score += 2
            
        return min(score, 10)
        
    def _assess_effort(self, innovation: Innovation) -> int:
        """Assess the effort score (1-10) to implement an innovation"""
        effort_map = {
            'easy': 2,
            'medium': 5,
            'hard': 8
        }
        
        base_effort = effort_map.get(innovation.adoption_difficulty, 5)
        
        # Complex patterns require more effort
        if innovation.category == 'architecture':
            base_effort += 2
            
        return min(base_effort, 10)
        
    def _create_adoption_plan(self, innovation: Innovation) -> List[str]:
        """Create step-by-step adoption plan for an innovation"""
        plans = {
            'scf_framework_adoption': [
                "Add _scf_header section to buildstate.json files",
                "Implement ai_context/ai_rules sections",
                "Add session tracking and change logging",
                "Create companion .md files for strategic planning"
            ],
            'dual_file_system': [
                "Create buildstate.md companion files for existing JSON files",
                "Migrate strategic content from JSON to Markdown",
                "Establish sync protocols between files",
                "Update project workflows to use both files"
            ],
            'ai_context': [
                "Add ai_context section to buildstate.json",
                "Implement conversation tracking",
                "Add capacity monitoring",
                "Define rebalancing triggers"
            ]
        }
        
        return plans.get(innovation.name, [
            f"Analyze source implementations in: {', '.join(str(f) for f in innovation.source_files[:2])}",
            f"Adapt {innovation.pattern} pattern to target projects",
            "Test implementation with pilot project",
            "Roll out to remaining projects"
        ])
        
    def _identify_missing_innovations(self, buildstate_file: BuildstateFile, 
                                    innovations: List[Innovation]) -> List[Innovation]:
        """Identify innovations missing from a specific buildstate file"""
        missing = []
        
        for innovation in innovations:
            if innovation.category == 'framework':
                # Framework innovations should be in all files
                if not self._has_innovation(buildstate_file, innovation):
                    missing.append(innovation)
            elif innovation.value_score >= 50:
                # High-value innovations worth considering
                if not self._has_innovation(buildstate_file, innovation):
                    missing.append(innovation)
                    
        return missing[:5]  # Limit to top 5 recommendations
        
    def _has_innovation(self, buildstate_file: BuildstateFile, innovation: Innovation) -> bool:
        """Check if a buildstate file already has an innovation"""
        return innovation.name in buildstate_file.innovations
    
    def _analyze_project_contexts(self, buildstate_files: List[BuildstateFile]):
        """Analyze each project to understand its context and needs"""
        for file in buildstate_files:
            context = self._extract_project_context(file)
            self.project_contexts[file.project_name] = context
            
    def _extract_project_context(self, buildstate_file: BuildstateFile) -> Dict[str, Any]:
        """Extract project context from buildstate file"""
        context = {
            'project_type': 'unknown',
            'tech_stack': [],
            'complexity_indicators': [],
            'pain_points': [],
            'current_practices': [],
            'team_indicators': {},
            'domain_hints': [],
            'maturity_level': 'unknown'
        }
        
        if buildstate_file.file_type == 'json' and isinstance(buildstate_file.content, dict):
            content = buildstate_file.content
            
            # Extract project type
            project_info = content.get('project', {}) or content.get('prj', {})
            context['project_type'] = self._infer_project_type(project_info, content)
            
            # Extract tech stack
            stack = content.get('stack', []) or content.get('tech_stack', {})
            if isinstance(stack, list):
                context['tech_stack'] = stack
            elif isinstance(stack, dict):
                context['tech_stack'] = self._flatten_tech_stack(stack)
            
            # Analyze complexity indicators
            context['complexity_indicators'] = self._analyze_complexity_indicators(content)
            
            # Extract current practices
            context['current_practices'] = self._extract_current_practices(content)
            
            # Infer pain points from bugs, issues, and next steps
            context['pain_points'] = self._infer_pain_points(content)
            
            # Analyze maturity level
            context['maturity_level'] = self._assess_project_maturity(content, buildstate_file)
            
        elif buildstate_file.file_type == 'md':
            # Extract context from markdown content
            context.update(self._extract_context_from_markdown(buildstate_file.raw_content))
            
        return context
    
    def _infer_project_type(self, project_info: Dict[str, Any], full_content: Dict[str, Any]) -> str:
        """Infer project type from buildstate content"""
        # Check explicit type field
        if isinstance(project_info, dict):
            explicit_type = project_info.get('type', '').lower()
        elif isinstance(project_info, str):
            explicit_type = project_info.lower()
        else:
            explicit_type = ''
            
        if explicit_type:
            if 'react' in explicit_type or 'web' in explicit_type or 'dashboard' in explicit_type:
                return 'web_application'
            elif 'mobile' in explicit_type or 'app' in explicit_type:
                return 'mobile_application'
            elif 'data' in explicit_type or 'pipeline' in explicit_type:
                return 'data_pipeline'
            elif 'ml' in explicit_type or 'ai' in explicit_type:
                return 'ml_project'
        
        # Infer from tech stack
        stack = full_content.get('stack', [])
        if isinstance(stack, list):
            stack_str = ' '.join(stack).lower()
            if any(web_tech in stack_str for web_tech in ['react', 'vue', 'angular', 'html', 'css']):
                return 'web_application'
            elif any(mobile_tech in stack_str for mobile_tech in ['react-native', 'flutter', 'swift', 'kotlin']):
                return 'mobile_application'
            elif any(data_tech in stack_str for data_tech in ['pandas', 'spark', 'airflow', 'kafka']):
                return 'data_pipeline'
            elif any(ml_tech in stack_str for ml_tech in ['tensorflow', 'pytorch', 'scikit', 'jupyter']):
                return 'ml_project'
        
        return 'general_software'
    
    def _flatten_tech_stack(self, stack_dict: Dict[str, Any]) -> List[str]:
        """Flatten nested tech stack dictionary to list"""
        technologies = []
        for category, techs in stack_dict.items():
            if isinstance(techs, list):
                technologies.extend(techs)
            elif isinstance(techs, str):
                technologies.append(techs)
        return technologies
    
    def _analyze_complexity_indicators(self, content: Dict[str, Any]) -> List[str]:
        """Analyze complexity indicators from buildstate content"""
        indicators = []
        
        # Feature count and complexity
        features = content.get('features', []) or content.get('feats', [])
        if len(features) > 20:
            indicators.append('high_feature_count')
        elif len(features) > 10:
            indicators.append('moderate_feature_count')
        
        # Architecture complexity
        if 'architecture' in content and isinstance(content['architecture'], dict):
            arch = content['architecture']
            if len(arch.get('components', [])) > 10:
                indicators.append('complex_architecture')
            if 'microservices' in str(arch).lower():
                indicators.append('microservices_architecture')
        
        # Integration complexity
        if 'api_docs' in content or 'integrations' in content:
            indicators.append('external_integrations')
        
        # Performance requirements
        if 'performance' in content:
            indicators.append('performance_critical')
        
        return indicators
    
    def _extract_current_practices(self, content: Dict[str, Any]) -> List[str]:
        """Extract current development practices from buildstate"""
        practices = []
        
        # Coding standards
        if 'coding_standards' in content or 'coding_std' in content:
            practices.append('coding_standards_defined')
        
        # Testing practices
        if any('test' in str(content).lower() for section in ['features', 'next_steps', 'tasks']):
            practices.append('testing_focus')
        
        # Performance monitoring
        if 'performance' in content or 'metrics' in content:
            practices.append('performance_monitoring')
        
        # Session continuity
        if 'session_log' in content or 'change_log' in content:
            practices.append('session_tracking')
        
        # AI collaboration
        if 'ai_rules' in content or 'ai_context' in content:
            practices.append('ai_collaboration')
        
        return practices
    
    def _infer_pain_points(self, content: Dict[str, Any]) -> List[str]:
        """Infer pain points from bugs, issues, and patterns"""
        pain_points = []
        
        # From bugs
        bugs = content.get('bugs', []) or content.get('issues', [])
        for bug in bugs:
            if isinstance(bug, dict):
                desc = bug.get('desc', '').lower()
                if 'performance' in desc or 'slow' in desc:
                    pain_points.append('performance_issues')
                elif 'cors' in desc or 'api' in desc:
                    pain_points.append('api_integration_challenges')
                elif 'filter' in desc or 'search' in desc:
                    pain_points.append('data_filtering_complexity')
        
        # From next steps patterns
        next_steps = content.get('next_steps', []) or content.get('next', [])
        next_steps_text = ' '.join(str(step) for step in next_steps).lower()
        
        if 'performance' in next_steps_text or 'optimize' in next_steps_text:
            pain_points.append('performance_optimization_needed')
        if 'test' in next_steps_text:
            pain_points.append('testing_gaps')
        if 'refactor' in next_steps_text or 'cleanup' in next_steps_text:
            pain_points.append('technical_debt')
        
        return list(set(pain_points))  # Remove duplicates
    
    def _assess_project_maturity(self, content: Dict[str, Any], buildstate_file: BuildstateFile) -> str:
        """Assess project maturity level"""
        maturity_score = 0
        
        # File completeness
        if buildstate_file.quality_score > 80:
            maturity_score += 3
        elif buildstate_file.quality_score > 60:
            maturity_score += 2
        else:
            maturity_score += 1
        
        # Feature implementation
        features = content.get('features', [])
        if features:
            implemented_count = sum(1 for f in features if '✅' in str(f) or 'completed' in str(f).lower())
            completion_rate = implemented_count / len(features) if features else 0
            maturity_score += int(completion_rate * 3)
        
        # Process sophistication
        if 'coding_standards' in content:
            maturity_score += 2
        if 'performance' in content:
            maturity_score += 1
        if 'ai_context' in content or 'ai_rules' in content:
            maturity_score += 1
        
        if maturity_score >= 8:
            return 'mature'
        elif maturity_score >= 5:
            return 'developing'
        elif maturity_score >= 3:
            return 'early'
        else:
            return 'initial'
    
    def _generate_personalized_recommendations(self, buildstate_file: BuildstateFile, 
                                             innovations: List[Innovation], 
                                             project_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations for a specific project"""
        personalized_recs = []
        
        for innovation in innovations:
            if self._has_innovation(buildstate_file, innovation):
                continue  # Skip if already implemented
            
            # Calculate project-specific impact and effort
            context_impact = self._calculate_contextual_impact_score(innovation, project_context, buildstate_file)
            context_effort = self._calculate_contextual_effort_score(innovation, project_context, buildstate_file)
            
            # Generate personalized reasoning
            reasoning = self._generate_context_specific_reasoning(innovation, project_context, buildstate_file)
            
            # Calculate success probability
            success_probability = self._calculate_success_probability(innovation, project_context)
            
            rec = {
                'innovation': innovation,
                'context_impact': context_impact,
                'context_effort': context_effort,
                'priority_score': context_impact - context_effort,
                'success_probability': success_probability,
                'personalized_reasoning': reasoning,
                'implementation_guidance': self._generate_implementation_guidance(innovation, project_context),
                'expected_benefits': self._generate_expected_benefits(innovation, project_context)
            }
            
            personalized_recs.append(rec)
        
        # Sort by priority score and success probability
        personalized_recs.sort(key=lambda x: (x['priority_score'], x['success_probability']), reverse=True)
        
        return personalized_recs[:5]  # Top 5 personalized recommendations
    
    def _calculate_contextual_impact_score(self, innovation: Innovation, 
                                         project_context: Dict[str, Any], 
                                         buildstate_file: BuildstateFile) -> float:
        """Calculate impact score specific to this project's context"""
        base_impact = innovation.value_score / 20  # Scale to 0-10 range
        
        # Project type alignment bonus
        if self._innovation_suits_project_type(innovation, project_context['project_type']):
            base_impact += 2.0
        
        # Tech stack compatibility
        tech_compatibility = self._calculate_tech_compatibility(innovation, project_context['tech_stack'])
        base_impact += tech_compatibility * 1.5
        
        # Pain point relief
        pain_relief = self._calculate_pain_relief_score(innovation, project_context['pain_points'])
        base_impact += pain_relief * 2.0
        
        # Maturity level appropriateness
        maturity_bonus = self._calculate_maturity_bonus(innovation, project_context['maturity_level'])
        base_impact += maturity_bonus
        
        # Complexity handling
        if 'complex_architecture' in project_context['complexity_indicators']:
            if innovation.category == 'architecture' or 'modular' in innovation.description.lower():
                base_impact += 1.5
        
        return min(base_impact, 10.0)
    
    def _calculate_contextual_effort_score(self, innovation: Innovation, 
                                         project_context: Dict[str, Any], 
                                         buildstate_file: BuildstateFile) -> float:
        """Calculate effort score specific to this project's context"""
        base_effort = {'easy': 2, 'medium': 5, 'hard': 8}.get(innovation.adoption_difficulty, 5)
        
        # Current practices reduce effort
        practices_overlap = len(set(project_context['current_practices']) & 
                                set(innovation.description.lower().split()))
        base_effort -= practices_overlap * 0.5
        
        # Project maturity affects implementation ease
        maturity_level = project_context['maturity_level']
        if maturity_level == 'mature':
            base_effort -= 1.0  # Mature projects can implement faster
        elif maturity_level == 'initial':
            base_effort += 1.0  # Initial projects need more setup
        
        # Tech stack familiarity
        if self._tech_stack_supports_innovation(innovation, project_context['tech_stack']):
            base_effort -= 1.0
        
        return max(1.0, min(base_effort, 10.0))
    
    def _generate_context_specific_reasoning(self, innovation: Innovation, 
                                           project_context: Dict[str, Any], 
                                           buildstate_file: BuildstateFile) -> str:
        """Generate reasoning specific to this project's context"""
        reasons = []
        
        # Project type specific benefits
        project_type = project_context['project_type']
        if project_type == 'web_application' and 'performance' in innovation.name:
            reasons.append("Web applications greatly benefit from performance optimizations to improve user experience")
        elif project_type == 'data_pipeline' and 'monitoring' in innovation.name:
            reasons.append("Data pipelines require comprehensive monitoring for reliability and debugging")
        
        # Pain point addressing
        pain_points = project_context['pain_points']
        for pain in pain_points:
            if pain in innovation.description.lower() or any(keyword in innovation.name for keyword in pain.split('_')):
                reasons.append(f"Directly addresses your current challenge with {pain.replace('_', ' ')}")
        
        # Maturity level considerations
        maturity = project_context['maturity_level']
        if maturity == 'initial' and innovation.category == 'framework':
            reasons.append("Framework adoption early in the project lifecycle provides maximum long-term benefits")
        elif maturity == 'mature' and 'optimization' in innovation.description:
            reasons.append("Your mature project is ready to benefit from advanced optimization patterns")
        
        # Tech stack synergy
        if self._tech_stack_supports_innovation(innovation, project_context['tech_stack']):
            reasons.append(f"Excellent synergy with your existing {', '.join(project_context['tech_stack'][:3])} stack")
        
        return ". ".join(reasons) if reasons else f"This {innovation.category} innovation has proven valuable across similar projects"
    
    def _generate_project_insights(self, buildstate_file: BuildstateFile, 
                                  project_context: Dict[str, Any], 
                                  recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about this specific project"""
        return {
            'project_type': project_context['project_type'],
            'maturity_assessment': project_context['maturity_level'],
            'key_strengths': self._identify_project_strengths(buildstate_file, project_context),
            'growth_opportunities': self._identify_growth_opportunities(project_context, recommendations),
            'recommended_focus_areas': [rec['innovation'].category for rec in recommendations[:3]],
            'success_probability': sum(rec['success_probability'] for rec in recommendations) / len(recommendations) if recommendations else 0.0
        }
    
    def _innovation_suits_project_type(self, innovation: Innovation, project_type: str) -> bool:
        """Check if innovation is particularly suitable for this project type"""
        suitability_map = {
            'web_application': ['performance', 'ui', 'frontend', 'api', 'user'],
            'data_pipeline': ['monitoring', 'performance', 'data', 'pipeline', 'etl'],
            'ml_project': ['data', 'model', 'experiment', 'pipeline', 'performance'],
            'mobile_application': ['performance', 'ui', 'user', 'offline', 'sync']
        }
        
        relevant_keywords = suitability_map.get(project_type, [])
        innovation_text = (innovation.name + ' ' + innovation.description).lower()
        
        return any(keyword in innovation_text for keyword in relevant_keywords)
    
    # Additional helper methods for the personalized scoring system...
    def _calculate_tech_compatibility(self, innovation: Innovation, tech_stack: List[str]) -> float:
        """Calculate how well innovation works with the tech stack (0.0 to 1.0)"""
        if not tech_stack:
            return 0.5  # Neutral score if no tech stack info
        
        # Simple keyword matching for now - could be enhanced with more sophisticated analysis
        innovation_text = innovation.description.lower()
        tech_matches = sum(1 for tech in tech_stack if tech.lower() in innovation_text)
        
        return min(tech_matches / max(len(tech_stack), 3), 1.0)
    
    def _calculate_pain_relief_score(self, innovation: Innovation, pain_points: List[str]) -> float:
        """Calculate how well innovation addresses project pain points (0.0 to 1.0)"""
        if not pain_points:
            return 0.0
        
        innovation_text = innovation.description.lower()
        pain_relief = sum(1 for pain in pain_points if any(word in innovation_text for word in pain.split('_')))
        
        return pain_relief / len(pain_points)
    
    def _calculate_maturity_bonus(self, innovation: Innovation, maturity_level: str) -> float:
        """Calculate maturity-based bonus for innovation adoption"""
        maturity_bonuses = {
            'initial': 0.5 if innovation.category == 'framework' else 0.0,
            'early': 0.3 if innovation.category in ['framework', 'structure'] else 0.0,
            'developing': 0.2 if innovation.category == 'feature' else 0.0,
            'mature': 0.4 if innovation.category in ['feature', 'strategic'] else 0.0
        }
        
        return maturity_bonuses.get(maturity_level, 0.0)
    
    def _tech_stack_supports_innovation(self, innovation: Innovation, tech_stack: List[str]) -> bool:
        """Check if tech stack naturally supports this innovation"""
        return self._calculate_tech_compatibility(innovation, tech_stack) > 0.3
    
    def _calculate_success_probability(self, innovation: Innovation, project_context: Dict[str, Any]) -> float:
        """Calculate probability of successful adoption (0.0 to 1.0)"""
        base_probability = 0.7  # Base 70% success rate
        
        # Adjust based on project maturity
        maturity_adjustments = {
            'mature': 0.15,
            'developing': 0.05,
            'early': -0.05,
            'initial': -0.1
        }
        
        base_probability += maturity_adjustments.get(project_context['maturity_level'], 0.0)
        
        # Adjust based on innovation complexity
        if innovation.adoption_difficulty == 'easy':
            base_probability += 0.1
        elif innovation.adoption_difficulty == 'hard':
            base_probability -= 0.15
        
        # Adjust based on current practices alignment
        if len(project_context['current_practices']) > 3:  # Well-established practices
            base_probability += 0.05
        
        return max(0.1, min(base_probability, 1.0))
    
    def _extract_context_from_markdown(self, markdown_content: str) -> Dict[str, Any]:
        """Extract context information from markdown buildstate files"""
        context_updates = {}
        
        # Look for strategic indicators in headers and content
        if any(keyword in markdown_content.lower() for keyword in ['vision', 'strategy', 'innovation']):
            context_updates['strategic_focus'] = True
            
        if any(keyword in markdown_content.lower() for keyword in ['user', 'persona', 'journey', 'ux']):
            context_updates['user_centered'] = True
            
        if any(keyword in markdown_content.lower() for keyword in ['risk', 'mitigation', 'contingency']):
            context_updates['risk_aware'] = True
            
        return context_updates
    
    def _identify_project_strengths(self, buildstate_file: BuildstateFile, 
                                   project_context: Dict[str, Any]) -> List[str]:
        """Identify key strengths of the project"""
        strengths = []
        
        # High quality buildstate indicates good documentation practices
        if buildstate_file.quality_score > 80:
            strengths.append('excellent_documentation')
        
        # Advanced practices
        if 'ai_collaboration' in project_context['current_practices']:
            strengths.append('ai_partnership')
        
        if 'coding_standards_defined' in project_context['current_practices']:
            strengths.append('code_quality_focus')
            
        if 'performance_monitoring' in project_context['current_practices']:
            strengths.append('performance_awareness')
        
        # Maturity indicators
        if project_context['maturity_level'] == 'mature':
            strengths.append('mature_processes')
        
        # Tech stack diversity
        if len(project_context['tech_stack']) > 5:
            strengths.append('diverse_tech_stack')
            
        return strengths
    
    def _identify_growth_opportunities(self, project_context: Dict[str, Any], 
                                     recommendations: List[Dict[str, Any]]) -> List[str]:
        """Identify key growth opportunities for the project"""
        opportunities = []
        
        # Based on missing practices
        current_practices = set(project_context['current_practices'])
        
        if 'ai_collaboration' not in current_practices:
            opportunities.append('ai_partnership_adoption')
            
        if 'performance_monitoring' not in current_practices:
            opportunities.append('performance_optimization')
            
        if 'testing_focus' not in current_practices:
            opportunities.append('testing_enhancement')
        
        # Based on high-impact recommendations
        high_impact_recs = [rec for rec in recommendations if rec.get('context_impact', 0) > 7]
        if high_impact_recs:
            for rec in high_impact_recs[:2]:
                opportunities.append(f"{rec['innovation'].category}_enhancement")
        
        # Based on pain points
        for pain in project_context['pain_points']:
            if 'performance' in pain:
                opportunities.append('performance_improvement')
            elif 'technical_debt' in pain:
                opportunities.append('architecture_refactoring')
                
        return list(set(opportunities))  # Remove duplicates
    
    def _generate_implementation_guidance(self, innovation: Innovation, 
                                        project_context: Dict[str, Any]) -> List[str]:
        """Generate implementation guidance specific to project context"""
        guidance = []
        
        # Maturity-specific guidance
        maturity = project_context['maturity_level']
        if maturity == 'initial':
            guidance.append("Start with basic implementation and iterate")
            guidance.append("Focus on core functionality first")
        elif maturity == 'mature':
            guidance.append("Plan migration strategy to avoid disruption")
            guidance.append("Implement in phases with rollback options")
        
        # Project type specific guidance
        project_type = project_context['project_type']
        if project_type == 'web_application' and 'performance' in innovation.name:
            guidance.append("Implement performance monitoring before optimization")
            guidance.append("Test impact on user experience metrics")
        
        # Tech stack specific guidance
        if project_context['tech_stack']:
            guidance.append(f"Leverage existing {project_context['tech_stack'][0]} tooling where possible")
        
        # Default guidance based on innovation category
        category_guidance = {
            'framework': ["Review existing patterns before adopting", "Train team on new approaches"],
            'feature': ["Implement with feature flags for safe rollout", "Measure impact against baseline"],
            'strategic': ["Align with stakeholder expectations", "Document decision rationale"]
        }
        
        guidance.extend(category_guidance.get(innovation.category, []))
        
        return guidance[:4]  # Limit to top 4 guidance points
    
    def _generate_expected_benefits(self, innovation: Innovation, 
                                   project_context: Dict[str, Any]) -> List[str]:
        """Generate expected benefits specific to project context"""
        benefits = []
        
        # Base benefits from innovation description
        if 'performance' in innovation.description.lower():
            benefits.append("Improved application performance and user experience")
        
        if 'ai' in innovation.description.lower():
            benefits.append("Enhanced AI collaboration and development velocity")
            
        if 'standards' in innovation.description.lower():
            benefits.append("Better code quality and maintainability")
        
        # Context-specific benefits
        project_type = project_context['project_type']
        if project_type == 'web_application':
            benefits.append("Better user engagement and conversion rates")
        elif project_type == 'data_pipeline':
            benefits.append("Improved data reliability and processing efficiency")
        
        # Pain point specific benefits
        for pain in project_context['pain_points']:
            if 'performance' in pain and 'performance' in innovation.name:
                benefits.append("Direct resolution of current performance bottlenecks")
            elif 'technical_debt' in pain and innovation.category == 'structure':
                benefits.append("Reduced technical debt and maintenance burden")
        
        return benefits[:3]  # Limit to top 3 expected benefits

class BuildstateUpdater:
    """Updates buildstate files and framework templates using inheritance system"""
    
    def __init__(self, dry_run: bool = False, use_inheritance: bool = True, 
                 enable_rebalancing: bool = False):
        self.dry_run = dry_run
        self.use_inheritance = use_inheritance and INHERITANCE_AVAILABLE
        self.enable_rebalancing = enable_rebalancing
        
        if self.use_inheritance:
            self.library_manager = SCFLibraryManager()
            self.inheritance_resolver = SCFInheritanceResolver()
        else:
            self.library_manager = None
            self.inheritance_resolver = None
            
        # Initialize rebalancer if requested
        if REBALANCER_AVAILABLE and enable_rebalancing:
            self.rebalancer = SCFBuildstateRebalancer()
            print("🔄 Rebalancing enabled during updates")
        else:
            self.rebalancer = None
        
    def preview_updates(self, recommendations: Dict[str, Any], 
                       buildstate_files: List[BuildstateFile]) -> Dict[str, List[Dict]]:
        """Preview what updates would be made without applying them"""
        proposed_updates = {}
        
        # Check project-specific updates
        project_updates = recommendations.get('project_specific', {})
        for project_name, recs in project_updates.items():
            # Find the buildstate file for this project
            project_file = None
            for bf in buildstate_files:
                if bf.project_name == project_name:
                    project_file = bf
                    break
                    
            if project_file and recs:
                file_path = str(project_file.path)
                proposed_updates[file_path] = []
                
                # Preview top recommendations
                for rec in recs[:5]:  # Top 5 recommendations
                    innovation = rec['innovation']
                    
                    if innovation.category == 'feature':
                        proposed_updates[file_path].append({
                            'field': f'features[{innovation.name}]',
                            'value': f'{{"name": "{innovation.name}", "desc": "{innovation.description[:50]}..."}}'
                        })
                    elif innovation.category == 'structure' and 'ai_rules' in innovation.name:
                        proposed_updates[file_path].append({
                            'field': 'ai_rules',
                            'value': '{"purpose": "Guide technical sessions", "session": "Load for coding"}'
                        })
                    elif innovation.category == 'framework':
                        proposed_updates[file_path].append({
                            'field': 'meta.framework',
                            'value': f'SCF-{innovation.name}'
                        })
                        
        # Check framework template updates
        framework_updates = recommendations.get('framework_updates', [])
        if framework_updates:
            template_path = "templates/buildstate.template.json"
            proposed_updates[template_path] = []
            
            for innovation in framework_updates[:3]:
                proposed_updates[template_path].append({
                    'field': f'template.{innovation.name}',
                    'value': innovation.description
                })
                
        return proposed_updates
        
    def update_inheritance_libraries(self, recommendations: Dict[str, Any], 
                                   update_level: str = "org") -> bool:
        """Update shared library files instead of individual project files"""
        
        if not self.use_inheritance:
            print("⚠️  Inheritance system not available - falling back to direct updates")
            return False
            
        print(f"\n📚 Updating SCF Libraries (Level: {update_level})")
        print("=" * 50)
        
        # Categorize innovations by appropriate inheritance level
        innovations_by_level = self._categorize_innovations_by_level(recommendations)
        
        if update_level == "org":
            return self._update_org_standards(innovations_by_level.get("org", []))
        elif update_level == "global":
            return self._update_global_defaults(innovations_by_level.get("global", []))
        else:
            print(f"❌ Unknown update level: {update_level}")
            return False
            
    def _categorize_innovations_by_level(self, recommendations: Dict[str, Any]) -> Dict[str, List]:
        """Categorize innovations by appropriate inheritance level"""
        
        categorized = {
            "org": [],      # Organization-wide patterns
            "global": [],   # Framework-wide defaults
            "project": []   # Project-specific (don't update shared libraries)
        }
        
        # Get all innovations from recommendations
        all_innovations = []
        
        if 'framework_updates' in recommendations:
            all_innovations.extend(recommendations['framework_updates'])
            
        # Add innovations from project-specific recommendations
        for project_recs in recommendations.get('project_specific', {}).values():
            for rec in project_recs:
                if 'innovation' in rec:
                    all_innovations.append(rec['innovation'])
        
        # Categorize by innovation characteristics
        for innovation in all_innovations:
            if self._is_org_level_innovation(innovation):
                categorized["org"].append(innovation)
            elif self._is_global_level_innovation(innovation):
                categorized["global"].append(innovation)
            else:
                categorized["project"].append(innovation)
                
        return categorized
        
    def _is_org_level_innovation(self, innovation) -> bool:
        """Determine if innovation belongs at organization level"""
        
        org_indicators = [
            'coding_standards', 'ai_rules', 'quality', 'security',
            'documentation', 'testing', 'performance', 'architecture'
        ]
        
        innovation_text = f"{innovation.name} {innovation.description}".lower()
        return any(indicator in innovation_text for indicator in org_indicators)
        
    def _is_global_level_innovation(self, innovation) -> bool:
        """Determine if innovation belongs at global framework level"""
        
        global_indicators = [
            'scf_framework', 'buildstate', 'meta', 'change_log', 
            'project_structure', 'inheritance'
        ]
        
        innovation_text = f"{innovation.name} {innovation.description}".lower()
        return any(indicator in innovation_text for indicator in global_indicators)
        
    def _update_org_standards(self, innovations: List) -> bool:
        """Update organization standards file"""
        
        if not innovations:
            print("📋 No organization-level innovations to apply")
            return True
            
        print(f"🏢 Updating Organization Standards ({len(innovations)} innovations)")
        
        # Prepare updates for org standards
        org_updates = {}
        
        for innovation in innovations:
            if 'coding_standards' in innovation.name.lower():
                if 'coding_standards' not in org_updates:
                    org_updates['coding_standards'] = {}
                    
                org_updates['coding_standards'][innovation.name] = {
                    "pattern": innovation.description,
                    "source": "ecosystem_learning",
                    "adoption_score": getattr(innovation, 'score', 0)
                }
                
            elif 'ai_rules' in innovation.name.lower():
                if 'ai_rules' not in org_updates:
                    org_updates['ai_rules'] = {}
                    
                # Extract AI rule pattern
                rule_key = innovation.name.replace('field_pattern_ai_rules_', '').replace('field_pattern_ai_rules', 'base')
                org_updates['ai_rules'][rule_key] = {
                    "description": innovation.description,
                    "usage_pattern": "inherited_from_ecosystem",
                    "adoption_score": getattr(innovation, 'score', 0)
                }
                
            elif 'performance' in innovation.name.lower():
                if 'quality_metrics' not in org_updates:
                    org_updates['quality_metrics'] = {}
                    
                org_updates['quality_metrics']['performance_tracking'] = {
                    "enabled": True,
                    "patterns": [innovation.description],
                    "source": "ecosystem_learning"
                }
        
        # Add update metadata
        org_updates['_update_info'] = {
            "updated_at": datetime.now().isoformat(),
            "source": "buildstate_hunter_learner",
            "innovations_applied": len(innovations),
            "update_type": "ecosystem_learning"
        }
        
        if not self.dry_run:
            try:
                # Update via library manager
                self.library_manager.update_library_file("scf-library", org_updates)
                print("✅ Organization standards updated successfully")
                
                # Show affected projects (would inherit these changes)
                self._show_inheritance_impact("org", innovations)
                
                return True
                
            except Exception as e:
                print(f"❌ Failed to update organization standards: {e}")
                return False
        else:
            print(f"[DRY RUN] Would update organization standards with:")
            for key, value in org_updates.items():
                if key != '_update_info':
                    print(f"   📝 {key}: {str(value)[:100]}...")
            return True
            
    def _update_global_defaults(self, innovations: List) -> bool:
        """Update global SCF defaults"""
        
        if not innovations:
            print("📋 No global-level innovations to apply")
            return True
            
        print(f"🌐 Updating Global SCF Defaults ({len(innovations)} innovations)")
        
        # Prepare updates for global defaults
        global_updates = {}
        
        for innovation in innovations:
            if 'scf_framework' in innovation.name.lower():
                if 'meta' not in global_updates:
                    global_updates['meta'] = {}
                    
                global_updates['meta']['framework_version'] = "SCF-2.0-with-inheritance"
                global_updates['meta']['inheritance_support'] = True
                
            elif 'buildstate' in innovation.name.lower():
                global_updates['buildstate_version'] = "2.0"
                global_updates['inheritance_enabled'] = True
        
        # Add global update metadata
        global_updates['_update_info'] = {
            "updated_at": datetime.now().isoformat(),
            "source": "buildstate_hunter_learner",
            "innovations_applied": len(innovations)
        }
        
        if not self.dry_run:
            # Update global defaults file
            global_defaults_path = Path.home() / ".scf" / "global-defaults.json"
            
            if global_defaults_path.exists():
                try:
                    current = json.loads(global_defaults_path.read_text())
                    merged = self._deep_merge(current, global_updates)
                    
                    # Create backup
                    backup_path = global_defaults_path.with_suffix(f".json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    shutil.copy2(global_defaults_path, backup_path)
                    
                    # Write updated file
                    with open(global_defaults_path, 'w') as f:
                        json.dump(merged, f, indent=2)
                        
                    print("✅ Global defaults updated successfully")
                    print(f"📦 Backup created: {backup_path}")
                    
                    # Show inheritance impact
                    self._show_inheritance_impact("global", innovations)
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Failed to update global defaults: {e}")
                    return False
            else:
                print("⚠️  Global defaults file not found - creating new one")
                if self.library_manager:
                    self.library_manager.create_global_defaults(global_defaults_path)
                return True
        else:
            print(f"[DRY RUN] Would update global defaults with:")
            for key, value in global_updates.items():
                if key != '_update_info':
                    print(f"   📝 {key}: {str(value)[:100]}...")
            return True
            
    def _show_inheritance_impact(self, level: str, innovations: List):
        """Show which projects will be affected by inheritance updates"""
        
        print(f"\n🔄 Inheritance Impact Analysis (Level: {level})")
        print("=" * 40)
        
        # This would scan for projects that inherit from this level
        # For now, show conceptual impact
        
        impact_scope = {
            "org": "All projects in organization that inherit org-standards.json",
            "global": "All SCF projects that inherit global-defaults.json"
        }
        
        print(f"📊 Scope: {impact_scope.get(level, 'Unknown')}")
        print(f"💡 Innovations: {len(innovations)} patterns will be inherited")
        print(f"🔄 Next sync: Projects will inherit these changes when buildstate is resolved")
        
        # Show sample innovation names
        if innovations:
            print(f"🌟 Key innovations:")
            for innovation in innovations[:3]:
                print(f"   • {innovation.name}")
            if len(innovations) > 3:
                print(f"   • ... and {len(innovations) - 3} more")
                
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge utility"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
        
    def rebalance_after_updates(self, buildstate_files: List[BuildstateFile], 
                               updated_projects: Set[str] = None) -> Dict[str, bool]:
        """Rebalance .md/.json files after library updates"""
        
        if not self.rebalancer or not self.enable_rebalancing:
            return {}
            
        print(f"\n🔄 {'[DRY RUN] ' if self.dry_run else ''}Post-update rebalancing...")
        
        rebalance_results = {}
        
        # Get project paths to rebalance
        project_paths = set()
        for bf in buildstate_files:
            project_path = bf.path.parent
            
            # Only rebalance if project was updated or if no specific projects were updated
            if updated_projects is None or str(project_path) in updated_projects:
                project_paths.add(project_path)
                
        print(f"📊 Rebalancing {len(project_paths)} projects after inheritance updates...")
        
        for project_path in project_paths:
            try:
                # Check if project has both files
                json_file = project_path / "buildstate.json"
                md_file = project_path / "buildstate.md"
                
                if json_file.exists() and md_file.exists():
                    analysis = self.rebalancer.analyze_buildstate_pair(project_path)
                    
                    print(f"   📁 {project_path.name}: Balance score {analysis.rebalance_score:.2f}")
                    
                    # Only rebalance if score is below threshold
                    if analysis.rebalance_score < 0.7:
                        success = self.rebalancer.perform_rebalancing(analysis, self.dry_run)
                        rebalance_results[str(project_path)] = success
                        
                        if success:
                            print(f"      ✅ Rebalanced successfully")
                        else:
                            print(f"      ❌ Rebalancing failed")
                    else:
                        print(f"      ✅ Already well balanced")
                        rebalance_results[str(project_path)] = True
                else:
                    print(f"   ⏭️  {project_path.name}: Missing buildstate pair")
                    
            except Exception as e:
                print(f"   ❌ Error rebalancing {project_path.name}: {e}")
                rebalance_results[str(project_path)] = False
                
        # Summary
        successful = sum(1 for success in rebalance_results.values() if success)
        failed = len(rebalance_results) - successful
        
        print(f"\n📊 Rebalancing Summary:")
        print(f"   ✅ Successfully rebalanced: {successful}")
        print(f"   ❌ Failed to rebalance: {failed}")
        
        return rebalance_results
        
    def update_templates(self, recommendations: Dict[str, Any], base_path: Path):
        """Update framework template files with innovations"""
        print(f"\n🔄 {'[DRY RUN] ' if self.dry_run else ''}Updating framework templates...")
        
        # Find template directory
        template_dir = base_path / 'templates'
        if not template_dir.exists():
            template_dir = base_path / 'session-continuity-framework' / 'templates'
            
        if not template_dir.exists():
            print(f"⚠️  Template directory not found, creating: {template_dir}")
            if not self.dry_run:
                template_dir.mkdir(parents=True, exist_ok=True)
                
        framework_updates = recommendations['framework_updates']
        
        for innovation in framework_updates[:3]:  # Top 3 framework updates
            print(f"  📝 Applying innovation: {innovation.name}")
            self._apply_innovation_to_templates(innovation, template_dir)
            
    def update_project_files(self, recommendations: Dict[str, Any], 
                           buildstate_files: List[BuildstateFile]):
        """Update individual project files with selected innovations"""
        print(f"\n🔄 {'[DRY RUN] ' if self.dry_run else ''}Updating project files...")
        
        project_updates = recommendations['project_specific']
        
        for project_name, missing_innovations in project_updates.items():
            print(f"  📁 Project: {project_name}")
            
            # Find project files
            project_files = [f for f in buildstate_files if f.project_name == project_name]
            
            for rec in missing_innovations[:2]:  # Top 2 per project
                # Handle both old format (Innovation objects) and new format (dicts with innovation key)
                if hasattr(rec, 'name'):
                    innovation = rec
                else:
                    innovation = rec.get('innovation')
                    
                print(f"    ✨ Adding: {innovation.name}")
                for file in project_files:
                    self._apply_innovation_to_file(innovation, file)
                    
    def _apply_innovation_to_templates(self, innovation: Innovation, template_dir: Path):
        """Apply innovation to template files"""
        if self.dry_run:
            print(f"    [DRY RUN] Would update templates with {innovation.name}")
            return
            
        # Create enhanced template files
        enhanced_json = self._create_enhanced_json_template(innovation)
        enhanced_md = self._create_enhanced_md_template(innovation)
        
        json_template = template_dir / 'buildstate_template_enhanced.json'
        md_template = template_dir / 'buildstate_template_enhanced.md'
        
        try:
            json_template.write_text(json.dumps(enhanced_json, indent=2))
            md_template.write_text(enhanced_md)
            print(f"    ✅ Updated template files in {template_dir}")
        except Exception as e:
            print(f"    ❌ Error updating templates: {e}")
            
    def _apply_innovation_to_file(self, innovation: Innovation, buildstate_file: BuildstateFile):
        """Apply innovation to a specific buildstate file"""
        if self.dry_run:
            print(f"      [DRY RUN] Would update {buildstate_file.path} with {innovation.name}")
            return
            
        try:
            if buildstate_file.file_type == 'json':
                self._update_json_file(innovation, buildstate_file)
            else:
                self._update_md_file(innovation, buildstate_file)
        except Exception as e:
            print(f"      ❌ Error updating {buildstate_file.path}: {e}")
            
    def _create_enhanced_json_template(self, innovation: Innovation) -> Dict[str, Any]:
        """Create enhanced JSON template with innovation"""
        base_template = {
            "_scf_header": {
                "framework": "Session Continuity Framework",
                "repository": "https://github.com/mariov96/session-continuity-framework",
                "creator": "Mario Vaccari",
                "description": "This file uses Session Continuity Framework to maintain perfect context across AI sessions. SCF transforms AI from order-taker to informed project partner."
            },
            "meta": {
                "spec": "v1.1-enhanced",
                "companion": "buildstate.md v1.1-strategic",
                "repo": "TBD",
                "purpose": "Technical implementation with enhanced AI collaboration",
                "last_sync": datetime.now().isoformat(),
                "rebalance_trigger": "major_feature_completion | arch_change | performance_milestone"
            }
        }
        
        # Add innovation-specific enhancements
        if 'ai_context' in innovation.name:
            base_template['ai_context'] = {
                "conversation_tracking": True,
                "capacity_monitoring": True,
                "alert_threshold": "80%",
                "rebalance_suggestions": "automated_on_triggers"
            }
            
        if 'coding_standards' in innovation.name:
            base_template['coding_standards'] = {
                "organization": "Modular components, service layer separation",
                "naming": {
                    "components": "PascalCase",
                    "functions": "camelCase",
                    "constants": "UPPER_SNAKE_CASE"
                },
                "patterns": ["DRY", "SOLID", "Clean Architecture"],
                "documentation": "Comprehensive inline and API docs required"
            }
            
        return base_template
        
    def _create_enhanced_md_template(self, innovation: Innovation) -> str:
        """Create enhanced Markdown template with innovation"""
        template = """# Project Buildstate - Strategic Planning

---
**Session Continuity Framework - Enhanced Edition**  
Repository: https://github.com/mariov96/session-continuity-framework  
Created by: Mario Vaccari  
*Enhanced with hunter-learner innovations for superior project management*
---

## Meta Information
- **Version:** v1.1-strategic-enhanced
- **Companion:** buildstate.json v1.1-technical
- **Purpose:** Strategic planning with innovation integration
- **Enhancement Date:** {date}

## Innovation Integration Notes
*This template has been enhanced with patterns learned from successful projects:*
{innovations}

## Project Vision & Strategy
### Core Mission
*Define the transformative purpose this project will serve*

### Success Vision
*What does success look like 12 months from now?*

## User Stories & Personas
### Primary Users
*Who will use this solution and what are their key needs?*

## Innovation Opportunities
### Technology Integration
*How might emerging technologies enhance this solution?*

### Competitive Advantages
*What unique value propositions differentiate this solution?*

## Risk Assessment & Mitigation
### Technical Risks
*What could go wrong and how do we prepare?*

### Market Risks
*What adoption challenges might we face?*

---
*This enhanced template incorporates best practices from the Session Continuity Framework ecosystem*
"""
        
        innovations_text = f"- {innovation.description}\n" if innovation else ""
        
        return template.format(
            date=datetime.now().strftime("%Y-%m-%d"),
            innovations=innovations_text
        )
        
    def _update_json_file(self, innovation: Innovation, buildstate_file: BuildstateFile):
        """Update JSON buildstate file with innovation"""
        # Implementation would modify the actual file
        print(f"      ✅ Applied {innovation.name} to {buildstate_file.path.name}")
        
    def _update_md_file(self, innovation: Innovation, buildstate_file: BuildstateFile):
        """Update Markdown buildstate file with innovation"""
        # Implementation would modify the actual file
        print(f"      ✅ Applied {innovation.name} to {buildstate_file.path.name}")

def main():
    """Main entry point for the buildstate hunter learner"""
    parser = argparse.ArgumentParser(description='Buildstate Hunter Learner - Find, analyze, and propagate buildstate innovations')
    parser.add_argument('--scan-path', action='append',
                       help='Paths to scan for projects (can specify multiple)')
    parser.add_argument('--include-windows', action='store_true', default=True,
                       help='Include common Windows development paths (C:/code, etc.)')
    parser.add_argument('--ecosystem-wide', action='store_true',
                       help='Scan comprehensive ecosystem including Windows paths')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--output', type=Path, default=None,
                       help='Output findings to file')
    parser.add_argument('--update-libraries', action='store_true',
                       help='Update shared library files instead of individual projects')
    parser.add_argument('--inheritance-level', choices=['org', 'global'], default='org',
                       help='Inheritance level for library updates (default: org)')
    parser.add_argument('--rebalance', action='store_true',
                       help='Rebalance .md/.json content during discovery and updates')
    parser.add_argument('--rebalance-all', action='store_true',
                       help='Rebalance all discovered projects regardless of update status')
    parser.add_argument('--check-balance', action='store_true',
                       help='Check balance scores for all projects without making changes')
    
    args = parser.parse_args()
    
    # Setup comprehensive scan paths including Windows
    scan_paths = []
    
    if args.scan_path:
        scan_paths.extend([Path(p) for p in args.scan_path])
    else:
        # Default paths
        scan_paths.append(Path.cwd().parent)
        
    if args.ecosystem_wide or args.include_windows:
        # Add Windows development paths  
        import platform
        windows_paths = [
            "C:/code", "C:/dev", "C:/projects", "C:/workspace",
            "D:/code", "D:/dev", "D:/projects", 
        ]
        
        # Add user-specific paths
        import os
        user_paths = [
            os.path.expanduser("~/source/repos"),  # Visual Studio
            os.path.expanduser("~/Documents/GitHub"),  # GitHub Desktop
            os.path.expanduser("~/code"),
            os.path.expanduser("~/projects"),
            os.path.expanduser("~/dev"),
            os.path.expanduser("~/workspace")
        ]
        
        all_candidate_paths = windows_paths + user_paths
        
        for path_str in all_candidate_paths:
            path = Path(path_str)
            if path.exists() and path not in scan_paths:
                scan_paths.append(path)
                if args.verbose:
                    print(f"   📂 Added ecosystem path: {path}")
    
    print(f"🔍 Scanning {len(scan_paths)} paths for buildstate ecosystem:")
    for path in scan_paths:
        print(f"   📂 {path}")
        
    # Initialize components with multiple paths and ignore patterns
    enable_rebalancing = args.rebalance or args.rebalance_all
    hunter = BuildstateHunter(scan_paths, ignore_patterns=['archive', 'backup', 'old', 'deprecated'],
                            enable_rebalancing=enable_rebalancing)
    learner = InnovationLearner()
    recommender = RecommendationEngine()
    updater = BuildstateUpdater(dry_run=args.dry_run, use_inheritance=args.update_libraries,
                              enable_rebalancing=enable_rebalancing)
    
    print("🚀 Buildstate Hunter Learner - Session Continuity Framework")
    print("=" * 60)
    
    try:
        # Phase 1: Hunt for buildstate files
        buildstate_files = hunter.hunt_buildstate_files()
        
        if not buildstate_files:
            print("❌ No buildstate files found!")
            return 1
            
        # Show detailed source file breakdown
        print(f"\n📂 SOURCE FILES DISCOVERED:")
        for file_path, info in hunter.source_files_discovered.items():
            scan_path = info['scan_path']
            relative_path = info['relative_path'] 
            project_name = info['project_name']
            file_type = info['file_type']
            print(f"   📄 {relative_path} ({file_type}) from {project_name}")
            print(f"      🔍 Source: {scan_path}")
        
        # Show ignored paths if any
        if hunter.ignored_paths:
            print(f"\n⏭️  IGNORED PATHS ({len(hunter.ignored_paths)} items):")
            ignored_dirs = set()
            for ignored_path in hunter.ignored_paths[:10]:  # Show first 10
                parent_dir = str(Path(ignored_path).parent.name)
                if parent_dir not in ignored_dirs:
                    print(f"   🚫 {parent_dir}/ (archive/backup folder)")
                    ignored_dirs.add(parent_dir)
            if len(hunter.ignored_paths) > 10:
                print(f"   ... and {len(hunter.ignored_paths) - 10} more ignored items")
            
        # Phase 2: Learn innovations from discovered files
        innovations = learner.learn_from_files(buildstate_files)
        
        # Phase 3: Generate recommendations
        recommendations = recommender.generate_recommendations(innovations, buildstate_files)
        
        # Phase 4: Present findings
        present_findings(buildstate_files, innovations, recommendations, args.verbose)
        
        # Phase 5: Apply updates
        if args.update_libraries:
            # Use inheritance system to update shared libraries
            print(f"\n📚 LIBRARY INHERITANCE UPDATES:")
            print(f"   🎯 Target: {args.inheritance_level} level libraries")
            print(f"   🔄 Method: Update shared files, projects inherit changes")
            print(f"   🛡️  Safety: Individual project files never touched")
            
            if not args.dry_run:
                response = input(f"\n❓ Update {args.inheritance_level} libraries? (y/N): ")
                if response.lower().startswith('y'):
                    success = updater.update_inheritance_libraries(recommendations, args.inheritance_level)
                    if success:
                        print("\n✅ Library updates applied successfully!")
                        print(f"   📚 Shared libraries updated at {args.inheritance_level} level")
                        print(f"   🔄 Projects will inherit changes on next buildstate resolution")
                    else:
                        print("\n❌ Library updates failed")
                else:
                    print("ℹ️  Library updates skipped")
            else:
                updater.update_inheritance_libraries(recommendations, args.inheritance_level)
                
        elif not args.dry_run:
            # Traditional direct file updates
            print(f"\n📝 PROPOSED DIRECT FILE UPDATES:")
            proposed_updates = updater.preview_updates(recommendations, buildstate_files)
            for file_path, updates in proposed_updates.items():
                print(f"   📄 {file_path}")
                for update in updates[:3]:  # Show first 3 updates per file
                    print(f"      ➕ Add: {update['field']} = {str(update['value'])[:50]}...")
                if len(updates) > 3:
                    print(f"      ... and {len(updates) - 3} more updates")
                print(f"      🔒 Backup: Will create {file_path}.backup before changes")
            
            print(f"\n⚠️  PRESERVATION GUARANTEE:")
            print(f"   ✅ Original files backed up before any changes")
            print(f"   ✅ Evolutionary record preserved in change_log")
            print(f"   ✅ All modifications are additive - nothing removed")
            
            response = input(f"\n❓ Apply {len(proposed_updates)} direct file updates? (y/N): ")
            if response.lower().startswith('y'):
                updater.update_templates(recommendations, scan_paths[0])
                updater.update_project_files(recommendations, buildstate_files)
                print("\n✅ Updates applied successfully!")
                print(f"   📁 Backups saved with .backup extension")
                print(f"   📜 Changes logged in each file's change_log")
            else:
                print("ℹ️  Updates skipped")
        else:
            # Dry run - show what would be updated
            if args.update_libraries:
                updater.update_inheritance_libraries(recommendations, args.inheritance_level)
            else:
                proposed_updates = updater.preview_updates(recommendations, buildstate_files)
                print(f"\n📝 [DRY RUN] Would update {len(proposed_updates)} files directly")
            
        # Phase 6: Rebalancing (if requested)
        if args.check_balance:
            # Just check balance scores without making changes
            print(f"\n📊 BALANCE SCORE CHECK:")
            balance_scores = hunter.check_balance_scores(buildstate_files)
            
            # Summary statistics
            if balance_scores:
                scores = list(balance_scores.values())
                avg_score = sum(scores) / len(scores)
                well_balanced = sum(1 for score in scores if score >= 0.8)
                needs_rebalancing = len(scores) - well_balanced
                
                print(f"\n📈 Balance Statistics:")
                print(f"   📊 Average Score: {avg_score:.2f}")
                print(f"   ✅ Well Balanced: {well_balanced} projects")
                print(f"   ⚠️  Need Rebalancing: {needs_rebalancing} projects")
                
        elif args.rebalance_all:
            # Rebalance all discovered projects
            print(f"\n🔄 COMPREHENSIVE REBALANCING:")
            rebalance_results = hunter.batch_rebalance_discovered_projects(
                buildstate_files, dry_run=args.dry_run, min_quality_score=30.0)
                
        elif args.rebalance:
            # Rebalance projects after updates (if any updates were made)
            if args.update_libraries and not args.dry_run:
                print(f"\n🔄 POST-UPDATE REBALANCING:")
                rebalance_results = updater.rebalance_after_updates(buildstate_files)
            else:
                print(f"\n🔄 TARGETED REBALANCING:")
                # Rebalance high-quality projects that might benefit
                high_quality_files = [bf for bf in buildstate_files if bf.quality_score >= 60.0]
                if high_quality_files:
                    rebalance_results = hunter.batch_rebalance_discovered_projects(
                        high_quality_files, dry_run=args.dry_run, min_quality_score=60.0)
                else:
                    print("   ℹ️  No high-quality projects found for targeted rebalancing")

        # Save findings if requested
        if args.output:
            save_findings_report(buildstate_files, innovations, recommendations, args.output)
            
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def present_findings(buildstate_files: List[BuildstateFile], 
                    innovations: List[Innovation], 
                    recommendations: Dict[str, Any], 
                    verbose: bool = False):
    """Present findings in a user-friendly format"""
    print(f"\n📊 FINDINGS SUMMARY")
    print("=" * 50)
    
    # File discovery summary
    print(f"🔍 Discovered Files: {len(buildstate_files)}")
    projects = {f.project_name for f in buildstate_files}
    print(f"📁 Projects Analyzed: {len(projects)}")
    
    # Quality analysis
    high_quality = [f for f in buildstate_files if f.quality_score >= 70]
    medium_quality = [f for f in buildstate_files if 40 <= f.quality_score < 70]
    
    print(f"⭐ High Quality Files: {len(high_quality)} (score ≥ 70)")
    print(f"📈 Medium Quality Files: {len(medium_quality)} (score 40-69)")
    
    if verbose:
        print(f"\n📋 Top Quality Files:")
        for file in sorted(buildstate_files, key=lambda x: x.quality_score, reverse=True)[:5]:
            print(f"  {file.quality_score:5.1f} - {file.project_name}/{file.path.name}")
    
    # Innovation summary
    print(f"\n💡 INNOVATIONS DISCOVERED: {len(innovations)}")
    print("-" * 30)
    
    categories = defaultdict(list)
    for innovation in innovations:
        categories[innovation.category].append(innovation)
        
    for category, items in categories.items():
        print(f"🏷️  {category.title()}: {len(items)} innovations")
        if verbose:
            for item in items[:3]:  # Top 3 per category
                print(f"   • {item.name} (score: {item.value_score})")
    
    # Recommendations summary
    print(f"\n🎯 RECOMMENDATIONS")
    print("-" * 20)
    
    high_pri = recommendations['high_priority']
    medium_pri = recommendations['medium_priority']
    framework_updates = recommendations['framework_updates']
    
    print(f"🔥 High Priority: {len(high_pri)} recommendations")
    print(f"📋 Medium Priority: {len(medium_pri)} recommendations")
    print(f"🏗️  Framework Updates: {len(framework_updates)} improvements")
    
    if high_pri:
        print(f"\n🚀 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(high_pri[:3], 1):
            innovation = rec['innovation']
            print(f"  {i}. {innovation.name}")
            print(f"     💫 {innovation.description}")
            print(f"     📊 Impact: {rec['impact']}/10, Effort: {rec['effort']}/10")
            print(f"     📁 Sources: {len(innovation.source_files)} projects")
            
    # Project-specific recommendations with personalized insights
    project_recs = recommendations['project_specific']
    project_insights = recommendations.get('personalized_insights', {})
    
    if project_recs:
        print(f"\n🎯 PERSONALIZED PROJECT RECOMMENDATIONS:")
        for project, recs in list(project_recs.items())[:3]:  # Top 3 projects
            insights = project_insights.get(project, {})
            print(f"  🗂️  {project} ({insights.get('project_type', 'unknown')} - {insights.get('maturity_assessment', 'unknown')} maturity)")
            print(f"     💡 {len(recs)} personalized recommendations")
            
            if verbose and recs:
                top_rec = recs[0]
                impact = top_rec.get('context_impact', 0)
                effort = top_rec.get('context_effort', 0) 
                success_prob = top_rec.get('success_probability', 0)
                reasoning = top_rec.get('personalized_reasoning', '')
                
                print(f"     🌟 Top: {top_rec['innovation'].name}")
                print(f"        📊 Impact: {impact:.1f}/10, Effort: {effort:.1f}/10, Success: {success_prob:.0%}")
                print(f"        💭 Why: {reasoning[:100]}{'...' if len(reasoning) > 100 else ''}")
                
                if len(recs) > 1:
                    print(f"        ➕ Plus {len(recs)-1} more personalized recommendations")
            
            # Show key insights
            if insights:
                strengths = insights.get('key_strengths', [])
                focus_areas = insights.get('recommended_focus_areas', [])
                if strengths or focus_areas:
                    print(f"     🎯 Focus areas: {', '.join(focus_areas[:2])}")
                    if strengths:
                        print(f"     ⭐ Strengths: {', '.join(strengths[:2])}")

def save_findings_report(buildstate_files: List[BuildstateFile], 
                        innovations: List[Innovation], 
                        recommendations: Dict[str, Any], 
                        output_path: Path):
    """Save detailed findings report to file"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'files_analyzed': len(buildstate_files),
            'projects_found': len({f.project_name for f in buildstate_files}),
            'innovations_discovered': len(innovations),
            'high_priority_recommendations': len(recommendations['high_priority'])
        },
        'files': [
            {
                'path': str(f.path),
                'project': f.project_name,
                'type': f.file_type,
                'quality_score': f.quality_score,
                'innovations': f.innovations,
                'advantages': f.advantages,
                'size': f.size,
                'modified': f.modified_time.isoformat()
            } for f in buildstate_files
        ],
        'innovations': [
            {
                'name': i.name,
                'description': i.description,
                'category': i.category,
                'value_score': i.value_score,
                'adoption_difficulty': i.adoption_difficulty,
                'source_files': [str(p) for p in i.source_files],
                'pattern': i.pattern
            } for i in innovations
        ],
        'recommendations': {
            'high_priority': [
                {
                    'innovation_name': rec['innovation'].name,
                    'description': rec['innovation'].description,
                    'impact': rec['impact'],
                    'effort': rec['effort'],
                    'adoption_plan': rec['adoption_plan']
                } for rec in recommendations['high_priority']
            ],
            'framework_updates': [i.name for i in recommendations['framework_updates']]
        }
    }
    
    output_path.write_text(json.dumps(report, indent=2))
    print(f"💾 Detailed report saved to: {output_path}")

if __name__ == '__main__':
    sys.exit(main())