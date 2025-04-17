"""
Unit tests for calculations module.
"""
import unittest
import os
from claudius.utils.calculations import (
    get_visible_items, get_root_items, get_display_name, 
    get_all_descendants, get_indentation_level, get_absolute_paths
)
from claudius.models.state import AppState

class TestCalculations(unittest.TestCase):
    """Test case for calculations module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.edges = {
            "": ["folder1", "folder2", "file1.txt"],
            "folder1": ["folder1/file1.txt", "folder1/file2.txt"],
            "folder2": ["folder2/file1.txt"]
        }
        
        self.folders = {"folder1", "folder2"}
        
        self.state = AppState(
            included_paths={"folder1", "folder1/file1.txt"},
            edges=self.edges,
            folders=self.folders,
            selected_item="folder1",
            expanded_folders={"folder1"}
        )
    
    def test_get_root_items(self):
        """Test get_root_items function."""
        expected = [""]
        result = get_root_items(self.edges)
        self.assertEqual(result, expected)
    
    def test_get_display_name(self):
        """Test get_display_name function."""
        self.assertEqual(get_display_name(""), ".")
        self.assertEqual(get_display_name("folder1"), "folder1")
        self.assertEqual(get_display_name("folder1/file1.txt"), "file1.txt")
    
    def test_get_all_descendants(self):
        """Test get_all_descendants function."""
        expected = {"folder1/file1.txt", "folder1/file2.txt"}
        result = get_all_descendants(self.edges, "folder1")
        self.assertEqual(result, expected)
    
    def test_get_indentation_level(self):
        """Test get_indentation_level function."""
        self.assertEqual(get_indentation_level(""), 0)
        self.assertEqual(get_indentation_level("folder1"), 1)
        self.assertEqual(get_indentation_level("folder1/file1.txt"), 2)
    
    def test_get_absolute_paths(self):
        """Test get_absolute_paths function."""
        root_dir = "/tmp/test"
        included_paths = {"folder1/file1.txt", "file2.txt"}
        expected = [
            os.path.join(root_dir, "file2.txt").replace('\\', '/'),
            os.path.join(root_dir, "folder1/file1.txt").replace('\\', '/')
        ]
        result = get_absolute_paths(included_paths, root_dir)
        self.assertEqual(sorted(result), sorted(expected))
    
    def test_get_visible_items(self):
        """Test get_visible_items function."""
        # With folder1 expanded, we should see root items + folder1's children
        expected = ["", "folder1", "folder1/file1.txt", "folder1/file2.txt", "folder2", "file1.txt"]
        result = get_visible_items(self.state)
        self.assertEqual(sorted(result), sorted(expected))
        
        # With no folders expanded, we should only see root items
        state_collapsed = AppState(
            included_paths=self.state.included_paths,
            edges=self.state.edges,
            folders=self.state.folders,
            selected_item=self.state.selected_item,
            expanded_folders=set()
        )
        expected = ["", "folder1", "folder2", "file1.txt"]
        result = get_visible_items(state_collapsed)
        self.assertEqual(sorted(result), sorted(expected))

if __name__ == "__main__":
    unittest.main()
