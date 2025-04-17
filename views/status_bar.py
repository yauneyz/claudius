"""
Status bar widget for Claudius.
Displays notifications and key bindings.
"""
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget


class StatusBar(Widget):
    """Status bar widget for displaying notifications."""

    DEFAULT_CSS = """
    StatusBar {
        dock: bottom;
        height: 1;
        background: $surface;
        color: $text;
    }
    
    StatusBar.notification {
        background: $success;
        color: $text;
    }
    """

    def __init__(self, name: str = None) -> None:
        super().__init__(name=name)
        self.message = None

    def update_message(self, message: str) -> None:
        """
        Update the status message.

        Args:
            message: Message to display
        """
        self.message = message
        self.add_class("notification")
        self.refresh()

    def clear_message(self) -> None:
        """Clear the status message."""
        self.message = None
        self.remove_class("notification")
        self.refresh()

    def render(self) -> RenderableType:
        """
        Render the status bar.

        Returns:
            Rich renderable
        """
        if self.message:
            return Text(f" {self.message} ", style="bold")

        # Show key bindings when no message is displayed
        keys = [
            ("j/k", "Navigate"),
            ("Tab", "Toggle Folder"),
            ("Enter", "Toggle Include"),
            ("w", "Write .claudeignore"),
            ("o", "Expand All"),
            ("p", "Collapse All"),
            ("q", "Quit")
        ]

        help_text = Text(" ")
        for key, description in keys:
            help_text.append(key, style="bold")
            help_text.append(f": {description} ", style="italic")
            help_text.append(" | ", style="dim")

        # Remove the last separator
        if help_text.plain.endswith(" | "):
            help_text = Text(help_text.plain[:-3], style=help_text.style)

        return help_text
