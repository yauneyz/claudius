"""
Pure functions for Claudius.
These functions perform calculations without side effects.
"""
from typing import Dict, List, Set, Optional
import os
from ..models.state import AppState

def get_visible_items(state: AppState) -> List[str]:
    """
    Return a list of visible items based on expanded folders.
    
    Args:
        state: Current application state
        
    Returns:
        List of visible item paths
    """
    visible = []
    
    # Helper function to traverse the tree
    def traverse(node, is_visible=True):
        if is_visible:
            visible.append(node)
        
        # If this is a folder and it's either the root or it's expanded
        if not node or (node in state.folders and node in state.expanded_folders):
            for child in state.edges.get(node, []):
                traverse(child, is_visible)
    
    # Start with root items
    traverse("", True)
    
    return visible

def get_root_items(edges: Dict[str, List[str]]) -> List[str]:
    """
    Return items that don't have parents in the edge dictionary.
    
    Args:
        edges: Dictionary mapping parent paths to lists of child paths
        
    Returns:
        List of root item paths
    """
    all_children = set()
    for children in edges.values():
        all_children.update(children)
    
    all_items = set(edges.keys())
    for children in edges.values():
        all_items.update(children)
    
    return sorted(list(all_items - all_children))

def get_display_name(path: str) -> str:
    """
    Return the display name for a path (the filename without the parent paths).
    
    Args:
        path: File or folder path
        
    Returns:
        Display name for the path
    """
    if not path:
        return "."  # Root directory
    return os.path.basename(path)

def get_all_descendants(edges: Dict[str, List[str]], node: str) -> Set[str]:
    """
    Get all descendants of a node recursively.
    
    Args:
        edges: Dictionary mapping parent paths to lists of child paths
        node: Node to get descendants for
        
    Returns:
        Set of descendant paths
    """
    result = set()
    
    def collect_descendants(current_node):
        for child in edges.get(current_node, []):
            result.add(child)
            collect_descendants(child)
    
    collect_descendants(node)
    return result

def get_indentation_level(path: str) -> int:
    """
    Calculate indentation level based on path depth.
    
    Args:
        path: File or folder path
        
    Returns:
        Indentation level
    """
    if not path:
        return 0
    return len(path.split(os.sep))

def get_path_for_ignore(path: str, root_dir: str) -> str:
    """
    Convert a path to the format used in .claudeignore file.
    
    Args:
        path: File or folder path
        root_dir: Root directory
        
    Returns:
        Path formatted for .claudeignore
    """
    # Make sure we're using the correct path separator
    path = path.replace('\\', '/')
    
    # If it's already an absolute path, just return it
    if os.path.isabs(path):
        return path
    
    # Otherwise, make it relative to root_dir
    return os.path.join(root_dir, path).replace('\\', '/')

def get_absolute_paths(included_paths: Set[str], root_dir: str) -> List[str]:
    """
    Convert relative paths to absolute paths for writing to .claudeignore.
    
    Args:
        included_paths: Set of included paths
        root_dir: Root directory
        
    Returns:
        List of absolute paths
    """
    return [get_path_for_ignore(path, root_dir) for path in sorted(included_paths)]
