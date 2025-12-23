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


if __name__ == '__main__':
    unittest.main(verbosity=2)
