"""
Persistence module for Claudius.
Handles saving and loading application state.
"""
import os
import json
import platform
from pathlib import Path
from typing import Dict, Set, Optional, Union, Any


def get_state_file_path(local_mode: bool = False) -> Path:
    """
    Get the path to the state file.

    Args:
        local_mode: If True, use local directory instead of user config dir

    Returns:
        Path to the state file
    """
    if local_mode:
        # When running locally, store state in the current directory
        return Path('.claudius_state.json')

    # Otherwise, use the appropriate config directory for the OS
    if platform.system() == 'Windows':
        config_dir = Path(os.path.expandvars('%APPDATA%')) / 'Claudius'
    else:  # Linux, MacOS, etc.
        config_dir = Path.home() / '.config' / 'claudius'

    # Ensure directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir / 'state.json'


def save_state(expanded_folders: Set[str], selected_item: Optional[str], local_mode: bool = None) -> bool:
    """
    Save application state to disk.

    Args:
        expanded_folders: Set of expanded folder paths
        selected_item: Currently selected item path
        local_mode: If True, save to local directory. If None, auto-detect.

    Returns:
        True if successful, False otherwise
    """
    if local_mode is None:
        local_mode = get_local_mode()
    state_path = get_state_file_path(local_mode)

    # Convert to serializable format
    state_data = {
        'expanded_folders': list(expanded_folders),
        'selected_item': selected_item
    }

    try:
        with open(state_path, 'w') as f:
            json.dump(state_data, f)
        return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False


def is_package_installed() -> bool:
    """
    Check if Claudius is installed as a proper package.

    Returns:
        True if properly installed, False if running locally
    """
    try:
        import importlib.metadata
        # Try to get metadata for the package
        importlib.metadata.metadata('claudius')
        return True
    except (ImportError, importlib.metadata.PackageNotFoundError):
        return False


def get_local_mode() -> bool:
    """
    Determine whether to use local mode based on how Claudius is being run.

    Returns:
        True if running locally, False if installed as a package
    """
    return not is_package_installed()


def load_state(local_mode: bool = None) -> Dict[str, Any]:
    """
    Load application state from disk.

    Args:
        local_mode: If True, load from local directory. If None, auto-detect.

    Returns:
        Dictionary with loaded state or empty values if file doesn't exist
    """
    if local_mode is None:
        local_mode = get_local_mode()
    state_path = get_state_file_path(local_mode)

    # Default state if file doesn't exist
    default_state = {
        'expanded_folders': set(),
        'selected_item': None
    }

    if not state_path.exists():
        return default_state

    try:
        with open(state_path, 'r') as f:
            state_data = json.load(f)

        # Convert lists back to sets
        return {
            'expanded_folders': set(state_data.get('expanded_folders', [])),
            'selected_item': state_data.get('selected_item')
        }
    except Exception as e:
        print(f"Error loading state: {e}")
        return default_statee
