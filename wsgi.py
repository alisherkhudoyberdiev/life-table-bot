import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/life-table-bot'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from bot import app

# For PythonAnywhere
application = app

if __name__ == "__main__":
    app.run()
