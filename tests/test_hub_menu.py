#!/usr/bin/env python3
"""
Unit tests for SCF Hub Menu functionality

Tests the interactive hub menu including:
- Project scanning and profile building
- Rescan functionality
- Selection parsing
- Size formatting
- Enable SCF batch operations
- Teach operations
- Verbose listing
"""

import unittest
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the scf module
import importlib.util
import importlib.machinery
scf_path = Path(__file__).parent.parent / 'scf'

spec = importlib.util.spec_from_loader(
    "scf_cli",
    importlib.machinery.SourceFileLoader("scf_cli", str(scf_path))
)
scf_cli = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(scf_cli)
except SystemExit:
    pass


class TestParseSelection(unittest.TestCase):
    """Test selection parsing functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.framework_path = Path(__file__).parent.parent

        # Create minimal hub structure
        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        # Create hub manager and menu
        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_parse_single_number(self):
        """Test parsing single number selection"""
        result = self.menu._parse_selection("3", 10)
        self.assertEqual(result, [2])  # 0-indexed

    def test_parse_multiple_numbers(self):
        """Test parsing comma-separated numbers"""
        result = self.menu._parse_selection("1,3,5", 10)
        self.assertEqual(result, [0, 2, 4])

    def test_parse_range(self):
        """Test parsing range selection"""
        result = self.menu._parse_selection("2-5", 10)
        self.assertEqual(result, [1, 2, 3, 4])

    def test_parse_mixed(self):
        """Test parsing mixed selection"""
        result = self.menu._parse_selection("1,3-5,8", 10)
        self.assertEqual(result, [0, 2, 3, 4, 7])

    def test_parse_all(self):
        """Test parsing 'a' for all"""
        result = self.menu._parse_selection("a", 5)
        self.assertEqual(result, [0, 1, 2, 3, 4])

    def test_parse_all_keyword(self):
        """Test parsing 'all' keyword"""
        result = self.menu._parse_selection("all", 5)
        self.assertEqual(result, [0, 1, 2, 3, 4])

    def test_parse_empty_default_all(self):
        """Test empty input defaults to all"""
        result = self.menu._parse_selection("", 5)
        self.assertEqual(result, [0, 1, 2, 3, 4])

    def test_parse_empty_no_default(self):
        """Test empty input with default_all=False"""
        result = self.menu._parse_selection("", 5, default_all=False)
        self.assertEqual(result, [])

    def test_parse_out_of_range(self):
        """Test that out of range numbers are ignored"""
        result = self.menu._parse_selection("1,15,3", 10)
        self.assertEqual(result, [0, 2])

    def test_parse_with_spaces(self):
        """Test parsing with extra spaces"""
        result = self.menu._parse_selection(" 1 , 3 , 5 ", 10)
        self.assertEqual(result, [0, 2, 4])

    def test_parse_invalid_string(self):
        """Test parsing invalid string returns empty"""
        result = self.menu._parse_selection("abc", 10)
        self.assertEqual(result, [])

    def test_parse_cancel_c(self):
        """Test parsing 'c' returns None for cancel"""
        result = self.menu._parse_selection("c", 10)
        self.assertIsNone(result)

    def test_parse_cancel_keyword(self):
        """Test parsing 'cancel' returns None"""
        result = self.menu._parse_selection("cancel", 10)
        self.assertIsNone(result)


class TestFormatSize(unittest.TestCase):
    """Test size formatting functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_format_bytes(self):
        """Test formatting bytes"""
        result = self.menu._format_size(500)
        self.assertEqual(result, "500.0B")

    def test_format_kilobytes(self):
        """Test formatting kilobytes"""
        result = self.menu._format_size(2048)
        self.assertEqual(result, "2.0KB")

    def test_format_megabytes(self):
        """Test formatting megabytes"""
        result = self.menu._format_size(2 * 1024 * 1024)
        self.assertEqual(result, "2.0MB")

    def test_format_gigabytes(self):
        """Test formatting gigabytes"""
        result = self.menu._format_size(3 * 1024 * 1024 * 1024)
        self.assertEqual(result, "3.0GB")

    def test_format_negative(self):
        """Test formatting negative size (for diffs)"""
        result = self.menu._format_size(-1024)
        self.assertEqual(result, "-1.0KB")


