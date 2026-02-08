#!/usr/bin/env python3
"""
This file is deprecated. Please use:
    python -m pulse <target>

Or install the package:
    pip install -e .
    pulse <target>
"""

import sys

def main():
    print("""
⚠️  DEPRECATED: pulse.py standalone is no longer supported.

Please use the new package structure:

    python -m pulse <target>

Or install the package:

    pip install -e .
    pulse <target>

For help:

    python -m pulse --help
    """)
    sys.exit(1)

if __name__ == "__main__":
    main()

