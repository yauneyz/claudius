"""
Unit tests for file_system module.
"""
import unittest
import os
import tempfile
import shutil
from claudius.models.file_system import scan_filesystem, read_claudeignore, write_claudeignore

class TestFileSystem(unittest.TestCase):
    """Test case for file_system module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a simple directory structure
        os.makedirs(os.path.join(self.test_dir, "folder1"))
        os.makedirs(os.path.join(self.test_dir, "folder2"))
        
        # Create some files
        open(os.path.join(self.test_dir, "file1.txt"), "w").close()
        open(os.path.join(self.test_dir, "folder1", "file1.txt"), "w").close()
        open(os.path.join(self.test_dir, "folder1", "file2.txt"), "w").close()
        open(os.path.join(self.test_dir, "folder2", "file1.txt"), "w").close()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_scan_filesystem(self):
        """Test scanning the filesystem."""
        edges, folders = scan_filesystem(self.test_dir)
        
        # Check edges
        self.assertIn("", edges)
        self.assertIn("folder1", edges.get("", []))
        self.assertIn("folder2", edges.get("", []))
        self.assertIn("file1.txt", edges.get("", []))
        
        # Check folders
        self.assertIn("folder1", folders)
        self.assertIn("folder2", folders)
    
    def test_read_claudeignore(self):
        """Test reading .claudeignore file."""
        # Create a .claudeignore file
        with open(os.path.join(self.test_dir, ".claudeignore"), "w") as f:
            f.write("folder1\n")
            f.write("file1.txt\n")
        
        included = read_claudeignore(self.test_dir)
        
        self.assertIn("folder1", included)
        self.assertIn("file1.txt", included)
    
    def test_write_claudeignore(self):
        """Test writing .claudeignore file."""
        included = {"folder1", "file1.txt"}
        
        success = write_claudeignore(self.test_dir, included)
        self.assertTrue(success)
        
        # Check the file was written correctly
        with open(os.path.join(self.test_dir, ".claudeignore"), "r") as f:
            lines = [line.strip() for line in f.readlines()]
        
        self.assertIn("folder1", lines)
        self.assertIn("file1.txt", lines)
    
    def test_read_claudeignore_nonexistent(self):
        """Test reading a non-existent .claudeignore file."""
        # Make sure file doesn't exist
        ignore_path = os.path.join(self.test_dir, ".claudeignore")
        if os.path.exists(ignore_path):
            os.remove(ignore_path)
            
        included = read_claudeignore(self.test_dir)
        self.assertEqual(len(included), 0)

if __name__ == "__main__":
    unittest.main()