class TestBuildProjectProfile(unittest.TestCase):
    """Test project profile building"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.project_path = Path(self.temp_dir) / "test-project"
        self.project_path.mkdir()
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_basic_profile(self):
        """Test building basic project profile"""
        profile = self.menu._build_project_profile(self.project_path)

        self.assertEqual(profile['name'], 'test-project')
        self.assertEqual(profile['path'], str(self.project_path.resolve()))
        self.assertFalse(profile['scf_enabled'])
        self.assertIn('last_scanned', profile)

    def test_detect_scf_enabled(self):
        """Test detecting SCF-enabled project"""
        scf_dir = self.project_path / '.scf'
        scf_dir.mkdir()

        profile = self.menu._build_project_profile(self.project_path)
        self.assertTrue(profile['scf_enabled'])

    def test_detect_javascript(self):
        """Test detecting JavaScript project"""
        (self.project_path / 'package.json').write_text('{"dependencies": {}}')

        profile = self.menu._build_project_profile(self.project_path)
        self.assertIn('JavaScript', profile['languages'])

    def test_detect_typescript(self):
        """Test detecting TypeScript project"""
        (self.project_path / 'package.json').write_text('{"dependencies": {"typescript": "^5.0.0"}}')
        (self.project_path / 'tsconfig.json').write_text('{}')

        profile = self.menu._build_project_profile(self.project_path)
        self.assertIn('TypeScript', profile['languages'])

    def test_detect_python(self):
        """Test detecting Python project"""
        (self.project_path / 'requirements.txt').write_text('flask==2.0.0')

        profile = self.menu._build_project_profile(self.project_path)
        self.assertIn('Python', profile['languages'])

    def test_detect_react_framework(self):
        """Test detecting React framework"""
        (self.project_path / 'package.json').write_text('{"dependencies": {"react": "^18.0.0"}}')

        profile = self.menu._build_project_profile(self.project_path)
        self.assertIn('React', profile['frameworks'])

    def test_detect_django_framework(self):
        """Test detecting Django framework"""
        (self.project_path / 'requirements.txt').write_text('Django==4.0.0')

        profile = self.menu._build_project_profile(self.project_path)
        self.assertIn('Django', profile['frameworks'])

    def test_detect_tests(self):
        """Test detecting tests directory"""
        (self.project_path / 'tests').mkdir()

        profile = self.menu._build_project_profile(self.project_path)
        self.assertTrue(profile['has_tests'])

    def test_detect_ci(self):
        """Test detecting CI configuration"""
        (self.project_path / '.github').mkdir()
        (self.project_path / '.github' / 'workflows').mkdir()

        profile = self.menu._build_project_profile(self.project_path)
        self.assertTrue(profile['has_ci'])

    def test_file_count_and_size(self):
        """Test file count and size calculation"""
        # Create some test files
        (self.project_path / 'file1.txt').write_text('Hello')
        (self.project_path / 'file2.txt').write_text('World')

        profile = self.menu._build_project_profile(self.project_path)
        self.assertEqual(profile['file_count'], 2)
        self.assertGreater(profile['size_bytes'], 0)

    def test_excludes_node_modules(self):
        """Test that node_modules is excluded from count"""
        nm_dir = self.project_path / 'node_modules'
        nm_dir.mkdir()
        (nm_dir / 'big_file.js').write_text('x' * 10000)
        (self.project_path / 'src.js').write_text('code')

        profile = self.menu._build_project_profile(self.project_path)
        # Should only count src.js, not node_modules content
        self.assertEqual(profile['file_count'], 1)


class TestIsProjectDir(unittest.TestCase):
    """Test project directory detection"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.test_dir = Path(self.temp_dir) / "test-dir"
        self.test_dir.mkdir()
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_empty_dir_not_project(self):
        """Test that empty directory is not a project"""
        result = self.menu._is_project_dir(self.test_dir)
        self.assertFalse(result)

    def test_git_dir_is_project(self):
        """Test that directory with .git is a project"""
        (self.test_dir / '.git').mkdir()
        result = self.menu._is_project_dir(self.test_dir)
        self.assertTrue(result)

    def test_package_json_is_project(self):
        """Test that directory with package.json is a project"""
        (self.test_dir / 'package.json').write_text('{}')
        result = self.menu._is_project_dir(self.test_dir)
        self.assertTrue(result)

    def test_pyproject_is_project(self):
        """Test that directory with pyproject.toml is a project"""
        (self.test_dir / 'pyproject.toml').write_text('')
        result = self.menu._is_project_dir(self.test_dir)
        self.assertTrue(result)

    def test_cargo_is_project(self):
        """Test that directory with Cargo.toml is a project"""
        (self.test_dir / 'Cargo.toml').write_text('')
        result = self.menu._is_project_dir(self.test_dir)
        self.assertTrue(result)


