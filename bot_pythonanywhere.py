#!/usr/bin/env python3
"""
Life Table Bot - PythonAnywhere Continuous Runner
Bu script PythonAnywhere'da doimiy ishlovchi bot uchun
"""

import os
import sys
import logging
import time
from datetime import datetime
import threading

# Environment variables'ni o'rnatish
os.environ['TELEGRAM_TOKEN'] = '7801647602:AAFFS4YxnQSTzF4Kj1_dHkJWBoXXdcRNyUY'
os.environ['ADMIN_ID'] = '5509505276'
os.environ['TZ'] = 'Asia/Tashkent'

# Add project path
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

# Import bot modules
from src.database.database import init_database
from src.database.user_repository import UserRepository
from src.utils import localization
from src.config import TELEGRAM_TOKEN, ADMIN_ID
from src.handlers import admin, commands, callbacks
from src.jobs import send_weekly_update

from telegram import BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from src.database.sqlite_persistence import SQLitePersistence
import pytz
from datetime import time

# Load locales
try:
    localization.LOCALES, localization.QUOTES = localization.load_locales()
except Exception as e:
    logging.error(f"Failed to load localization files: {e}")
    localization.LOCALES = {
        "languages": {"uz": "🇺🇿 Oʻzbekcha", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"},
        "welcome": {"uz": "Assalomu alaykum!", "ru": "Здравствуйте!", "en": "Hello!"}
    }
    localization.QUOTES = {"uz": ["Vaqt o'tmoqda"], "ru": ["Время идет"], "en": ["Time is passing"]}

# Initialize database
init_database()
user_repo = UserRepository()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    """Post-initialization function to set bot commands."""
    bot_commands = {}
    languages = localization.LOCALES.get("languages", {"en": "English"})

    for lang_code in languages.keys():
        bot_commands[lang_code] = [
            BotCommand("start", localization.get_text("commands.start", lang_code)),
            BotCommand("menu", localization.get_text("commands.menu", lang_code)),
            BotCommand("help", localization.get_text("commands.help", lang_code)),
        ]
    
    for lang_code, cmds in bot_commands.items():
        try:
            api_lang_code = "uz" if lang_code == "uz_cyrl" else lang_code
            await application.bot.set_my_commands(cmds, language_code=api_lang_code)
        except Exception as e:
            logger.error(f"Could not set commands for language '{lang_code}': {e}")
    
    if 'en' in bot_commands:
        await application.bot.set_my_commands(bot_commands['en'])
        
    logger.info("Bot commands set for all available languages.")

def setup_bot():
    """Bot'ni sozlash va ishga tushirish"""
    persistence = SQLitePersistence()

    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .persistence(persistence)
        .post_init(post_init)
        .build()
    )

    # Add job to queue
    job_queue = application.job_queue
    # Run every Sunday at 15:27 Tashkent time (UTC+5)
    # 10:27 UTC
    job_queue.run_daily(
        send_weekly_update, 
        time=time(hour=10, minute=27, tzinfo=pytz.utc), 
        days=(6,) # 0=Monday, 6=Sunday
    )

    # Register handlers
    # Admin handlers
    application.add_handler(CommandHandler("admin", admin.admin_command))
    application.add_handler(MessageHandler(filters.Chat(ADMIN_ID) & ~filters.COMMAND, admin.handle_broadcast_message))

    # Command handlers
    application.add_handler(CommandHandler("start", commands.start_command))
    application.add_handler(CommandHandler("menu", commands.menu_command))
    application.add_handler(CommandHandler("help", commands.help_command))

    # Callback query handler
    application.add_handler(CallbackQueryHandler(callbacks.button_callback))

    # Get all localized "main menu" button texts
    try:
        menu_texts = [
            v for k, v in localization.LOCALES["main_keyboard_menu_button"].items()
        ]
    except (KeyError, AttributeError):
        menu_texts = ["☰ Asosiy Menyu", "☰ Асосий Меню", "☰ Главное Меню", "☰ Main Menu"]

    # Message handlers
    application.add_handler(MessageHandler(filters.Text(menu_texts), commands.menu_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, commands.handle_birthday_message))

    return application

def run_bot_forever():
    """Bot'ni doimiy ishlatish"""
    logger.info("🚀 Life Table Bot - PythonAnywhere Continuous Runner")
    logger.info("=" * 60)
    
    while True:
        try:
            logger.info("Bot ishga tushmoqda...")
            application = setup_bot()
            application.run_polling()
        except Exception as e:
            logger.error(f"Bot xatosi: {e}")
            logger.info("5 soniyadan keyin qayta urinish...")
            time.sleep(5)

def main():
    """Asosiy funksiya"""
    logger.info("PythonAnywhere'da doimiy ishlovchi bot ishga tushmoqda...")
    
    # Bot'ni alohida thread'da ishlatish
    bot_thread = threading.Thread(target=run_bot_forever, daemon=True)
    bot_thread.start()
    
    logger.info("Bot thread'da ishga tushdi. Asosiy thread davom etmoqda...")
    
    # Asosiy thread'da kutish
    try:
        while True:
            time.sleep(60)  # Har daqiqada tekshirish
            logger.info("Bot ishlayapti...")
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi.")

if __name__ == "__main__":
    main() 