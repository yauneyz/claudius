"""
File tree widget for Claudius.
Renders the file tree with appropriate styling.
"""
from rich.console import RenderableType
from rich.text import Text
from rich.tree import Tree
from textual.widget import Widget

from ..models.state import AppState
from ..utils.calculations import get_display_name


class FileTree(Widget):
    """Widget for displaying the file tree."""

    DEFAULT_CSS = """
    FileTree {
        width: 1fr;
        height: 1fr;
        overflow: auto;
    }
    """

    def __init__(self, name: str = None) -> None:
        super().__init__(name=name)
        self.state = None

    def update_from_state(self, state: AppState) -> None:
        """
        Update view from app state.

        Args:
            state: Current application state
        """
        self.state = state
        self.refresh()

    def render(self) -> RenderableType:
        """
        Render the file tree.

        Returns:
            Rich renderable
        """
        if not self.state:
            return Text("Loading...")

        # Start with a root tree
        tree = Tree("📁 .")

        # Build a nested tree structure from the flat edges
        self._build_tree(tree, "", 0)

        return tree

    def _build_tree(self, tree, current_path, level):
        """
        Recursively build the tree structure.

        Args:
            tree: The current tree node
            current_path: The current path being processed
            level: The current indentation level
        """
        # Skip if not visible (parent folder not expanded)
        if level > 0 and (not current_path or current_path not in self.state.expanded_folders):
            return

        # Add children
        for child in self.state.edges.get(current_path, []):
            is_folder = child in self.state.folders
            is_included = child in self.state.included_paths
            is_selected = child == self.state.selected_item
            is_expanded = child in self.state.expanded_folders

            # Determine icon
            icon = "📁 " if is_folder else "📄 "
            if is_folder and is_expanded:
                icon = "📂 "  # Open folder icon

            # Create display text
            display_name = get_display_name(child)
            text = Text(f"{icon}{display_name}")

            # Apply styling
            if is_included:
                text.stylize("bold green")
            if is_selected:
                text.stylize("reverse")

            # Add to tree
            child_tree = tree.add(text)

            # Recursively add children if it's a folder
            if is_folder:
                self._build_tree(child_tree, child, level + 1)