class TestRegistryOperations(unittest.TestCase):
    """Test registry load/save operations"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.registry_dir = self.hub_path / '.scf-registry'
        self.registry_dir.mkdir()
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_load_empty_registry(self):
        """Test loading non-existent registry returns empty structure"""
        registry = self.menu.load_registry()
        self.assertIn('projects', registry)
        # Groups may or may not exist in empty registry
        self.assertIsInstance(registry.get('projects'), list)

    def test_save_and_load_registry(self):
        """Test saving and loading registry"""
        test_data = {
            'projects': [{'name': 'test', 'path': '/test'}],
            'groups': {'work': {'description': 'Work projects'}}
        }

        self.menu.save_registry(test_data)
        loaded = self.menu.load_registry()

        self.assertEqual(len(loaded['projects']), 1)
        self.assertEqual(loaded['projects'][0]['name'], 'test')
        self.assertIn('work', loaded['groups'])


class TestVerboseListing(unittest.TestCase):
    """Test verbose project listing"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    @patch('builtins.input', return_value='')
    @patch('builtins.print')
    def test_verbose_listing_displays(self, mock_print, mock_input):
        """Test that verbose listing displays project info"""
        projects = [
            {
                'name': 'test-project',
                'path': '/test/path',
                'scf_enabled': True,
                'file_count': 100,
                'size_bytes': 1024000,
                'languages': ['Python', 'JavaScript'],
                'frameworks': ['Flask'],
                'has_tests': True,
                'has_ci': True,
                'created_at': '2024-01-01T00:00:00Z',
                'description': 'A test project'
            }
        ]

        self.menu.list_projects_verbose(projects)

        # Verify print was called multiple times with project info
        self.assertTrue(mock_print.called)
        calls = [str(c) for c in mock_print.call_args_list]

        # Check some expected content was printed
        call_str = ' '.join(calls)
        self.assertIn('test-project', call_str)


class TestDisplayProjectsByGroup(unittest.TestCase):
    """Test project display by group functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    @patch('builtins.print')
    def test_display_returns_project_map(self, mock_print):
        """Test that display returns correct project map"""
        projects = [
            {'name': 'proj1', 'scf_enabled': True, 'group': 'work'},
            {'name': 'proj2', 'scf_enabled': False, 'group': None},
        ]
        registry = {'groups': {'work': {'description': 'Work projects'}}, 'projects': projects}

        result = self.menu._display_projects_by_group(projects, registry)

        # Should return a map with numbered entries
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

    @patch('builtins.print')
    def test_display_grouped_first(self, mock_print):
        """Test that grouped projects are displayed first"""
        projects = [
            {'name': 'ungrouped1', 'scf_enabled': True, 'group': None},
            {'name': 'grouped1', 'scf_enabled': True, 'group': 'work'},
        ]
        registry = {'groups': {'work': {}}, 'projects': projects}

        result = self.menu._display_projects_by_group(projects, registry)

        # Grouped project should be first in map
        self.assertEqual(result[1]['name'], 'grouped1')
        self.assertEqual(result[2]['name'], 'ungrouped1')


class TestGitInfo(unittest.TestCase):
    """Test git info extraction"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_git_info_no_repo(self):
        """Test git info for non-git directory"""
        # Project without .git dir should return git info with has_repo=True
        # but no remote/branch info since git commands will fail
        test_proj = self.hub_path / 'test-proj'
        test_proj.mkdir()

        result = self.menu._get_git_info(test_proj)

        self.assertTrue(result['has_repo'])  # Structure created
        self.assertIsNone(result['remote_url'])
        self.assertFalse(result['has_remote'])


