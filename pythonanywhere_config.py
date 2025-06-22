# PythonAnywhere Configuration
# Bu fayl PythonAnywhere'da environment variables'ni o'rnatish uchun

import os

# Environment variables
os.environ['TELEGRAM_TOKEN'] = 'your_bot_token_here'
os.environ['ADMIN_ID'] = 'your_admin_id_here'
os.environ['TZ'] = 'Asia/Tashkent'
os.environ['LOG_LEVEL'] = 'INFO'

print("Environment variables o'rnatildi")
