import os
# from dotenv import load_dotenv # Bu qator endi kerak emas

# Load environment variables from .env file
# load_dotenv() # Bu funksiya ham endi kerak emas

# Telegram Bot Token
# Ma'lumotlar endi to'g'ridan-to'g'ri os.environ'dan olinadi
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Admin User ID
ADMIN_ID = int(os.getenv("ADMIN_ID", 0)) 