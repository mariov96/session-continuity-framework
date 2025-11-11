#!/usr/bin/env python3
"""
SCF Meta-Learning Evaluator
============================

Extracts non-project-specific patterns, policies, and best practices from buildstate files
to build a knowledge library that can intelligently suggest framework improvements and 
project-type-aware recommendations.

This is the "Borg assimilation" system - learning from successful projects to improve
both the SCF framework and suggest relevant patterns to new projects based on their type.

Key Features:
- Extracts meta-patterns (IDE configs, dev workflows, testing approaches)
- Builds categorized knowledge library by project type
- Suggests framework improvements based on discovered patterns
- Recommends project-specific adoptions based on project type matching
- Learns from bug resolution patterns to prevent repeated time waste
- Maintains best practices library with applicability rules

Usage:
    python scf_meta_learner.py --scan-path /path/to/projects --extract-patterns
    python scf_meta_learner.py --evaluate-project /path/to/project --project-type web
    python scf_meta_learner.py --update-framework-library --dry-run
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
import argparse
import re
from collections import defaultdict, Counter
import subprocess
import yaml

@dataclass
class MetaPattern:
    """Represents a learned meta-pattern that can be applied across projects"""
    name: str
    category: str  # ide_config, dev_workflow, testing, deployment, bug_resolution
    project_types: List[str]  # web, desktop, cli, mobile, data_pipeline, etc.
    pattern_data: Dict[str, Any]
    source_projects: List[str]
    confidence_score: float  # Based on how many projects use this pattern
    applicability_rules: Dict[str, Any]
    description: str
    implementation_guide: List[str]
    
@dataclass 
class ProjectTypeProfile:
    """Profile of patterns specific to a project type"""
    project_type: str
    common_patterns: List[MetaPattern]
    ide_configurations: Dict[str, Any]
    dev_workflows: Dict[str, Any]
    testing_approaches: Dict[str, Any]
    deployment_patterns: Dict[str, Any]
    bug_resolution_learnings: List[Dict[str, Any]]
    
class SCFMetaLearner:
    """Learns meta-patterns from buildstate files and builds knowledge library"""
    
    def __init__(self, framework_library_path: Path = None):
        self.framework_library_path = framework_library_path or Path("~/.scf/meta-patterns.json").expanduser()
        self.patterns_database = {}
        self.project_type_profiles = {}
        self.framework_knowledge = self._load_framework_knowledge()
        
        # Project type detection patterns
        self.project_type_indicators = {
            'web_application': ['react', 'vue', 'angular', 'express', 'django', 'flask', 'fastapi', 'next.js'],
            'desktop_application': ['electron', 'pyqt', 'pyside', 'tkinter', 'wpf', 'gtk', 'flutter_desktop'],
            'mobile_application': ['react-native', 'flutter', 'swift', 'kotlin', 'xamarin', 'ionic'],
            'cli_tool': ['click', 'argparse', 'commander', 'cobra', 'clap', 'typer'],
            'data_pipeline': ['pandas', 'spark', 'airflow', 'dbt', 'prefect', 'dagster'],
            'ml_project': ['tensorflow', 'pytorch', 'scikit-learn', 'jupyter', 'mlflow', 'kubeflow'],
            'api_service': ['fastapi', 'express', 'gin', 'spring', 'asp.net', 'rails'],
            'library_package': ['setuptools', 'npm_package', 'cargo', 'gem', 'composer']
        }
        
    def _load_framework_knowledge(self) -> Dict[str, Any]:
        """Load existing framework knowledge library"""
        if self.framework_library_path.exists():
            try:
                with open(self.framework_library_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading framework knowledge: {e}")
                
        return {
            'meta_patterns': {},
            'project_type_profiles': {},
            'last_updated': None,
            'version': '1.0'
        }
        
    def extract_meta_patterns_from_analysis(self, buildstate_files: List[Any], 
                                          analysis_results: Dict[str, Any]) -> List[MetaPattern]:
        """Extract meta-patterns using rich analysis data from InnovationLearner"""
        print("🧠 Extracting meta-patterns from ecosystem analysis...")
        
        extracted_patterns = []
        
        # Extract patterns from discovered innovations
        if 'innovations' in analysis_results:
            innovations = analysis_results['innovations']
            extracted_patterns.extend(self._extract_patterns_from_innovations(innovations, buildstate_files))
        
        # Extract IDE/development patterns from buildstate content  
        extracted_patterns.extend(self._extract_ide_patterns(buildstate_files))
        
        # Extract workflow patterns from project structures
        extracted_patterns.extend(self._extract_dev_workflow_patterns(buildstate_files))
        
        # Extract testing patterns from coding standards
        extracted_patterns.extend(self._extract_testing_patterns(buildstate_files))
        
        print(f"✅ Extracted {len(extracted_patterns)} meta-patterns from analysis")
        return extracted_patterns
        
    def extract_meta_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract non-project-specific patterns from buildstate files"""
        print("🧠 Extracting meta-patterns from buildstate ecosystem...")
        
        extracted_patterns = []
        
        # Extract IDE configuration patterns
        extracted_patterns.extend(self._extract_ide_patterns(buildstate_files))
        
        # Extract development workflow patterns  
        extracted_patterns.extend(self._extract_dev_workflow_patterns(buildstate_files))
        
        # Extract testing approach patterns
        extracted_patterns.extend(self._extract_testing_patterns(buildstate_files))
        
        # Extract deployment and environment patterns
        extracted_patterns.extend(self._extract_deployment_patterns(buildstate_files))
        
        # Extract bug resolution learnings
        extracted_patterns.extend(self._extract_bug_resolution_patterns(buildstate_files))
        
        # Extract performance optimization patterns
        extracted_patterns.extend(self._extract_performance_patterns(buildstate_files))
        
        print(f"✅ Extracted {len(extracted_patterns)} meta-patterns")
        return extracted_patterns
        
    def _extract_ide_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract IDE configuration patterns"""
        patterns = []
        
        # VS Code settings patterns
        vscode_settings = defaultdict(list)
        tasks_json_patterns = defaultdict(list)
        launch_configs = defaultdict(list)
        
        for bf in buildstate_files:
            project_type = self._detect_project_type(bf)
            
            if bf.file_type == 'json' and isinstance(bf.content, dict):
                content = bf.content
                
                # Look for IDE configuration sections
                if 'ide_config' in content or 'vscode' in content or 'development_environment' in content:
                    ide_config = content.get('ide_config') or content.get('vscode') or content.get('development_environment', {})
                    
                    if 'settings' in ide_config:
                        vscode_settings[project_type].append(ide_config['settings'])
                        
                    if 'tasks' in ide_config:
                        tasks_json_patterns[project_type].append(ide_config['tasks'])
                        
                    if 'launch' in ide_config or 'debug' in ide_config:
                        launch_configs[project_type].append(ide_config.get('launch') or ide_config.get('debug'))
                
                # Look for development workflow sections that include IDE patterns
                if 'dev_workflow' in content:
                    workflow = content['dev_workflow']
                    if isinstance(workflow, dict):
                        # Extract port management patterns
                        if 'port_management' in workflow:
                            port_config = workflow['port_management']
                            patterns.append(MetaPattern(
                                name=f"port_management_{project_type}",
                                category="dev_workflow",
                                project_types=[project_type],
                                pattern_data=port_config,
                                source_projects=[bf.project_name],
                                confidence_score=0.7,
                                applicability_rules={'requires': ['dev_server']},
                                description=f"Port management strategy for {project_type} projects",
                                implementation_guide=[
                                    "Check if port is already in use before starting dev server",
                                    "Use environment variables for port configuration",
                                    "Implement graceful port switching when conflicts occur"
                                ]
                            ))
        
        # Create patterns from collected IDE configurations
        for project_type, settings_list in vscode_settings.items():
            if len(settings_list) >= 2:  # Pattern found in multiple projects
                common_settings = self._find_common_settings(settings_list)
                if common_settings:
                    patterns.append(MetaPattern(
                        name=f"vscode_settings_{project_type}",
                        category="ide_config",
                        project_types=[project_type],
                        pattern_data={'settings.json': common_settings},
                        source_projects=[],
                        confidence_score=len(settings_list) * 0.2,
                        applicability_rules={'ide': 'vscode', 'project_type': project_type},
                        description=f"Optimal VS Code settings for {project_type} projects",
                        implementation_guide=[
                            "Add settings to .vscode/settings.json",
                            "Configure extensions for optimal development experience", 
                            "Set up language-specific formatting and linting"
                        ]
                    ))
                    
        return patterns
        
    def _extract_dev_workflow_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract development workflow patterns"""
        patterns = []
        
        # Common workflow patterns to detect
        workflow_categories = {
            'instance_management': [],
            'development_server': [],
            'hot_reloading': [],
            'environment_setup': [],
            'dependency_management': []
        }
        
        for bf in buildstate_files:
            if bf.file_type == 'json' and isinstance(bf.content, dict):
                content = bf.content
                project_type = self._detect_project_type(bf)
                
                # Extract development workflow patterns
                if 'dev_workflow' in content or 'development' in content:
                    workflow = content.get('dev_workflow') or content.get('development', {})
                    
                    # Instance management patterns
                    if 'instance_management' in workflow or 'port_strategy' in workflow:
                        instance_pattern = workflow.get('instance_management') or workflow.get('port_strategy')
                        workflow_categories['instance_management'].append({
                            'project_type': project_type,
                            'project_name': bf.project_name,
                            'pattern': instance_pattern
                        })
                    
                    # Development server patterns
                    if 'dev_server' in workflow or 'server_config' in workflow:
                        server_pattern = workflow.get('dev_server') or workflow.get('server_config')
                        workflow_categories['development_server'].append({
                            'project_type': project_type,
                            'project_name': bf.project_name,
                            'pattern': server_pattern
                        })
                
                # Extract from stack configuration
                if 'stack' in content or 'tech_stack' in content:
                    stack = content.get('stack') or content.get('tech_stack', {})
                    
                    # Detect hot reloading patterns
                    if isinstance(stack, dict) and 'development' in stack:
                        dev_stack = stack['development']
                        if 'hot_reload' in str(dev_stack).lower() or 'live_reload' in str(dev_stack).lower():
                            workflow_categories['hot_reloading'].append({
                                'project_type': project_type,
                                'project_name': bf.project_name,
                                'pattern': dev_stack
                            })
        
        # Create patterns from collected workflows
        for category, instances in workflow_categories.items():
            if len(instances) >= 2:
                # Group by project type
                by_type = defaultdict(list)
                for instance in instances:
                    by_type[instance['project_type']].append(instance)
                
                for project_type, type_instances in by_type.items():
                    if len(type_instances) >= 2:
                        common_pattern = self._extract_common_workflow_pattern(type_instances)
                        if common_pattern:
                            patterns.append(MetaPattern(
                                name=f"{category}_{project_type}",
                                category="dev_workflow",
                                project_types=[project_type],
                                pattern_data=common_pattern,
                                source_projects=[inst['project_name'] for inst in type_instances],
                                confidence_score=len(type_instances) * 0.3,
                                applicability_rules={'project_type': project_type},
                                description=f"{category.replace('_', ' ').title()} pattern for {project_type}",
                                implementation_guide=self._generate_workflow_implementation_guide(category, common_pattern)
                            ))
                            
        return patterns
        
    def _extract_testing_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract testing approach patterns"""
        patterns = []
        
        testing_approaches = defaultdict(lambda: defaultdict(list))
        
        for bf in buildstate_files:
            if bf.file_type == 'json' and isinstance(bf.content, dict):
                content = bf.content
                project_type = self._detect_project_type(bf)
                
                # Look for testing configurations
                test_config = None
                for key in ['testing', 'tests', 'test_config', 'quality_assurance']:
                    if key in content:
                        test_config = content[key]
                        break
                
                if test_config and isinstance(test_config, dict):
                    # Extract test framework patterns
                    if 'framework' in test_config or 'test_framework' in test_config:
                        framework = test_config.get('framework') or test_config.get('test_framework')
                        testing_approaches[project_type]['frameworks'].append(framework)
                    
                    # Extract coverage patterns
                    if 'coverage' in test_config:
                        coverage = test_config['coverage']
                        testing_approaches[project_type]['coverage'].append(coverage)
                    
                    # Extract test structure patterns
                    if 'structure' in test_config or 'organization' in test_config:
                        structure = test_config.get('structure') or test_config.get('organization')
                        testing_approaches[project_type]['structure'].append(structure)
                
                # Look for testing patterns in coding standards
                if 'coding_standards' in content:
                    standards = content['coding_standards']
                    if isinstance(standards, dict) and 'testing' in standards:
                        test_standards = standards['testing']
                        testing_approaches[project_type]['standards'].append(test_standards)
        
        # Create testing patterns
        for project_type, approaches in testing_approaches.items():
            if sum(len(v) for v in approaches.values()) >= 2:  # Sufficient data
                pattern_data = {}
                
                # Most common test framework
                if approaches['frameworks']:
                    framework_counts = Counter(approaches['frameworks'])
                    pattern_data['recommended_framework'] = framework_counts.most_common(1)[0][0]
                
                # Common coverage patterns
                if approaches['coverage']:
                    pattern_data['coverage_config'] = self._merge_coverage_configs(approaches['coverage'])
                
                # Common structure patterns
                if approaches['structure']:
                    pattern_data['test_structure'] = self._merge_test_structures(approaches['structure'])
                
                if pattern_data:
                    patterns.append(MetaPattern(
                        name=f"testing_approach_{project_type}",
                        category="testing",
                        project_types=[project_type],
                        pattern_data=pattern_data,
                        source_projects=[],
                        confidence_score=sum(len(v) for v in approaches.values()) * 0.15,
                        applicability_rules={'project_type': project_type},
                        description=f"Comprehensive testing approach for {project_type} projects",
                        implementation_guide=self._generate_testing_implementation_guide(pattern_data, project_type)
                    ))
                    
        return patterns
        
    def _extract_deployment_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract deployment and environment patterns"""
        patterns = []
        
        deployment_configs = defaultdict(lambda: defaultdict(list))
        
        for bf in buildstate_files:
            if bf.file_type == 'json' and isinstance(bf.content, dict):
                content = bf.content
                project_type = self._detect_project_type(bf)
                
                # Look for deployment configurations
                deploy_sections = ['deployment', 'deploy', 'environments', 'env_config']
                for section in deploy_sections:
                    if section in content:
                        deploy_config = content[section]
                        if isinstance(deploy_config, dict):
                            # Extract environment patterns
                            if 'environments' in deploy_config:
                                deployment_configs[project_type]['environments'].append(deploy_config['environments'])
                            
                            # Extract build patterns
                            if 'build' in deploy_config or 'build_process' in deploy_config:
                                build_config = deploy_config.get('build') or deploy_config.get('build_process')
                                deployment_configs[project_type]['build'].append(build_config)
                            
                            # Extract CI/CD patterns
                            if 'ci_cd' in deploy_config or 'pipeline' in deploy_config:
                                pipeline = deploy_config.get('ci_cd') or deploy_config.get('pipeline')
                                deployment_configs[project_type]['pipeline'].append(pipeline)
        
        # Create deployment patterns
        for project_type, configs in deployment_configs.items():
            if sum(len(v) for v in configs.values()) >= 2:
                pattern_data = {}
                
                # Environment configuration patterns
                if configs['environments']:
                    pattern_data['environment_setup'] = self._merge_environment_configs(configs['environments'])
                
                # Build process patterns
                if configs['build']:
                    pattern_data['build_process'] = self._merge_build_configs(configs['build'])
                
                if pattern_data:
                    patterns.append(MetaPattern(
                        name=f"deployment_pattern_{project_type}",
                        category="deployment",
                        project_types=[project_type],
                        pattern_data=pattern_data,
                        source_projects=[],
                        confidence_score=sum(len(v) for v in configs.values()) * 0.2,
                        applicability_rules={'project_type': project_type},
                        description=f"Deployment and environment setup pattern for {project_type}",
                        implementation_guide=self._generate_deployment_implementation_guide(pattern_data, project_type)
                    ))
                    
        return patterns
        
    def _extract_bug_resolution_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract bug resolution learnings to prevent repeated time waste"""
        patterns = []
        
        bug_learnings = defaultdict(list)
        
        for bf in buildstate_files:
            if bf.file_type == 'json' and isinstance(bf.content, dict):
                content = bf.content
                project_type = self._detect_project_type(bf)
                
                # Look for bug resolution learnings
                bugs_sections = ['bugs', 'issues', 'bug_learnings', 'troubleshooting']
                for section in bugs_sections:
                    if section in content:
                        bugs = content[section]
                        if isinstance(bugs, list):
                            for bug in bugs:
                                if isinstance(bug, dict) and 'resolution' in bug:
                                    bug_learnings[project_type].append(bug)
                
                # Look in session logs for bug resolution patterns
                if 'session_log' in content:
                    session_log = content['session_log']
                    if isinstance(session_log, list):
                        for entry in session_log:
                            if isinstance(entry, dict):
                                entry_text = str(entry).lower()
                                if any(keyword in entry_text for keyword in ['bug', 'fix', 'debug', 'resolve', 'solution']):
                                    if 'resolution' in entry or 'solution' in entry:
                                        bug_learnings[project_type].append(entry)
        
        # Create bug resolution patterns
        for project_type, learnings in bug_learnings.items():
            if len(learnings) >= 3:  # Need multiple examples to establish pattern
                common_issues = self._categorize_bug_learnings(learnings)
                
                for category, issues in common_issues.items():
                    if len(issues) >= 2:
                        patterns.append(MetaPattern(
                            name=f"bug_resolution_{category}_{project_type}",
                            category="bug_resolution",
                            project_types=[project_type],
                            pattern_data={
                                'category': category,
                                'common_issues': issues,
                                'prevention_strategies': self._extract_prevention_strategies(issues),
                                'diagnostic_approaches': self._extract_diagnostic_approaches(issues)
                            },
                            source_projects=[],
                            confidence_score=len(issues) * 0.25,
                            applicability_rules={'project_type': project_type, 'category': category},
                            description=f"Bug resolution learnings for {category} issues in {project_type}",
                            implementation_guide=self._generate_bug_resolution_guide(category, issues)
                        ))
                        
        return patterns
        
    def _extract_performance_patterns(self, buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract performance optimization patterns"""
        patterns = []
        
        perf_configs = defaultdict(lambda: defaultdict(list))
        
        for bf in buildstate_files:
            if bf.file_type == 'json' and isinstance(bf.content, dict):
                content = bf.content
                project_type = self._detect_project_type(bf)
                
                # Look for performance configurations
                perf_sections = ['performance', 'optimization', 'perf_config', 'metrics']
                for section in perf_sections:
                    if section in content:
                        perf_config = content[section]
                        if isinstance(perf_config, dict):
                            # Extract monitoring patterns
                            if 'monitoring' in perf_config:
                                perf_configs[project_type]['monitoring'].append(perf_config['monitoring'])
                            
                            # Extract optimization patterns
                            if 'optimization' in perf_config or 'optimizations' in perf_config:
                                opts = perf_config.get('optimization') or perf_config.get('optimizations')
                                perf_configs[project_type]['optimization'].append(opts)
                            
                            # Extract benchmarking patterns
                            if 'benchmarks' in perf_config or 'targets' in perf_config:
                                benchmarks = perf_config.get('benchmarks') or perf_config.get('targets')
                                perf_configs[project_type]['benchmarks'].append(benchmarks)
        
        # Create performance patterns
        for project_type, configs in perf_configs.items():
            if sum(len(v) for v in configs.values()) >= 2:
                pattern_data = {}
                
                # Monitoring patterns
                if configs['monitoring']:
                    pattern_data['monitoring_setup'] = self._merge_monitoring_configs(configs['monitoring'])
                
                # Optimization patterns
                if configs['optimization']:
                    pattern_data['common_optimizations'] = self._merge_optimization_configs(configs['optimization'])
                
                if pattern_data:
                    patterns.append(MetaPattern(
                        name=f"performance_pattern_{project_type}",
                        category="performance",
                        project_types=[project_type],
                        pattern_data=pattern_data,
                        source_projects=[],
                        confidence_score=sum(len(v) for v in configs.values()) * 0.2,
                        applicability_rules={'project_type': project_type},
                        description=f"Performance optimization patterns for {project_type}",
                        implementation_guide=self._generate_performance_implementation_guide(pattern_data, project_type)
                    ))
                    
        return patterns
        
    def evaluate_project_for_improvements(self, project_path: Path, 
                                        project_type: str = None) -> Dict[str, Any]:
        """Evaluate a specific project and recommend applicable meta-patterns"""
        print(f"🎯 Evaluating project: {project_path.name}")
        
        # Detect project type if not provided
        if not project_type:
            project_type = self._detect_project_type_from_filesystem(project_path)
            
        # Load project's current buildstate
        current_buildstate = self._load_project_buildstate(project_path)
        
        # Get applicable patterns for this project type
        applicable_patterns = self._get_applicable_patterns(project_type, current_buildstate)
        
        # Analyze what the project is missing
        missing_patterns = self._identify_missing_patterns(current_buildstate, applicable_patterns)
        
        # Generate recommendations
        recommendations = self._generate_project_recommendations(
            project_type, current_buildstate, missing_patterns
        )
        
        return {
            'project_path': str(project_path),
            'project_type': project_type,
            'current_patterns': self._identify_current_patterns(current_buildstate),
            'missing_patterns': missing_patterns,
            'recommendations': recommendations,
            'framework_improvements': self._suggest_framework_improvements(current_buildstate),
            'evaluation_timestamp': datetime.now().isoformat()
        }
        
    def update_framework_library(self, new_patterns: List[MetaPattern], 
                               dry_run: bool = False) -> bool:
        """Update the framework knowledge library with new patterns"""
        print(f"📚 {'[DRY RUN] ' if dry_run else ''}Updating framework library...")
        
        # Merge new patterns with existing knowledge
        updated_knowledge = self._merge_patterns_into_framework(new_patterns)
        
        # Update project type profiles
        updated_profiles = self._update_project_type_profiles(new_patterns)
        
        if not dry_run:
            # Save updated framework library
            self.framework_library_path.parent.mkdir(parents=True, exist_ok=True)
            
            framework_data = {
                'meta_patterns': updated_knowledge,
                'project_type_profiles': updated_profiles,
                'last_updated': datetime.now().isoformat(),
                'version': '1.1'
            }
            
            with open(self.framework_library_path, 'w') as f:
                json.dump(framework_data, f, indent=2)
                
            print(f"✅ Framework library updated: {self.framework_library_path}")
            return True
        else:
            print(f"[DRY RUN] Would update framework library with {len(new_patterns)} patterns")
            return True
            
    def _detect_project_type(self, buildstate_file) -> str:
        """Detect project type from buildstate content"""
        if hasattr(buildstate_file, 'content') and isinstance(buildstate_file.content, dict):
            content = buildstate_file.content
            
            # Check explicit project type
            project_info = content.get('project', {})
            if isinstance(project_info, dict) and 'type' in project_info:
                explicit_type = project_info['type'].lower()
                for ptype in self.project_type_indicators:
                    if ptype.replace('_', ' ') in explicit_type or ptype in explicit_type:
                        return ptype
            
            # Check tech stack
            stack = content.get('stack') or content.get('tech_stack', [])
            if isinstance(stack, dict):
                stack = list(stack.values())
            elif isinstance(stack, str):
                stack = [stack]
            
            if stack:
                stack_str = ' '.join(str(s).lower() for s in stack)
                for ptype, indicators in self.project_type_indicators.items():
                    if any(indicator in stack_str for indicator in indicators):
                        return ptype
                        
        return 'unknown'
        
    def _detect_project_type_from_filesystem(self, project_path: Path) -> str:
        """Detect project type from filesystem structure and files"""
        # Check for common project files
        files_in_project = [f.name.lower() for f in project_path.iterdir() if f.is_file()]
        
        # Web application indicators
        if any(f in files_in_project for f in ['package.json', 'webpack.config.js', 'vite.config.js']):
            return 'web_application'
            
        # Python project indicators
        if any(f in files_in_project for f in ['setup.py', 'pyproject.toml', 'requirements.txt']):
            if 'main.py' in files_in_project or any('gui' in f or 'qt' in f for f in files_in_project):
                return 'desktop_application'
            return 'cli_tool'
            
        # Mobile application indicators
        if any(f in files_in_project for f in ['pubspec.yaml', 'android', 'ios']):
            return 'mobile_application'
            
        return 'unknown'
        
    def _extract_patterns_from_innovations(self, innovations: List[Dict], 
                                         buildstate_files: List[Any]) -> List[MetaPattern]:
        """Extract meta-patterns from discovered innovations"""
        patterns = []
        
        # Group innovations by type and look for cross-project patterns
        innovation_groups = defaultdict(list)
        for innovation in innovations:
            category = innovation.get('type', 'unknown')
            innovation_groups[category].append(innovation)
            
        # Extract patterns for each innovation category
        for category, category_innovations in innovation_groups.items():
            if len(category_innovations) >= 3:  # Pattern needs multiple examples
                
                # Look for field patterns (common configuration approaches)
                if 'field_pattern' in str(category_innovations[0].get('name', '')):
                    field_patterns = self._analyze_field_patterns(category_innovations)
                    patterns.extend(field_patterns)
                    
                # Look for framework patterns (development approach patterns)
                elif category == 'framework':
                    framework_patterns = self._analyze_framework_patterns(category_innovations)
                    patterns.extend(framework_patterns)
                    
                # Look for structure patterns (project organization patterns)  
                elif category == 'structure':
                    structure_patterns = self._analyze_structure_patterns(category_innovations)
                    patterns.extend(structure_patterns)
                    
        return patterns
        
    def _analyze_field_patterns(self, innovations: List[Dict]) -> List[MetaPattern]:
        """Analyze field pattern innovations to extract universal configuration approaches"""
        patterns = []
        
        # Group by field name to find common configuration patterns
        field_groups = defaultdict(list)
        for innovation in innovations:
            field_name = innovation.get('name', '').replace('field_pattern_', '')
            field_groups[field_name].append(innovation)
            
        # Create patterns for widely used fields
        for field_name, field_innovations in field_groups.items():
            if len(field_innovations) >= 2:  # Used across multiple projects
                
                # Analyze the pattern data
                pattern_data = {
                    'field_name': field_name,
                    'usage_frequency': len(field_innovations),
                    'description': field_innovations[0].get('description', f'Configuration pattern for {field_name}'),
                    'impact_score': sum(innov.get('impact', 0) for innov in field_innovations) / len(field_innovations)
                }
                
                patterns.append(MetaPattern(
                    name=f"config_field_{field_name}",
                    category="configuration", 
                    project_types=['all'],  # Field patterns apply broadly
                    pattern_data=pattern_data,
                    source_projects=[],
                    confidence_score=len(field_innovations) * 0.3,
                    applicability_rules={'has_configuration': True},
                    description=f"Standardized configuration pattern for {field_name} field",
                    implementation_guide=[
                        f"Add {field_name} field to project configuration",
                        f"Follow established structure for {field_name} data",
                        "Maintain consistency with other projects using this pattern",
                        "Document the field usage for team members"
                    ]
                ))
                
        return patterns
        
    def _analyze_framework_patterns(self, innovations: List[Dict]) -> List[MetaPattern]:
        """Analyze framework innovations to extract development approach patterns"""
        patterns = []
        
        # Look for framework adoption patterns
        framework_adoptions = [i for i in innovations if 'framework' in i.get('name', '').lower()]
        
        if len(framework_adoptions) >= 2:
            pattern_data = {
                'adoption_count': len(framework_adoptions),
                'framework_type': 'scf_framework' if 'scf' in str(framework_adoptions).lower() else 'general',
                'benefits': [innov.get('description', 'Framework integration') for innov in framework_adoptions[:3]]
            }
            
            patterns.append(MetaPattern(
                name="framework_adoption_pattern",
                category="framework_integration",
                project_types=['all'],  # Framework patterns apply broadly
                pattern_data=pattern_data,
                source_projects=[],
                confidence_score=len(framework_adoptions) * 0.4,
                applicability_rules={'needs_framework': True},
                description="Standardized approach to framework adoption and integration",
                implementation_guide=[
                    "Follow established framework integration patterns",
                    "Document framework adoption decisions and rationale",
                    "Implement consistent configuration across similar projects",
                    "Share framework learnings with other projects"
                ]
            ))
            
        return patterns
        
    def _analyze_structure_patterns(self, innovations: List[Dict]) -> List[MetaPattern]:
        """Analyze structural innovations to extract project organization patterns"""
        patterns = []
        
        # Group structure innovations by type
        structure_types = defaultdict(list)
        for innovation in innovations:
            struct_type = innovation.get('category', 'general')
            structure_types[struct_type].append(innovation)
            
        # Create patterns for common structural approaches
        for struct_type, structures in structure_types.items():
            if len(structures) >= 5:  # Need multiple examples for structure patterns
                
                pattern_data = {
                    'structure_type': struct_type,
                    'element_count': len(structures),
                    'common_names': [s.get('name', 'unknown')[:50] for s in structures[:5]],  # Top 5 examples
                    'avg_impact': sum(s.get('impact', 0) for s in structures) / len(structures)
                }
                
                patterns.append(MetaPattern(
                    name=f"structure_pattern_{struct_type}",
                    category="project_structure",
                    project_types=['all'],  # Structure patterns can apply broadly
                    pattern_data=pattern_data,
                    source_projects=[],
                    confidence_score=len(structures) * 0.1,  # Lower confidence for structure patterns
                    applicability_rules={'needs_structure': True},
                    description=f"Project organization pattern for {struct_type} elements",
                    implementation_guide=[
                        f"Organize {struct_type} elements following established patterns",
                        "Maintain consistent project structure across similar projects", 
                        "Document structural decisions for team clarity",
                        "Review and refine structure based on project evolution"
                    ]
                ))
                
        return patterns

    # Helper methods for pattern extraction and merging
    def _find_common_settings(self, settings_list: List[Dict]) -> Dict[str, Any]:
        """Find common settings across multiple configurations"""
        if not settings_list:
            return {}
            
        common = {}
        for key in settings_list[0].keys():
            values = [s.get(key) for s in settings_list if key in s]
            if len(values) >= len(settings_list) * 0.6:  # Present in 60% of configs
                # Take the most common value
                from collections import Counter
                value_counts = Counter(str(v) for v in values)
                most_common = value_counts.most_common(1)[0][0]
                try:
                    common[key] = json.loads(most_common)
                except:
                    common[key] = most_common
                    
        return common
        
    def _extract_common_workflow_pattern(self, instances: List[Dict]) -> Dict[str, Any]:
        """Extract common workflow pattern from multiple instances"""
        patterns = [inst['pattern'] for inst in instances if inst['pattern']]
        if not patterns:
            return {}
            
        common_pattern = {}
        
        # Find common keys
        all_keys = set()
        for pattern in patterns:
            if isinstance(pattern, dict):
                all_keys.update(pattern.keys())
                
        # For each key, find the most common value
        for key in all_keys:
            values = [p.get(key) for p in patterns if isinstance(p, dict) and key in p]
            if len(values) >= len(patterns) * 0.5:  # Present in 50% of patterns
                if all(isinstance(v, bool) for v in values):
                    common_pattern[key] = any(values)  # Use True if any is True
                elif all(isinstance(v, (int, float)) for v in values):
                    common_pattern[key] = sum(values) / len(values)  # Average
                else:
                    # Take most common string value
                    from collections import Counter
                    value_counts = Counter(str(v) for v in values)
                    common_pattern[key] = value_counts.most_common(1)[0][0]
                    
        return common_pattern
        
    def _generate_workflow_implementation_guide(self, category: str, pattern: Dict) -> List[str]:
        """Generate implementation guide for workflow patterns"""
        guides = {
            'instance_management': [
                "Check for existing process before starting new instance",
                "Use PID files or port checking to detect running instances",
                "Implement graceful shutdown handling",
                "Configure process monitoring and auto-restart if needed"
            ],
            'development_server': [
                "Configure hot reloading for faster development",
                "Set up environment-specific configuration",
                "Implement proper error handling and logging",
                "Use consistent port management across team"
            ],
            'hot_reloading': [
                "Configure file watchers for source code changes",
                "Set up automatic browser refresh for web projects",
                "Implement efficient change detection algorithms",
                "Handle asset reloading separately from code reloading"
            ]
        }
        
        return guides.get(category, [
            "Implement the pattern according to project-specific requirements",
            "Test the implementation thoroughly in development environment",
            "Document the configuration for team members",
            "Monitor performance impact and optimize as needed"
        ])
        
    def _merge_coverage_configs(self, coverage_configs: List[Any]) -> Dict[str, Any]:
        """Merge multiple coverage configurations into common pattern"""
        merged = {}
        
        # Extract common coverage targets
        thresholds = []
        for config in coverage_configs:
            if isinstance(config, dict):
                if 'threshold' in config:
                    thresholds.append(config['threshold'])
                elif 'target' in config:
                    thresholds.append(config['target'])
                    
        if thresholds:
            # Convert to numbers and find average
            numeric_thresholds = []
            for t in thresholds:
                if isinstance(t, (int, float)):
                    numeric_thresholds.append(t)
                elif isinstance(t, str) and '%' in t:
                    try:
                        numeric_thresholds.append(float(t.replace('%', '')))
                    except:
                        pass
                        
            if numeric_thresholds:
                merged['recommended_threshold'] = f"{sum(numeric_thresholds) / len(numeric_thresholds):.0f}%"
                
        return merged
        
    def _merge_test_structures(self, structures: List[Any]) -> Dict[str, Any]:
        """Merge test structure patterns"""
        merged = {}
        
        # Common directory patterns
        common_dirs = []
        for structure in structures:
            if isinstance(structure, dict) and 'directories' in structure:
                dirs = structure['directories']
                if isinstance(dirs, list):
                    common_dirs.extend(dirs)
                    
        if common_dirs:
            from collections import Counter
            dir_counts = Counter(common_dirs)
            merged['recommended_directories'] = [d for d, c in dir_counts.most_common(5)]
            
        return merged
        
    # Additional helper methods would continue here...
    # (Implementing all the helper methods for merging configs, generating guides, etc.)
        
    def _load_project_buildstate(self, project_path: Path) -> Dict[str, Any]:
        """Load project's current buildstate"""
        buildstate_files = ['buildstate.json', 'BUILDSTATE.json', '.buildstate.json']
        
        for filename in buildstate_files:
            file_path = project_path / filename
            if file_path.exists():
                try:
                    with open(file_path) as f:
                        return json.load(f)
                except Exception as e:
                    print(f"⚠️  Error loading {filename}: {e}")
                    
        return {}
        
    def _get_applicable_patterns(self, project_type: str, 
                               current_buildstate: Dict) -> List[MetaPattern]:
        """Get patterns applicable to this project type"""
        applicable = []
        
        for pattern_name, pattern_data in self.framework_knowledge.get('meta_patterns', {}).items():
            if project_type in pattern_data.get('project_types', []):
                # Check applicability rules
                rules = pattern_data.get('applicability_rules', {})
                if self._check_applicability_rules(rules, current_buildstate, project_type):
                    # Convert dict back to MetaPattern object
                    pattern = MetaPattern(
                        name=pattern_data['name'],
                        category=pattern_data['category'],
                        project_types=pattern_data['project_types'],
                        pattern_data=pattern_data['pattern_data'],
                        source_projects=pattern_data.get('source_projects', []),
                        confidence_score=pattern_data.get('confidence_score', 0.0),
                        applicability_rules=pattern_data.get('applicability_rules', {}),
                        description=pattern_data.get('description', ''),
                        implementation_guide=pattern_data.get('implementation_guide', [])
                    )
                    applicable.append(pattern)
                    
        return applicable
        
    def _check_applicability_rules(self, rules: Dict, buildstate: Dict, project_type: str) -> bool:
        """Check if applicability rules are met"""
        if not rules:
            return True
            
        # Check project type rule
        if 'project_type' in rules and rules['project_type'] != project_type:
            return False
            
        # Check requires rule
        if 'requires' in rules:
            required = rules['requires']
            if isinstance(required, str):
                required = [required]
            for req in required:
                if req not in str(buildstate):
                    return False
                    
        # Check excludes rule
        if 'excludes' in rules:
            excluded = rules['excludes']
            if isinstance(excluded, str):
                excluded = [excluded]
            for excl in excluded:
                if excl in str(buildstate):
                    return False
                    
        return True
        
    def _identify_missing_patterns(self, current_buildstate: Dict, 
                                 applicable_patterns: List[MetaPattern]) -> List[MetaPattern]:
        """Identify patterns that are missing from current buildstate"""
        missing = []
        
        for pattern in applicable_patterns:
            if not self._pattern_exists_in_buildstate(pattern, current_buildstate):
                missing.append(pattern)
                
        return missing
        
    def _pattern_exists_in_buildstate(self, pattern: MetaPattern, buildstate: Dict) -> bool:
        """Check if pattern already exists in buildstate"""
        category = pattern.category
        
        if category == 'ide_config':
            return 'ide_config' in buildstate or 'vscode' in buildstate
        elif category == 'dev_workflow':
            return 'dev_workflow' in buildstate or 'development' in buildstate
        elif category == 'testing':
            return 'testing' in buildstate or 'tests' in buildstate
        elif category == 'deployment':
            return 'deployment' in buildstate or 'deploy' in buildstate
        elif category == 'performance':
            return 'performance' in buildstate or 'optimization' in buildstate
        elif category == 'bug_resolution':
            return 'bug_learnings' in buildstate or 'troubleshooting' in buildstate
            
        return False
        
    def _generate_project_recommendations(self, project_type: str, current_buildstate: Dict,
                                        missing_patterns: List[MetaPattern]) -> List[Dict]:
        """Generate specific recommendations for the project"""
        recommendations = []
        
        for pattern in missing_patterns:
            recommendation = {
                'pattern_name': pattern.name,
                'category': pattern.category,
                'description': pattern.description,
                'confidence_score': pattern.confidence_score,
                'implementation_guide': pattern.implementation_guide,
                'pattern_data': pattern.pattern_data,
                'priority': self._calculate_recommendation_priority(pattern, current_buildstate),
                'effort_estimate': self._estimate_implementation_effort(pattern, project_type),
                'expected_benefits': self._describe_expected_benefits(pattern, project_type)
            }
            recommendations.append(recommendation)
            
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations
        
    def _calculate_recommendation_priority(self, pattern: MetaPattern, buildstate: Dict) -> float:
        """Calculate priority score for recommendation"""
        priority = pattern.confidence_score
        
        # Boost priority for missing critical patterns
        if pattern.category in ['dev_workflow', 'testing']:
            priority += 0.3
            
        # Boost if project seems mature but missing pattern
        if len(str(buildstate)) > 5000:  # Large buildstate indicates mature project
            priority += 0.2
            
        return priority
        
    def _estimate_implementation_effort(self, pattern: MetaPattern, project_type: str) -> str:
        """Estimate implementation effort"""
        effort_map = {
            'ide_config': 'Low (1-2 hours)',
            'dev_workflow': 'Medium (1-2 days)', 
            'testing': 'High (1-2 weeks)',
            'deployment': 'High (1-2 weeks)',
            'performance': 'Medium (2-5 days)',
            'bug_resolution': 'Low (documentation only)'
        }
        
        return effort_map.get(pattern.category, 'Medium (1-5 days)')
        
    def _describe_expected_benefits(self, pattern: MetaPattern, project_type: str) -> List[str]:
        """Describe expected benefits of implementing pattern"""
        benefits_map = {
            'ide_config': [
                "Improved developer experience and productivity",
                "Consistent development environment across team",
                "Better code formatting and error detection"
            ],
            'dev_workflow': [
                "Faster development iteration cycles",
                "Reduced setup time for new developers",
                "More reliable development processes"
            ],
            'testing': [
                "Higher code quality and reliability",
                "Faster bug detection and resolution",
                "Improved confidence in deployments"
            ],
            'deployment': [
                "More reliable and consistent deployments",
                "Reduced deployment-related issues",
                "Better environment management"
            ],
            'performance': [
                "Better application performance",
                "Faster identification of performance issues",
                "Improved user experience"
            ],
            'bug_resolution': [
                "Faster resolution of similar issues in future",
                "Reduced debugging time",
                "Improved team knowledge sharing"
            ]
        }
        
        return benefits_map.get(pattern.category, ["Improved development experience"])
        
    def _suggest_framework_improvements(self, current_buildstate: Dict) -> List[Dict]:
        """Suggest improvements to the SCF framework based on project patterns"""
        suggestions = []
        
        # Look for novel patterns that could be added to framework
        novel_patterns = self._identify_novel_patterns(current_buildstate)
        
        for pattern_data in novel_patterns:
            suggestion = {
                'type': 'framework_enhancement',
                'description': f"Add support for {pattern_data['category']} patterns",
                'rationale': f"Project uses {pattern_data['name']} which isn't in framework library",
                'implementation': f"Extract pattern and add to {pattern_data['category']} category",
                'benefit': "Would help other similar projects adopt this successful pattern"
            }
            suggestions.append(suggestion)
            
        return suggestions
        
    def _identify_novel_patterns(self, buildstate: Dict) -> List[Dict]:
        """Identify patterns in buildstate that aren't in framework library yet"""
        novel = []
        
        # Check for sections not covered by existing patterns
        framework_sections = set()
        for pattern_data in self.framework_knowledge.get('meta_patterns', {}).values():
            if 'category' in pattern_data:
                framework_sections.add(pattern_data['category'])
                
        # Look for buildstate sections that don't map to known categories
        for key in buildstate.keys():
            if key not in ['_scf_header', 'meta', 'project', 'current_state']:
                # Check if this represents a novel category
                if not any(cat in key.lower() for cat in framework_sections):
                    novel.append({
                        'name': key,
                        'category': 'unknown',
                        'data': buildstate[key],
                        'potential_category': self._infer_category_from_content(buildstate[key])
                    })
                    
        return novel
        
    def _infer_category_from_content(self, content: Any) -> str:
        """Infer category from content structure"""
        if isinstance(content, dict):
            keys = list(content.keys())
            key_str = ' '.join(keys).lower()
            
            if any(word in key_str for word in ['config', 'settings', 'preferences']):
                return 'configuration'
            elif any(word in key_str for word in ['test', 'spec', 'coverage']):
                return 'testing'
            elif any(word in key_str for word in ['deploy', 'build', 'release']):
                return 'deployment'
            elif any(word in key_str for word in ['perf', 'metric', 'monitor']):
                return 'performance'
            elif any(word in key_str for word in ['workflow', 'process', 'pipeline']):
                return 'dev_workflow'
                
        return 'misc'
        
    def _merge_patterns_into_framework(self, new_patterns: List[MetaPattern]) -> Dict[str, Any]:
        """Merge new patterns into existing framework knowledge"""
        merged = self.framework_knowledge.get('meta_patterns', {}).copy()
        
        for pattern in new_patterns:
            pattern_dict = {
                'name': pattern.name,
                'category': pattern.category,
                'project_types': pattern.project_types,
                'pattern_data': pattern.pattern_data,
                'source_projects': pattern.source_projects,
                'confidence_score': pattern.confidence_score,
                'applicability_rules': pattern.applicability_rules,
                'description': pattern.description,
                'implementation_guide': pattern.implementation_guide,
                'created_date': datetime.now().isoformat()
            }
            
            # Merge with existing pattern if it exists
            if pattern.name in merged:
                existing = merged[pattern.name]
                # Update confidence score based on additional evidence
                existing['confidence_score'] = max(existing.get('confidence_score', 0), pattern.confidence_score)
                # Merge source projects
                existing_sources = set(existing.get('source_projects', []))
                new_sources = set(pattern.source_projects)
                existing['source_projects'] = list(existing_sources | new_sources)
                # Update other fields if new pattern has higher confidence
                if pattern.confidence_score > existing.get('confidence_score', 0):
                    existing.update(pattern_dict)
            else:
                merged[pattern.name] = pattern_dict
                
        return merged
        
    def _update_project_type_profiles(self, new_patterns: List[MetaPattern]) -> Dict[str, Any]:
        """Update project type profiles with new patterns"""
        profiles = self.framework_knowledge.get('project_type_profiles', {}).copy()
        
        # Group patterns by project type
        by_type = defaultdict(list)
        for pattern in new_patterns:
            for ptype in pattern.project_types:
                by_type[ptype].append(pattern)
                
        # Update each project type profile
        for project_type, type_patterns in by_type.items():
            if project_type not in profiles:
                profiles[project_type] = {
                    'project_type': project_type,
                    'common_patterns': [],
                    'pattern_categories': defaultdict(list)
                }
                
            profile = profiles[project_type]
            
            # Add new patterns to profile
            for pattern in type_patterns:
                profile['common_patterns'].append(pattern.name)
                profile['pattern_categories'][pattern.category].append(pattern.name)
                
            # Update profile statistics
            profile['last_updated'] = datetime.now().isoformat()
            profile['pattern_count'] = len(set(profile['common_patterns']))
            
        return profiles

