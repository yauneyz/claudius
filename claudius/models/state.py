"""
State management for Claudius.
Uses immutable pattern with dataclasses for state management.
"""
from dataclasses import dataclass, replace as dataclass_replace
from typing import Set, Dict, Optional, List, Any


@dataclass(frozen=True)
class AppState:
    """Immutable app state."""
    included_paths: Set[str]  # Paths to include in .claudeignore
    edges: Dict[str, List[str]]  # Map of parent paths to child paths
    folders: Set[str]  # Set of paths that are folders
    selected_item: Optional[str]  # Currently selected item
    expanded_folders: Set[str]  # Set of expanded folders
    notification: Optional[str] = None  # Current notification message

    def update(self, **kwargs) -> 'AppState':
        """Create a new state with the specified updates."""
        return dataclass_replace(self, **kwargs)


def get_initial_state() -> AppState:
    """Return the initial application state."""
    # Note: We don't load persisted state here because we need filesystem data first
    # The app.py's load_data method will handle merging persisted state with filesystem data
    return AppState(
        included_paths=set(),
        edges={},
        folders=set(),
        selected_item=None,
        expanded_folders=set(),
        notification=None
    )

# Action types


class ActionType:
    """Constants for action types."""
    TOGGLE_INCLUDE = "TOGGLE_INCLUDE"
    MOVE_SELECTION = "MOVE_SELECTION"
    TOGGLE_EXPAND = "TOGGLE_EXPAND"
    EXPAND_ALL = "EXPAND_ALL"
    COLLAPSE_ALL = "COLLAPSE_ALL"
    SET_NOTIFICATION = "SET_NOTIFICATION"
    CLEAR_NOTIFICATION = "CLEAR_NOTIFICATION"
    LOAD_DATA = "LOAD_DATA"
    WRITE_IGNORE_FILE = "WRITE_IGNORE_FILE"

# Reducer function


def reducer(state: AppState, action: Dict[str, Any]) -> AppState:
    """
    Pure function to handle state transitions.

    Args:
        state: Current application state
        action: Action to apply with type and payload

    Returns:
        New application state
    """
    action_type = action["type"]

    if action_type == ActionType.TOGGLE_INCLUDE:
        path = action["path"]
        if not path:  # Skip empty path
            return state

        if path in state.included_paths:
            new_included = state.included_paths - {path}

            # If it's a folder, remove all children recursively
            if path in state.folders:
                from ..utils.calculations import get_all_descendants
                children_to_remove = get_all_descendants(state.edges, path)
                new_included = new_included - children_to_remove
        else:
            new_included = state.included_paths | {path}

            # If it's a folder, include all children recursively
            if path in state.folders:
                from ..utils.calculations import get_all_descendants
                children_to_include = get_all_descendants(state.edges, path)
                new_included = new_included | children_to_include

        return state.update(included_paths=new_included)

    elif action_type == ActionType.MOVE_SELECTION:
        direction = action["direction"]
        from ..utils.calculations import get_visible_items
        visible_items = get_visible_items(state)

        if not visible_items:
            return state

        if state.selected_item not in visible_items:
            return state.update(selected_item=visible_items[0])

        current_index = visible_items.index(state.selected_item)

        if direction == "down":
            new_index = (current_index + 1) % len(visible_items)
        else:  # "up"
            new_index = (current_index - 1) % len(visible_items)

        return state.update(selected_item=visible_items[new_index])

    elif action_type == ActionType.TOGGLE_EXPAND:
        path = action["path"]
        if not path or path not in state.folders:
            return state

        if path in state.expanded_folders:
            new_expanded = state.expanded_folders - {path}
        else:
            new_expanded = state.expanded_folders | {path}

        return state.update(expanded_folders=new_expanded)

    elif action_type == ActionType.EXPAND_ALL:
        return state.update(expanded_folders=state.folders.copy())

    elif action_type == ActionType.COLLAPSE_ALL:
        return state.update(expanded_folders=set())

    elif action_type == ActionType.SET_NOTIFICATION:
        return state.update(notification=action["message"])

    elif action_type == ActionType.CLEAR_NOTIFICATION:
        return state.update(notification=None)

    elif action_type == ActionType.LOAD_DATA:
        return state.update(
            edges=action["edges"],
            folders=action["folders"],
            included_paths=action["included_paths"],
            selected_item=action["selected_item"],
            expanded_folders=action["expanded_folders"]
        )

    return state
