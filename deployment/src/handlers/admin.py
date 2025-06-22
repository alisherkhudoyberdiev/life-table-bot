import os
import asyncio
from functools import wraps
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.config import ADMIN_ID
from src.database.user_repository import UserRepository
from src.database.stats_repository import StatsRepository
from src.utils import localization
from src.utils.helpers import get_user_lang
from src.jobs import send_weekly_update

# Initialize repositories and logger
user_repo = UserRepository()
stats_repo = StatsRepository()
logger = logging.getLogger(__name__)

# Environment variables
# ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# --- Decorators ---

def admin_only(func):
    """Decorator to restrict usage of a handler to the admin."""
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            lang_code = get_user_lang(context)
            if update.message:
                await update.message.reply_text(localization.get_text("admin.access_denied", lang_code))
            elif update.callback_query:
                await update.callback_query.answer(localization.get_text("admin.access_denied", lang_code), show_alert=True)
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

# --- Admin Command Handlers ---

@admin_only
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the admin panel."""
    stats_repo.track_command_usage('admin', update.effective_user.id)
    lang_code = get_user_lang(context)
    keyboard = [
        [InlineKeyboardButton(localization.get_text("admin.broadcast_button", lang_code), callback_data="admin_broadcast")],
        [InlineKeyboardButton(localization.get_text("admin.analytics_button", lang_code), callback_data="admin_analytics")],
        [InlineKeyboardButton(localization.get_text("admin.manual_weekly_update_button", lang_code), callback_data="admin_manual_weekly_update")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=localization.get_text("admin.admin_menu_title", lang_code), reply_markup=reply_markup)

@admin_only
async def manual_weekly_update_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the manual weekly update button."""
    lang_code = get_user_lang(context)
    await update.callback_query.answer("🚀 Starting manual weekly update for all users...")
    
    successful_sends, total_users = await send_weekly_update(context)
    
    response_text = localization.get_text("admin.manual_weekly_update_finished", lang_code).format(
        successful_sends=successful_sends,
        total_users=total_users
    )
    await update.callback_query.message.reply_text(text=response_text)

async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle broadcast messages from admin."""
    if not context.user_data.get('awaiting_broadcast'):
        return

    context.user_data.pop('awaiting_broadcast')
    
    all_users = user_repo.get_all_users()
    all_user_ids = [user['telegram_id'] for user in all_users]
    
    successful_sends = 0
    failed_sends = 0
    
    message = update.message
    
    # Show initial status to admin
    await message.reply_text(f"📢 Broadcasting to {len(all_user_ids)} users. Please wait...")
    
    async def send_message_to_user(user_id):
        nonlocal successful_sends, failed_sends
        try:
            # copy_message handles all message types including text, photo, video etc.
            await context.bot.copy_message(
                chat_id=user_id, 
                from_chat_id=message.chat_id, 
                message_id=message.message_id
            )
            successful_sends += 1
        except Exception as e:
            error_message = str(e).lower()
            logger.error(f"Failed to send broadcast to {user_id}: {error_message}")
            failed_sends += 1
            if "user is deactivated" in error_message or "bot was blocked by the user" in error_message:
                user_repo.deactivate_user(user_id)
                logger.info(f"Deactivated user {user_id}")
        await asyncio.sleep(0.1) # Respect rate limits
    
    tasks = [send_message_to_user(user_id) for user_id in all_user_ids]
    await asyncio.gather(*tasks)
    
    await update.message.reply_text(
        f"📢 *Broadcast Finished*\n\n"
        f"✅ Sent: {successful_sends}\n"
        f"❌ Failed: {failed_sends}\n"
        f"📊 Total Users: {len(all_user_ids)}",
        parse_mode="Markdown"
    ) 