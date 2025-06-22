import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Admin User ID
ADMIN_ID = int(os.getenv("ADMIN_ID", 0)) 