"""
Unit tests for state module.
"""
import unittest
from claudius.models.state import AppState, reducer, ActionType
from claudius.utils.calculations import get_all_descendants, get_visible_items

class TestState(unittest.TestCase):
    """Test case for state module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.edges = {
            "": ["folder1", "folder2", "file1.txt"],
            "folder1": ["folder1/file1.txt", "folder1/file2.txt"],
            "folder2": ["folder2/file1.txt"]
        }
        
        self.folders = {"folder1", "folder2"}
        
        self.state = AppState(
            included_paths=set(),
            edges=self.edges,
            folders=self.folders,
            selected_item="folder1",
            expanded_folders=set()
        )
    
    def test_toggle_include_file(self):
        """Test toggling include state for a file."""
        action = {
            "type": ActionType.TOGGLE_INCLUDE,
            "path": "file1.txt"
        }
        
        new_state = reducer(self.state, action)
        self.assertIn("file1.txt", new_state.included_paths)
        
        # Toggle again to remove
        new_state = reducer(new_state, action)
        self.assertNotIn("file1.txt", new_state.included_paths)
    
    def test_toggle_include_folder(self):
        """Test toggling include state for a folder."""
        # Patch get_all_descendants to use in the test
        # (In a real environment this would be imported correctly)
        def mock_get_descendants(edges, node):
            if node == "folder1":
                return {"folder1/file1.txt", "folder1/file2.txt"}
            return set()
            
        # Save original function and replace with mock
        original_func = get_all_descendants
        # This is a trick for testing - in real code you'd use a proper mocking framework
        globals()['get_all_descendants'] = mock_get_descendants
        
        try:
            action = {
                "type": ActionType.TOGGLE_INCLUDE,
                "path": "folder1"
            }
            
            new_state = reducer(self.state, action)
            self.assertIn("folder1", new_state.included_paths)
            self.assertIn("folder1/file1.txt", new_state.included_paths)
            self.assertIn("folder1/file2.txt", new_state.included_paths)
            
            # Toggle again to remove
            new_state = reducer(new_state, action)
            self.assertNotIn("folder1", new_state.included_paths)
            self.assertNotIn("folder1/file1.txt", new_state.included_paths)
            self.assertNotIn("folder1/file2.txt", new_state.included_paths)
        finally:
            # Restore original function
            globals()['get_all_descendants'] = original_func
    
    def test_toggle_expand(self):
        """Test toggling folder expansion."""
        action = {
            "type": ActionType.TOGGLE_EXPAND,
            "path": "folder1"
        }
        
        # Expand folder
        new_state = reducer(self.state, action)
        self.assertIn("folder1", new_state.expanded_folders)
        
        # Collapse folder
        new_state = reducer(new_state, action)
        self.assertNotIn("folder1", new_state.expanded_folders)
    
    def test_expand_all(self):
        """Test expanding all folders."""
        action = {
            "type": ActionType.EXPAND_ALL
        }
        
        new_state = reducer(self.state, action)
        self.assertEqual(new_state.expanded_folders, self.folders)
    
    def test_collapse_all(self):
        """Test collapsing all folders."""
        # First expand all
        state_expanded = AppState(
            included_paths=self.state.included_paths,
            edges=self.state.edges,
            folders=self.state.folders,
            selected_item=self.state.selected_item,
            expanded_folders=self.folders.copy()
        )
        
        action = {
            "type": ActionType.COLLAPSE_ALL
        }
        
        new_state = reducer(state_expanded, action)
        self.assertEqual(len(new_state.expanded_folders), 0)
    
    def test_set_notification(self):
        """Test setting a notification."""
        action = {
            "type": ActionType.SET_NOTIFICATION,
            "message": "Test notification"
        }
        
        new_state = reducer(self.state, action)
        self.assertEqual(new_state.notification, "Test notification")
    
    def test_clear_notification(self):
        """Test clearing a notification."""
        # First set a notification
        state_with_notification = AppState(
            included_paths=self.state.included_paths,
            edges=self.state.edges,
            folders=self.state.folders,
            selected_item=self.state.selected_item,
            expanded_folders=self.state.expanded_folders,
            notification="Test notification"
        )
        
        action = {
            "type": ActionType.CLEAR_NOTIFICATION
        }
        
        new_state = reducer(state_with_notification, action)
        self.assertIsNone(new_state.notification)

if __name__ == "__main__":
    unittest.main()
