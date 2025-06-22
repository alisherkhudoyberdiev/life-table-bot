#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WSGI entry point for Life Table Bot
This file is used by hosting providers to run the bot
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the bot
from bot import main

if __name__ == "__main__":
    main() 