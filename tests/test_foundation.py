#!/usr/bin/env python3
"""
Unit tests for SCF Foundation System

Tests the project foundation checking, drift detection, and guided setup functionality.
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

from teach import check_foundation_status


class TestFoundationStatus(unittest.TestCase):
    """Test foundation status checking functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_project = Path(self.temp_dir) / "test-project"
        self.test_project.mkdir()
        self.scf_dir = self.test_project / '.scf'
        self.scf_dir.mkdir()

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)

    def test_no_buildstate_file(self):
        """Test when no buildstate file exists"""
        result = check_foundation_status(self.test_project)

        self.assertFalse(result['complete'])
        self.assertIn("No buildstate.json found", result['issues'])

    def test_invalid_json(self):
        """Test with invalid JSON in buildstate"""
        buildstate_path = self.scf_dir / 'BUILDSTATE.json'
        buildstate_path.write_text("{ invalid json }")

        result = check_foundation_status(self.test_project)

        self.assertFalse(result['complete'])
        self.assertIn("buildstate.json is not valid JSON", result['issues'])

    def test_no_foundation_section(self):
        """Test when _project_foundation section is missing"""
        buildstate = {
            "project": {"name": "test"},
            "_session_state": {}
        }
        buildstate_path = self.scf_dir / 'BUILDSTATE.json'
        buildstate_path.write_text(json.dumps(buildstate))

        result = check_foundation_status(self.test_project)

        self.assertFalse(result['complete'])
        self.assertIn("No _project_foundation section found", result['issues'])

    def test_incomplete_foundation(self):
        """Test when foundation exists but completed is False"""
        buildstate = {
            "_project_foundation": {
                "completed": False,
                "identity": {}
            }
        }
        buildstate_path = self.scf_dir / 'BUILDSTATE.json'
        buildstate_path.write_text(json.dumps(buildstate))

        result = check_foundation_status(self.test_project)

        self.assertFalse(result['complete'])
        self.assertIn("Project foundation not completed", result['issues'])

    def test_complete_foundation(self):
        """Test with complete foundation"""
        buildstate = {
            "_project_foundation": {
                "completed": True,
                "identity": {
                    "type": "code",
                    "name": "Test Project",
                    "one_liner": "A test project",
                    "success_looks_like": "All tests pass"
                },
                "boundaries": {
                    "in_scope": ["Testing"],
                    "out_of_scope": ["Production"]
                }
            },
            "_session_state": {
                "requires_review": False
            }
        }
        buildstate_path = self.scf_dir / 'BUILDSTATE.json'
        buildstate_path.write_text(json.dumps(buildstate))

        result = check_foundation_status(self.test_project)

        self.assertTrue(result['complete'])
        self.assertEqual(len(result['issues']), 0)

    def test_complete_with_missing_fields(self):
        """Test complete foundation but missing optional fields"""
        buildstate = {
            "_project_foundation": {
                "completed": True,
                "identity": {
                    "type": "code",
                    "name": "Test Project"
                    # Missing one_liner and success_looks_like
                },
                "boundaries": {}  # Missing in_scope
            }
        }
        buildstate_path = self.scf_dir / 'BUILDSTATE.json'
        buildstate_path.write_text(json.dumps(buildstate))

        result = check_foundation_status(self.test_project)

        self.assertTrue(result['complete'])
        self.assertIn("Missing project one-liner description", result['issues'])
        self.assertIn("Missing success definition", result['issues'])
        self.assertIn("No scope boundaries defined", result['issues'])

    def test_requires_review_flag(self):
        """Test detection of requires_review flag"""
        buildstate = {
            "_project_foundation": {
                "completed": True,
                "identity": {
                    "one_liner": "Test",
                    "success_looks_like": "Done"
                },
                "boundaries": {
                    "in_scope": ["Everything"]
                }
            },
            "_session_state": {
                "requires_review": True,
                "review_reason": "Major architecture change"
            }
        }
        buildstate_path = self.scf_dir / 'BUILDSTATE.json'
        buildstate_path.write_text(json.dumps(buildstate))

        result = check_foundation_status(self.test_project)

        self.assertTrue(result['complete'])
        self.assertIn("Review required: Major architecture change", result['issues'])

    def test_legacy_buildstate_location(self):
        """Test finding buildstate in legacy location (project root)"""
        # Remove .scf directory
        shutil.rmtree(self.scf_dir)

        # Create buildstate in project root
        buildstate = {
            "_project_foundation": {
                "completed": True,
                "identity": {
                    "one_liner": "Legacy project",
                    "success_looks_like": "Working"
                },
                "boundaries": {"in_scope": ["All"]}
            }
        }
        buildstate_path = self.test_project / 'buildstate.json'
        buildstate_path.write_text(json.dumps(buildstate))

        result = check_foundation_status(self.test_project)

        self.assertTrue(result['complete'])


class TestFoundationTemplates(unittest.TestCase):
    """Test foundation-ready templates"""

    def setUp(self):
        """Set up test environment"""
        self.templates_dir = Path(__file__).parent.parent / 'templates' / 'spoke'

    def test_spoke_template_has_foundation(self):
        """Test that spoke BUILDSTATE.json template includes foundation"""
        template_path = self.templates_dir / 'BUILDSTATE.json'

        if not template_path.exists():
            self.skipTest("Template not found")

        with open(template_path) as f:
            template = json.load(f)

        self.assertIn('_project_foundation', template)
        self.assertFalse(template['_project_foundation']['completed'])
        self.assertIn('identity', template['_project_foundation'])
        self.assertIn('boundaries', template['_project_foundation'])
        self.assertIn('philosophy', template['_project_foundation'])

    def test_preset_templates_exist(self):
        """Test that preset templates exist for different project types"""
        presets_dir = self.templates_dir / 'presets'

        if not presets_dir.exists():
            self.skipTest("Presets directory not found")

        expected_presets = ['research.json', 'writing.json', 'design.json']

        for preset in expected_presets:
            preset_path = presets_dir / preset
            self.assertTrue(preset_path.exists(), f"Missing preset: {preset}")

            with open(preset_path) as f:
                data = json.load(f)

            self.assertIn('_project_foundation', data)
            self.assertIn('ai_rules', data)


class TestHubTemplates(unittest.TestCase):
    """Test hub templates"""

    def setUp(self):
        """Set up test environment"""
        self.templates_dir = Path(__file__).parent.parent / 'templates' / 'hub'

    def test_hub_profile_template_exists(self):
        """Test that hub-profile.json template exists"""
        template_path = self.templates_dir / 'hub-profile.json'

        if not template_path.exists():
            self.skipTest("Hub template not found")

        with open(template_path) as f:
            template = json.load(f)

        self.assertIn('user', template)
        self.assertIn('work_style', template)
        self.assertIn('hub_config', template)
        self.assertIn('learning_philosophy', template)

    def test_spoke_projects_template_exists(self):
        """Test that spoke-projects.json template exists"""
        template_path = self.templates_dir / 'spoke-projects.json'

        if not template_path.exists():
            self.skipTest("Spoke projects template not found")

        with open(template_path) as f:
            template = json.load(f)

        self.assertIn('projects', template)
        self.assertEqual(template['projects'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
