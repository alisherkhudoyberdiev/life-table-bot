from telegram import Update
from telegram.ext import ContextTypes

from helpers import get_text, get_user_lang, track_command_usage

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the help message."""
    track_command_usage(context, 'help')
    lang_code = get_user_lang(context)
    await update.message.reply_text(get_text("help_text", lang_code)) 