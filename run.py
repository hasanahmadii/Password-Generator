#!/usr/bin/env python3
"""
Launcher script for the Password Generator application.

This script launches the Streamlit application.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit application."""
    # Get the path to main.py
    src_dir = Path(__file__).parent / "src"
    main_file = src_dir / "main.py"

    if not main_file.exists():
        print(f"Error: Could not find {main_file}")
        sys.exit(1)

    # Launch streamlit
    print("🚀 Launching Password Generator...")
    print(f"📂 Running: streamlit run {main_file}")
    print("\n" + "="*60)

    try:
        subprocess.run(
            ["streamlit", "run", str(main_file)],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Error: Streamlit is not installed!")
        print("Please install it with: pip install streamlit")
        sys.exit(1)


if __name__ == "__main__":
    main()
