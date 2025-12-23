#!/usr/bin/env python3
"""
Unit tests for update_scf.py functionality
Tests indentation fix and spoke project update scenarios
"""

import unittest
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import update_scf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from update_scf import SCFProjectUpdater


class TestUpdateSCF(unittest.TestCase):
    """Test SCF project update functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_project_path = Path(self.temp_dir) / "test-project"
        self.test_project_path.mkdir()
        
        # Create mock buildstate files
        self.buildstate_json = self.test_project_path / "buildstate.json"
        self.buildstate_md = self.test_project_path / "buildstate.md"
        
        # Create valid buildstate.json
        self.buildstate_json.write_text(json.dumps({
            "_scf_metadata": {
                "template_version": "v2.0",
                "hub_path": "~/projects/session-continuity-framework"
            },
            "project": {
                "name": "test-project",
                "version": "1.0.0"
            },
            "features": [],
            "decisions": []
        }, indent=2))
        
        # Create buildstate.md
        self.buildstate_md.write_text("# Test Project\n\nTest project buildstate")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_syntax_validation(self):
        """Test that update_scf.py has valid Python syntax"""
        updater = SCFProjectUpdater(dry_run=True)
        # If we can instantiate the class, the indentation is fixed
        self.assertIsInstance(updater, SCFProjectUpdater)
    
    def test_update_project_method_exists(self):
        """Test that update_project method is properly defined"""
        updater = SCFProjectUpdater(dry_run=True)
        self.assertTrue(hasattr(updater, 'update_project'))
        self.assertTrue(callable(getattr(updater, 'update_project')))
    
    def test_project_validation_success(self):
        """Test successful project validation"""
        updater = SCFProjectUpdater(dry_run=True)
        result = updater._validate_project(self.test_project_path)
        self.assertTrue(result)
    
    def test_project_validation_missing_directory(self):
        """Test project validation with missing directory"""
        updater = SCFProjectUpdater(dry_run=True)
        missing_path = Path(self.temp_dir) / "nonexistent"
        
        with patch('builtins.print'):  # Suppress print output
            result = updater._validate_project(missing_path)
        
        self.assertFalse(result)
    
    def test_project_validation_missing_buildstate_files(self):
        """Test project validation with missing buildstate files"""
        updater = SCFProjectUpdater(dry_run=True)
        
        # Remove buildstate files
        self.buildstate_json.unlink()
        self.buildstate_md.unlink()
        
        with patch('builtins.print'):  # Suppress print output
            result = updater._validate_project(self.test_project_path)
        
        self.assertFalse(result)
    
    def test_dry_run_mode(self):
        """Test that dry run mode is properly set"""
        updater = SCFProjectUpdater(dry_run=True)
        self.assertTrue(updater.dry_run)
        
        updater = SCFProjectUpdater(dry_run=False)
        self.assertFalse(updater.dry_run)
    
    @patch('update_scf.SCFProjectUpdater._validate_project')
    @patch('update_scf.SCFProjectUpdater._rebalance_content')
    @patch('update_scf.SCFProjectUpdater._update_agents_compatibility')
    @patch('update_scf.SCFProjectUpdater._sync_inheritance')
    @patch('update_scf.SCFProjectUpdater._update_llm_integration')
    @patch('builtins.print')
    def test_update_project_workflow_success(self, mock_print, mock_llm, mock_inherit, 
                                           mock_agents, mock_rebalance, mock_validate):
        """Test successful update project workflow"""
        # Mock all validation and update steps to succeed
        mock_validate.return_value = True
        mock_rebalance.return_value = True
        mock_agents.return_value = True
        mock_inherit.return_value = True
        mock_llm.return_value = True
        
        updater = SCFProjectUpdater(dry_run=True)
        result = updater.update_project(self.test_project_path)
        
        self.assertTrue(result)
        mock_validate.assert_called_once_with(self.test_project_path)
        mock_rebalance.assert_called_once()
        mock_agents.assert_called_once()
        mock_inherit.assert_called_once()
        mock_llm.assert_called_once()
    
    @patch('update_scf.SCFProjectUpdater._validate_project')
    @patch('builtins.print')
    def test_update_project_validation_failure(self, mock_print, mock_validate):
        """Test update project with validation failure"""
        mock_validate.return_value = False
        
        updater = SCFProjectUpdater(dry_run=True)
        result = updater.update_project(self.test_project_path)
        
        self.assertFalse(result)
        mock_validate.assert_called_once_with(self.test_project_path)
    
    def test_changes_tracking(self):
        """Test that changes are properly tracked"""
        updater = SCFProjectUpdater(dry_run=True)
        self.assertEqual(len(updater.changes_made), 0)
        
        updater.changes_made.append("Test change")
        self.assertEqual(len(updater.changes_made), 1)
        self.assertEqual(updater.changes_made[0], "Test change")
    
    def test_templates_directory_path(self):
        """Test that templates directory path is correctly set"""
        updater = SCFProjectUpdater(dry_run=True)
        expected_path = Path(__file__).parent.parent / "templates"
        self.assertEqual(updater.templates_dir.name, "templates")
    
    @patch('builtins.print')
    def test_skip_rebalance_option(self, mock_print):
        """Test skip rebalance option"""
        with patch.object(SCFProjectUpdater, '_validate_project', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_agents_compatibility', return_value=True), \
             patch.object(SCFProjectUpdater, '_sync_inheritance', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_llm_integration', return_value=True):
            
            updater = SCFProjectUpdater(dry_run=True)
            result = updater.update_project(self.test_project_path, skip_rebalance=True)
            self.assertTrue(result)
    
    @patch('builtins.print')
    def test_force_rebalance_option(self, mock_print):
        """Test force rebalance option"""
        with patch.object(SCFProjectUpdater, '_validate_project', return_value=True), \
             patch.object(SCFProjectUpdater, '_rebalance_content', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_agents_compatibility', return_value=True), \
             patch.object(SCFProjectUpdater, '_sync_inheritance', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_llm_integration', return_value=True):
            
            updater = SCFProjectUpdater(dry_run=True)
            result = updater.update_project(self.test_project_path, force_rebalance=True)
            self.assertTrue(result)


class TestUpdateSCFIntegration(unittest.TestCase):
    """Integration tests for update_scf.py with real spoke projects"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.spoke_project = Path(self.temp_dir) / "condoshield-crm"
        self.spoke_project.mkdir()
        
        # Create realistic spoke buildstate.json
        buildstate_content = {
            "_scf_metadata": {
                "template_version": "v2.1",
                "source_repo": "https://github.com/mariov96/session-continuity-framework",
                "hub_path": "/home/mario/projects/session-continuity-framework",
                "last_sync_date": "2025-12-13T00:00:00Z"
            },
            "_session_state": {
                "last_modified_by": "claude-sonnet-4.5",
                "last_modified_at": "2025-12-13T10:30:00Z",
                "session_count": 15
            },
            "project": {
                "name": "condoshield-crm",
                "version": "1.0.0",
                "type": "web_application",
                "description": "CRM system for condo management"
            },
            "stack": ["React", "Node.js", "PostgreSQL"],
            "features": [
                {
                    "id": "user-auth",
                    "name": "User Authentication",
                    "status": "✅",
                    "priority": "high"
                }
            ],
            "decisions": [
                {
                    "date": "2025-12-13",
                    "desc": "Chose PostgreSQL for data persistence",
                    "impact": 7
                }
            ],
            "next_steps": [
                "Implement user dashboard",
                "Add property management features"
            ]
        }
        
        buildstate_json = self.spoke_project / "buildstate.json"
        buildstate_json.write_text(json.dumps(buildstate_content, indent=2))
        
        # Create buildstate.md
        buildstate_md = self.spoke_project / "buildstate.md"
        buildstate_md.write_text("""# CondoShield CRM

## Overview
CRM system for condo management with property tracking and resident communication.

## Current Status
- User authentication implemented
- Database schema designed
- Frontend scaffolding complete

## Next Steps
- Implement user dashboard
- Add property management features
""")
    
    def tearDown(self):
        """Clean up integration test environment"""
        shutil.rmtree(self.temp_dir)
    
    @patch('builtins.print')
    def test_preserve_existing_data_during_update(self, mock_print):
        """Test that existing buildstate data is preserved during updates"""
        # Read original data
        original_buildstate = json.loads((self.spoke_project / "buildstate.json").read_text())
        original_features = original_buildstate["features"][0]
        original_decisions = original_buildstate["decisions"][0]
        
        # Mock the update methods to avoid file system operations
        with patch.object(SCFProjectUpdater, '_rebalance_content', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_agents_compatibility', return_value=True), \
             patch.object(SCFProjectUpdater, '_sync_inheritance', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_llm_integration', return_value=True):
            
            updater = SCFProjectUpdater(dry_run=True)
            result = updater.update_project(self.spoke_project)
        
        # Verify data preservation (in dry run, files shouldn't actually change)
        updated_buildstate = json.loads((self.spoke_project / "buildstate.json").read_text())
        
        # Key data should be preserved
        self.assertEqual(updated_buildstate["project"]["name"], "condoshield-crm")
        self.assertEqual(updated_buildstate["features"][0]["name"], "User Authentication")
        self.assertEqual(updated_buildstate["decisions"][0]["desc"], "Chose PostgreSQL for data persistence")
        self.assertTrue(result)
    
    @patch('builtins.print')
    def test_session_state_preservation(self, mock_print):
        """Test that session state is preserved during updates"""
        original_buildstate = json.loads((self.spoke_project / "buildstate.json").read_text())
        original_session_count = original_buildstate["_session_state"]["session_count"]
        
        with patch.object(SCFProjectUpdater, '_rebalance_content', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_agents_compatibility', return_value=True), \
             patch.object(SCFProjectUpdater, '_sync_inheritance', return_value=True), \
             patch.object(SCFProjectUpdater, '_update_llm_integration', return_value=True):
            
            updater = SCFProjectUpdater(dry_run=True)
            result = updater.update_project(self.spoke_project)
        
        # Session count should be preserved
        updated_buildstate = json.loads((self.spoke_project / "buildstate.json").read_text())
        self.assertEqual(updated_buildstate["_session_state"]["session_count"], original_session_count)
        self.assertTrue(result)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)