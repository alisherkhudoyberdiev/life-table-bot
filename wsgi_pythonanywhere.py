import sys
import os

# Add your project directory to the sys.path
# PythonAnywhere'da username'ingizni o'zgartiring
path = '/home/yourusername/life-table-bot'
if path not in sys.path:
    sys.path.append(path)

# Environment variables'ni o'rnatish
os.environ['TELEGRAM_TOKEN'] = '7801647602:AAFFS4YxnQSTzF4Kj1_dHkJWBoXXdcRNyUY'
os.environ['ADMIN_ID'] = '5509505276'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'your_secure_password_here'
os.environ['SECRET_KEY'] = 'your-secret-key-change-this'
os.environ['TZ'] = 'Asia/Tashkent'

# Import your Flask app from admin panel
from web_admin.app_pythonanywhere import app

# For PythonAnywhere
application = app

if __name__ == "__main__":
    app.run() 