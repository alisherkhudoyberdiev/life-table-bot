#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Alternative entry point for hosting providers
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the bot
from bot import main

# For hosting providers that expect an 'app' variable
app = main

if __name__ == "__main__":
    main() 