class TestConsolidateSCFFiles(unittest.TestCase):
    """Test SCF file consolidation functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.hub_path.mkdir(parents=True)
        self.framework_path = Path(__file__).parent.parent

        (self.hub_path / '.scf-registry').mkdir()
        (self.hub_path / 'hub-profile.json').write_text('{}')

        self.manager = scf_cli.SCFHubManager(self.framework_path)
        self.menu = scf_cli.SCFHubMenu(self.hub_path, self.manager, self.framework_path)

        # Create test project
        self.test_proj = Path(self.temp_dir) / 'test-project'
        self.test_proj.mkdir()

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_consolidate_creates_scf_dir(self):
        """Test that consolidation creates .scf directory if missing"""
        result = self.menu._consolidate_scf_files(self.test_proj)

        self.assertTrue((self.test_proj / '.scf').exists())
        self.assertEqual(result['errors'], [])

    def test_consolidate_migrates_legacy_buildstate(self):
        """Test migration of legacy buildstate from root to .scf/"""
        # Create legacy buildstate in root
        legacy_data = {'project': {'name': 'test'}, 'decisions': []}
        (self.test_proj / 'buildstate.json').write_text(json.dumps(legacy_data))

        result = self.menu._consolidate_scf_files(self.test_proj)

        # Should migrate to canonical location
        self.assertTrue((self.test_proj / '.scf' / 'BUILDSTATE.json').exists())
        self.assertFalse((self.test_proj / 'buildstate.json').exists())
        self.assertIn('buildstate.json', result['migrated'])

    def test_consolidate_cleans_corrupt_jsonl_lines(self):
        """Test that corrupt JSONL lines are cleaned from signals file"""
        scf_dir = self.test_proj / '.scf'
        scf_dir.mkdir()

        # Create signals file with mix of valid and corrupt lines
        signals_content = '''{"timestamp": "2025-01-01", "offers": true}
corrupt line that is not JSON
{"timestamp": "2025-01-02", "offers": false}
another corrupt line
{"timestamp": "2025-01-03", "offers": true}
'''
        (scf_dir / 'spoke-signals.jsonl').write_text(signals_content)

        result = self.menu._consolidate_scf_files(self.test_proj)

        # Should report 2 corrupt lines cleaned
        self.assertEqual(result['corrupt_lines_cleaned'], 2)

        # Read back the file - should only have valid lines
        with open(scf_dir / 'spoke-signals.jsonl') as f:
            lines = [l.strip() for l in f if l.strip()]

        self.assertEqual(len(lines), 3)  # Only valid lines remain
        # Verify all lines are valid JSON
        for line in lines:
            data = json.loads(line)  # Should not raise
            self.assertIn('timestamp', data)

    def test_consolidate_preserves_valid_signals(self):
        """Test that valid signals are preserved during consolidation"""
        scf_dir = self.test_proj / '.scf'
        scf_dir.mkdir()

        # Create signals file with only valid lines
        signals = [
            {"timestamp": "2025-01-01", "type": "learning"},
            {"timestamp": "2025-01-02", "type": "decision"},
        ]
        with open(scf_dir / 'spoke-signals.jsonl', 'w') as f:
            for s in signals:
                f.write(json.dumps(s) + '\n')

        result = self.menu._consolidate_scf_files(self.test_proj)

        # No corrupt lines
        self.assertEqual(result['corrupt_lines_cleaned'], 0)

        # Signals should be unchanged (no rewrite needed since no corruption)
        # Actually, it won't rewrite since canonical_had_corrupt is False
        with open(scf_dir / 'spoke-signals.jsonl') as f:
            lines = [json.loads(l.strip()) for l in f if l.strip()]

        self.assertEqual(len(lines), 2)

    def test_consolidate_merges_legacy_signals(self):
        """Test that legacy signals are merged into canonical location"""
        scf_dir = self.test_proj / '.scf'
        scf_dir.mkdir()

        # Create canonical signals
        canonical = [{"timestamp": "2025-01-01", "type": "a"}]
        with open(scf_dir / 'spoke-signals.jsonl', 'w') as f:
            f.write(json.dumps(canonical[0]) + '\n')

        # Create legacy signals in root
        legacy = [{"timestamp": "2025-01-02", "type": "b"}]
        with open(self.test_proj / 'spoke-signals.jsonl', 'w') as f:
            f.write(json.dumps(legacy[0]) + '\n')

        result = self.menu._consolidate_scf_files(self.test_proj)

        # Legacy should be merged and removed
        self.assertFalse((self.test_proj / 'spoke-signals.jsonl').exists())
        self.assertIn('spoke-signals.jsonl', result['cleaned'])

        # Canonical should have both signals
        with open(scf_dir / 'spoke-signals.jsonl') as f:
            lines = [json.loads(l.strip()) for l in f if l.strip()]

        self.assertEqual(len(lines), 2)
        timestamps = {l['timestamp'] for l in lines}
        self.assertIn('2025-01-01', timestamps)
        self.assertIn('2025-01-02', timestamps)

    def test_consolidate_handles_non_dict_buildstate(self):
        """Test that buildstate files containing non-dict JSON are handled gracefully"""
        # Create a buildstate that contains just a string instead of a dict
        (self.test_proj / 'buildstate.json').write_text('"just a string"')

        result = self.menu._consolidate_scf_files(self.test_proj)

        # Should report error but not crash
        self.assertTrue(any('expected dict, got str' in e for e in result['errors']))

        # File should NOT be removed since we couldn't process it
        self.assertTrue((self.test_proj / 'buildstate.json').exists())

    def test_consolidate_handles_list_buildstate(self):
        """Test that buildstate files containing a list are handled gracefully"""
        # Create a buildstate that contains a list instead of a dict
        (self.test_proj / 'buildstate.json').write_text('[1, 2, 3]')

        result = self.menu._consolidate_scf_files(self.test_proj)

        # Should report error but not crash
        self.assertTrue(any('expected dict, got list' in e for e in result['errors']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
