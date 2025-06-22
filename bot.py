import logging
import os
from datetime import time, datetime
import pytz
import random
from dotenv import load_dotenv
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
from src.database.database import init_database
from src.database.user_repository import UserRepository
from src.utils import localization

# --- Load locales first, before other modules that depend on them ---
try:
    localization.LOCALES, localization.QUOTES = localization.load_locales()
except Exception as e:
    logging.error(f"Failed to load localization files: {e}")
    # Create fallback locales for basic functionality
    localization.LOCALES = {
        "languages": {"uz": "🇺🇿 Oʻzbekcha", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"},
        "welcome": {"uz": "Assalomu alaykum!", "ru": "Здравствуйте!", "en": "Hello!"}
    }
    localization.QUOTES = {"uz": ["Vaqt o'tmoqda"], "ru": ["Время идет"], "en": ["Time is passing"]}

# --- Now import other modules ---
from src.config import TELEGRAM_TOKEN, ADMIN_ID
from src.handlers import admin, commands, callbacks
from src.jobs import send_weekly_update

# Load environment variables
load_dotenv()

# Initialize database
init_database()
user_repo = UserRepository()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    """Post-initialization function to set bot commands."""
    bot_commands = {}

    # Get available languages, with a fallback
    languages = localization.LOCALES.get("languages", {"en": "English"})

    for lang_code in languages.keys():
        bot_commands[lang_code] = [
            BotCommand("start", localization.get_text("commands.start", lang_code)),
            BotCommand("menu", localization.get_text("commands.menu", lang_code)),
            BotCommand("help", localization.get_text("commands.help", lang_code)),
        ]
    
    # Set commands for each language
    for lang_code, cmds in bot_commands.items():
        try:
            # Handle non-standard 'uz_cyrl' code for Telegram
            api_lang_code = "uz" if lang_code == "uz_cyrl" else lang_code
            await application.bot.set_my_commands(cmds, language_code=api_lang_code)
        except Exception as e:
            logger.error(f"Could not set commands for language '{lang_code}': {e}")
    
    # Set default commands (e.g., for English)
    if 'en' in bot_commands:
        await application.bot.set_my_commands(bot_commands['en'])
        
    logger.info("Bot commands set for all available languages.")

persistence = SQLitePersistence()

application = (
    Application.builder()
    .token(TELEGRAM_TOKEN)
    .persistence(persistence)
    .post_init(post_init)
    .build()
)

# --- Add job to queue ---
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
    # Fallback in case locales are not loaded correctly
    menu_texts = ["☰ Asosiy Menyu", "☰ Асосий Меню", "☰ Главное Меню", "☰ Main Menu"]

# Message handlers
# The more specific handler for the menu button must come first.
application.add_handler(MessageHandler(filters.Text(menu_texts), commands.menu_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, commands.handle_birthday_message))

def main() -> None:
    """Start the bot."""
    # Run the bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main() 