#!/usr/bin/env python3
"""
Unit tests for SCF CLI functionality

Tests the unified CLI including hub management and guided init.
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

# Import the scf module (it's a script without .py extension)
import importlib.util
import importlib.machinery
scf_path = Path(__file__).parent.parent / 'scf'

# Load the module from file
spec = importlib.util.spec_from_loader(
    "scf_cli",
    importlib.machinery.SourceFileLoader("scf_cli", str(scf_path))
)
scf_cli = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(scf_cli)
except SystemExit:
    pass  # Module calls sys.exit on import sometimes


class TestSCFHubManager(unittest.TestCase):
    """Test SCF Hub Manager functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.hub_path = Path(self.temp_dir) / "test-hub"
        self.framework_path = Path(__file__).parent.parent

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_hub_manager_init(self):
        """Test SCFHubManager initialization"""
        manager = scf_cli.SCFHubManager(self.framework_path)
        self.assertEqual(manager.framework_path, self.framework_path)

    @patch('builtins.input', side_effect=['Test User', 'Python, Web', '2'])
    @patch('builtins.print')
    def test_create_hub_interactive(self, mock_print, mock_input):
        """Test interactive hub creation"""
        manager = scf_cli.SCFHubManager(self.framework_path)
        result = manager.create_hub(self.hub_path, interactive=True)

        self.assertTrue(result)
        self.assertTrue(self.hub_path.exists())
        self.assertTrue((self.hub_path / '.scf').exists())
        self.assertTrue((self.hub_path / '.scf-registry').exists())
        self.assertTrue((self.hub_path / 'hub-profile.json').exists())
        self.assertTrue((self.hub_path / 'learnings').exists())

    @patch('builtins.print')
    def test_create_hub_non_interactive(self, mock_print):
        """Test non-interactive hub creation"""
        manager = scf_cli.SCFHubManager(self.framework_path)
        result = manager.create_hub(self.hub_path, interactive=False)

        self.assertTrue(result)
        self.assertTrue(self.hub_path.exists())

        # Check hub-profile.json was created
        profile_path = self.hub_path / 'hub-profile.json'
        self.assertTrue(profile_path.exists())

        with open(profile_path) as f:
            profile = json.load(f)

        self.assertIn('user', profile)
        self.assertIn('hub_config', profile)

    @patch('builtins.print')
    def test_hub_buildstate_created(self, mock_print):
        """Test that hub creates its own buildstate"""
        manager = scf_cli.SCFHubManager(self.framework_path)
        manager.create_hub(self.hub_path, interactive=False)

        buildstate_path = self.hub_path / '.scf' / 'BUILDSTATE.json'
        self.assertTrue(buildstate_path.exists())

        with open(buildstate_path) as f:
            buildstate = json.load(f)

        self.assertTrue(buildstate['_scf_metadata']['is_hub'])
        self.assertTrue(buildstate['_project_foundation']['completed'])

    def test_find_hub_not_found(self):
        """Test find_hub when no hub exists"""
        result = scf_cli.SCFHubManager.find_hub()
        # This may or may not find a hub depending on the system
        # Just verify it returns Path or None
        self.assertTrue(result is None or isinstance(result, Path))


class TestSCFOnboarding(unittest.TestCase):
    """Test SCF Onboarding functionality"""

    def test_onboarding_init(self):
        """Test SCFOnboarding initialization"""
        onboarding = scf_cli.SCFOnboarding()
        self.assertIsInstance(onboarding, scf_cli.SCFOnboarding)

    @patch('builtins.print')
    def test_show_welcome(self, mock_print):
        """Test welcome message display"""
        onboarding = scf_cli.SCFOnboarding()
        onboarding.show_welcome()
        mock_print.assert_called()

    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_choose_role_hub(self, mock_print, mock_input):
        """Test role selection - hub"""
        onboarding = scf_cli.SCFOnboarding()
        result = onboarding.choose_role()
        self.assertEqual(result, 'hub')

    @patch('builtins.input', return_value='2')
    @patch('builtins.print')
    def test_choose_role_spoke(self, mock_print, mock_input):
        """Test role selection - spoke"""
        onboarding = scf_cli.SCFOnboarding()
        result = onboarding.choose_role()
        self.assertEqual(result, 'spoke')


class TestCreateParser(unittest.TestCase):
    """Test argument parser creation"""

    def test_parser_creation(self):
        """Test that parser is created successfully"""
        parser = scf_cli.create_parser()
        self.assertIsNotNone(parser)

    def test_parser_init_command(self):
        """Test init command parsing"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['init'])
        self.assertEqual(args.command, 'init')
        self.assertEqual(args.path, '.')

    def test_parser_init_guided(self):
        """Test init --guided parsing"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['init', '--guided'])
        self.assertEqual(args.command, 'init')
        self.assertTrue(args.guided)

    def test_parser_hub_create(self):
        """Test hub create command parsing"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['hub', 'create'])
        self.assertEqual(args.command, 'hub')
        self.assertEqual(args.action, 'create')

    def test_parser_hub_create_with_path(self):
        """Test hub create with custom path"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['hub', 'create', '/custom/path'])
        self.assertEqual(args.command, 'hub')
        self.assertEqual(args.action, 'create')
        self.assertEqual(args.path, '/custom/path')

    def test_parser_sync_command(self):
        """Test sync command parsing"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['sync'])
        self.assertEqual(args.command, 'sync')

    def test_parser_sync_status(self):
        """Test sync --status parsing"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['sync', '--status'])
        self.assertEqual(args.command, 'sync')
        self.assertTrue(args.status)

    def test_parser_projects_scan(self):
        """Test projects scan command"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['projects', 'scan'])
        self.assertEqual(args.command, 'projects')
        self.assertEqual(args.action, 'scan')


class TestSCFCommands(unittest.TestCase):
    """Test SCF command implementations"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_project = Path(self.temp_dir) / "test-project"
        self.test_project.mkdir()

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    @patch('builtins.print')
    def test_cmd_hub_locate_not_found(self, mock_print):
        """Test hub locate when no hub exists"""
        parser = scf_cli.create_parser()
        args = parser.parse_args(['hub', 'locate'])

        # Mock find_hub to return None
        with patch.object(scf_cli.SCFHubManager, 'find_hub', return_value=None):
            scf_cli.SCFCommands.cmd_hub(args)

        # Should print "No hub found"
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
