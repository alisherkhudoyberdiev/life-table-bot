#!/usr/bin/env python3
"""
Life Table Bot - PythonAnywhere Deployment Script
Bu script PythonAnywhere'ga joylashtirish uchun ishlatiladi
"""

import os
import sys
from pathlib import Path

def create_wsgi_file():
    """WSGI file yaratish PythonAnywhere uchun"""
    wsgi_content = '''import sys
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
'''
    
    with open('wsgi.py', 'w') as f:
        f.write(wsgi_content)
    
    print("✅ wsgi.py fayli yaratildi")

def create_pythonanywhere_config():
    """PythonAnywhere konfiguratsiyasi"""
    config_content = '''# PythonAnywhere Configuration
# Bu fayl PythonAnywhere'da environment variables'ni o'rnatish uchun

import os

# Environment variables
os.environ['TELEGRAM_TOKEN'] = 'your_bot_token_here'
os.environ['ADMIN_ID'] = 'your_admin_id_here'
os.environ['TZ'] = 'Asia/Tashkent'
os.environ['LOG_LEVEL'] = 'INFO'

print("Environment variables o'rnatildi")
'''
    
    with open('pythonanywhere_config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ pythonanywhere_config.py fayli yaratildi")

def create_requirements_pa():
    """PythonAnywhere uchun requirements fayli"""
    requirements_content = '''# PythonAnywhere uchun requirements
# Asosiy dependencies
python-telegram-bot==22.1
Flask==3.0.0
python-dotenv==1.1.0
SQLAlchemy==2.0.27
APScheduler==3.11.0
pillow==11.2.1
pytz==2024.1
qrcode==7.4.2
reportlab==4.0.7
Babel==2.9.1
aiofiles==23.2.1
aiogram==2.25.2
aiohttp==3.8.6
aiosignal==1.3.2
anyio==4.9.0
async-timeout==4.0.3
attrs==25.3.0
certifi==2025.1.31
charset-normalizer==3.3.2
frozenlist==1.5.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
lxml==5.4.0
magic-filter==1.0.12
multidict==6.2.0
propcache==0.3.0
pypng==0.20220715.0
python-docx==1.1.0
typing_extensions==4.14.0
tzdata==2024.1
tzlocal==5.3.1
urllib3==2.2.2
yarl==1.18.3
'''
    
    with open('requirements_pythonanywhere.txt', 'w') as f:
        f.write(requirements_content)
    
    print("✅ requirements_pythonanywhere.txt fayli yaratildi")

def main():
    """Asosiy funksiya"""
    print("🚀 Life Table Bot - PythonAnywhere Deployment")
    print("=" * 50)
    
    # Fayllarni yaratish
    create_wsgi_file()
    create_pythonanywhere_config()
    create_requirements_pa()
    
    print("\n📋 PythonAnywhere'ga joylashtirish qadamlari:")
    print("1. PythonAnywhere'ga kiring: https://www.pythonanywhere.com")
    print("2. Yangi account yarating yoki mavjud hisobingizga kiring")
    print("3. 'Files' tab'iga o'ting")
    print("4. GitHub'dan kodni clone qiling:")
    print("   git clone https://github.com/alisherkhudoyberdiev/life-table-bot.git")
    print("5. 'Web' tab'iga o'ting va yangi web app yarating")
    print("6. Source code: /home/yourusername/life-table-bot")
    print("7. WSGI configuration file'ni tahrirlang")
    print("8. Environment variables'ni o'rnating")
    print("9. Requirements'ni o'rnating:")
    print("   pip install -r requirements_pythonanywhere.txt")
    print("10. Web app'ni reload qiling")
    
    print("\n⚠️  Eslatma:")
    print("- wsgi.py faylini o'z username'ingiz bilan tahrirlang")
    print("- pythonanywhere_config.py'da maxfiy ma'lumotlarni kiriting")
    print("- Web app'da 'Code' section'da WSGI file'ni ko'rsating")

if __name__ == "__main__":
    main() 