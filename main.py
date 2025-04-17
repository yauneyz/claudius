#!/usr/bin/env python3
"""
Claudius - A terminal UI for managing .claudeignore files.
"""
import os
import sys
from claudius.views.app import ClaudiusApp


def main():
    """Main entry point for the application."""
    app = ClaudiusApp()
    app.run()


if __name__ == "__main__":
    main()
