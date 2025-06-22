"""
Entry point for the News Aggregation & Analysis System.

Determines whether to launch the CLI tool using command-line arguments
or via the interactive menu if no arguments are provided.
"""

import sys
from src.cli.interface import run_cli, run_interactive_cli

if __name__ == "__main__":
    # Launch CLI with arguments if provided, otherwise run interactive menu
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_interactive_cli()