def main():
    """Main entry point for SCF Meta-Learning Evaluator"""
    parser = argparse.ArgumentParser(description='SCF Meta-Learning Evaluator - Extract and apply cross-project patterns')
    parser.add_argument('--scan-path', action='append', help='Paths to scan for buildstate files')
    parser.add_argument('--extract-patterns', action='store_true', help='Extract meta-patterns from discovered buildstate files')
    parser.add_argument('--evaluate-project', type=Path, help='Evaluate specific project for improvements')
    parser.add_argument('--project-type', type=str, help='Specify project type for evaluation')
    parser.add_argument('--update-framework-library', action='store_true', help='Update framework knowledge library')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--library-path', type=Path, help='Path to framework library file')
    
    args = parser.parse_args()
    
    # Initialize meta-learner
    meta_learner = SCFMetaLearner(framework_library_path=args.library_path)
    
    print("🧠 SCF Meta-Learning Evaluator - Pattern Extraction & Framework Enhancement")
    print("=" * 80)
    
    if args.extract_patterns or args.update_framework_library:
        # Import the buildstate hunter to get files
        try:
            from buildstate_hunter_learner import BuildstateHunter, InnovationLearner
            
            # Hunt for buildstate files and analyze them
            scan_paths = [Path(p) for p in args.scan_path] if args.scan_path else [Path.cwd().parent]
            hunter = BuildstateHunter(scan_paths)
            buildstate_files = hunter.hunt_buildstate_files()
            
            if not buildstate_files:
                print("❌ No buildstate files found!")
                return 1
                
            # Use the innovation learner to get detailed analysis
            learner = InnovationLearner()
            innovations = learner.learn_from_files(buildstate_files)
            
            # Convert innovations to analysis results format
            analysis_results = {'innovations': [
                {
                    'name': innov.name,
                    'description': innov.description,
                    'type': innov.category,
                    'impact': innov.value_score,
                    'source_files': innov.source_files
                } 
                for innov in innovations
            ]}
            
            # Extract meta-patterns using the rich analysis data
            meta_patterns = meta_learner.extract_meta_patterns_from_analysis(buildstate_files, analysis_results)
            
            print(f"\n📊 META-PATTERN EXTRACTION RESULTS:")
            print(f"   🔍 Analyzed: {len(buildstate_files)} buildstate files")
            print(f"   📈 Extracted: {len(meta_patterns)} meta-patterns")
            
            # Group patterns by category
            by_category = defaultdict(list)
            for pattern in meta_patterns:
                by_category[pattern.category].append(pattern)
                
            print(f"\n📋 PATTERNS BY CATEGORY:")
            for category, patterns in by_category.items():
                print(f"   🏷️  {category.title()}: {len(patterns)} patterns")
                if args.verbose:
                    for pattern in patterns[:3]:  # Show top 3
                        print(f"      • {pattern.name} (confidence: {pattern.confidence_score:.2f})")
                        
            # Update framework library if requested
            if args.update_framework_library:
                success = meta_learner.update_framework_library(meta_patterns, dry_run=args.dry_run)
                if success:
                    print(f"\n✅ Framework library updated with {len(meta_patterns)} patterns")
                    
        except ImportError:
            print("❌ buildstate_hunter_learner module required for pattern extraction")
            return 1
            
    elif args.evaluate_project:
        # Evaluate specific project
        if not args.evaluate_project.exists():
            print(f"❌ Project path does not exist: {args.evaluate_project}")
            return 1
            
        evaluation = meta_learner.evaluate_project_for_improvements(
            args.evaluate_project, args.project_type
        )
        
        print(f"\n🎯 PROJECT EVALUATION RESULTS:")
        print(f"   📁 Project: {evaluation['project_path']}")
        print(f"   🏷️  Type: {evaluation['project_type']}")
        print(f"   ✅ Current Patterns: {len(evaluation['current_patterns'])}")
        print(f"   ❌ Missing Patterns: {len(evaluation['missing_patterns'])}")
        print(f"   💡 Recommendations: {len(evaluation['recommendations'])}")
        
        if evaluation['recommendations']:
            print(f"\n🚀 TOP RECOMMENDATIONS:")
            for i, rec in enumerate(evaluation['recommendations'][:5], 1):
                print(f"   {i}. {rec['pattern_name']} ({rec['category']})")
                print(f"      📝 {rec['description']}")
                print(f"      📊 Priority: {rec['priority']:.2f}, Effort: {rec['effort_estimate']}")
                print(f"      💡 Benefits: {', '.join(rec['expected_benefits'][:2])}")
                print()
                
        if evaluation['framework_improvements']:
            print(f"🔧 FRAMEWORK IMPROVEMENT SUGGESTIONS:")
            for suggestion in evaluation['framework_improvements']:
                print(f"   • {suggestion['description']}")
                print(f"     💭 {suggestion['rationale']}")
                
    else:
        print("❓ Please specify an action: --extract-patterns, --evaluate-project, or --update-framework-library")
        return 1
        
    return 0

if __name__ == '__main__':
    sys.exit(main())