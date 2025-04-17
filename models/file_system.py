"""
File system operations for Claudius.
These functions handle reading/writing files and scanning the filesystem.
"""
import os
from typing import Set, Dict, List, Tuple

def scan_filesystem(root_dir: str) -> Tuple[Dict[str, List[str]], Set[str]]:
    """
    Scan filesystem and return edges and folders.
    
    Args:
        root_dir: Root directory to scan
        
    Returns:
        Tuple containing:
        - edges: Dict mapping parent paths to lists of child paths
        - folders: Set of paths that are folders
    """
    edges = {"": []}  # Start with empty root
    folders = set()
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel_dirpath = os.path.relpath(dirpath, root_dir)
        if rel_dirpath == '.':
            rel_dirpath = ''
        
        # Add this directory to folders set (except root)
        if rel_dirpath:
            folders.add(rel_dirpath)
        
        # Create edges for subdirectories
        parent = rel_dirpath
        children = []
        
        for dirname in sorted(dirnames):
            child_path = os.path.join(rel_dirpath, dirname).replace('\\', '/')
            children.append(child_path)
        
        # Create edges for files
        for filename in sorted(filenames):
            # Skip .claudeignore itself
            if filename == '.claudeignore' and rel_dirpath == '':
                continue
                
            child_path = os.path.join(rel_dirpath, filename).replace('\\', '/')
            children.append(child_path)
        
        edges[parent] = children
    
    return edges, folders

def read_claudeignore(root_dir: str) -> Set[str]:
    """
    Read .claudeignore file and return set of included paths.
    
    Args:
        root_dir: Root directory containing .claudeignore
        
    Returns:
        Set of included paths
    """
    ignore_path = os.path.join(root_dir, '.claudeignore')
    included = set()
    
    if os.path.exists(ignore_path):
        try:
            with open(ignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Convert absolute paths to relative if needed
                        if os.path.isabs(line) and line.startswith(root_dir):
                            line = os.path.relpath(line, root_dir).replace('\\', '/')
                        included.add(line)
        except Exception as e:
            print(f"Error reading .claudeignore: {e}")
    
    return included

def write_claudeignore(root_dir: str, included_paths: Set[str]) -> bool:
    """
    Write included paths to .claudeignore file.
    
    Args:
        root_dir: Root directory for .claudeignore
        included_paths: Set of paths to include
        
    Returns:
        bool: True if successful, False otherwise
    """
    ignore_path = os.path.join(root_dir, '.claudeignore')
    
    try:
        with open(ignore_path, 'w') as f:
            for path in sorted(included_paths):
                # Ensure path uses forward slashes
                path = path.replace('\\', '/')
                f.write(f"{path}\n")
        return True
    except Exception as e:
        print(f"Error writing .claudeignore: {e}")
        return False
