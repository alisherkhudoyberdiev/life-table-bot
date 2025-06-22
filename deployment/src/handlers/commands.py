from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime

from src.database.user_repository import UserRepository
from src.database.stats_repository import StatsRepository
from src.utils import localization
from src.utils.helpers import get_user_lang, get_zodiac_sign

user_repo = UserRepository()
stats_repo = StatsRepository()

def get_main_reply_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    """Creates the main reply keyboard with a menu button."""
    keyboard = [[KeyboardButton(localization.get_text("main_keyboard_menu_button", lang_code))]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    stats_repo.track_command_usage('start', update.effective_user.id)
    
    # Check if user exists and has birthday set
    existing_user = user_repo.get_user(update.effective_user.id)
    
    if not existing_user:
        # New user - create and ask for language first
        user_repo.get_or_create_user(
            telegram_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )
        await choose_lang_command(update, context)
    else:
        # Existing user - check if they have birthday set
        if not existing_user.get('birthday'):
            # User exists but no birthday - ask for birthday
            lang_code = existing_user.get('language', 'uz')
            context.user_data['lang'] = lang_code
            await ask_for_birthday(update, context, lang_code)
        else:
            # User exists and has birthday - show menu and reply keyboard
            lang_code = existing_user.get('language', 'uz')
            context.user_data['lang'] = lang_code
            await update.message.reply_text(
                text="Assalomu alaykum!", # A simple greeting
                reply_markup=get_main_reply_keyboard(lang_code)
            )
            await menu_command(update, context)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the main menu."""
    stats_repo.track_command_usage('menu', update.effective_user.id)
    
    if context.user_data.get('awaiting_broadcast'):
        context.user_data.pop('awaiting_broadcast')
        await update.message.reply_text("❌ Broadcast cancelled.")
    
    lang_code = get_user_lang(context)
    keyboard = [
        [InlineKeyboardButton(localization.get_text("stats_menu_button", lang_code), callback_data="stats_menu")],
        [InlineKeyboardButton(localization.get_text("info_menu_button", lang_code), callback_data="info_menu")],
        [InlineKeyboardButton(localization.get_text("choose_lang_button", lang_code), callback_data="choose_lang")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = localization.get_text("start_text", lang_code)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the help message."""
    stats_repo.track_command_usage('help', update.effective_user.id)
    lang_code = get_user_lang(context)
    await update.message.reply_text(localization.get_text("help_text", lang_code), parse_mode="Markdown")

async def choose_lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows language selection buttons."""
    stats_repo.track_command_usage('lang', update.effective_user.id)
    # Get languages from localization module
    languages = localization.LOCALES.get("languages", {})
    if not languages:
        # Fallback if languages not loaded
        languages = {"uz": "O'zbekcha", "uz_cyrl": "Ўзбекча", "ru": "Русский", "en": "English"}
    
    buttons = [
        InlineKeyboardButton(name, callback_data=f"lang_{code}")
        for code, name in languages.items()
    ]
    keyboard_layout = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard = InlineKeyboardMarkup(keyboard_layout)
    
    text = "Tilni tanlang / Тилни танланг / Выберите язык / Choose your language:"
    
    if update.callback_query:
        await update.callback_query.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

async def ask_for_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE, lang_code: str = None) -> None:
    """Ask user to enter their birthday."""
    if lang_code is None:
        lang_code = get_user_lang(context)
    context.user_data['awaiting_birthday'] = True
    
    welcome_text = localization.get_text("welcome", lang_code)
    birthday_prompt = localization.get_text("birthday_prompt", lang_code)
    
    keyboard = [[InlineKeyboardButton(localization.get_text("cancel_button", lang_code), callback_data="cancel_birthday")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    full_text = f"{welcome_text}\n\n{birthday_prompt}"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=full_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=full_text, reply_markup=reply_markup)

async def set_birthday_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle birthday message from user."""
    if not context.user_data.get('awaiting_birthday'):
        return
    
    lang_code = get_user_lang(context)
    user_id = update.effective_user.id
    birthday_text = update.message.text.strip()
    
    try:
        # Try different date formats
        birthday = None
        for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y"]:
            try:
                birthday = datetime.strptime(birthday_text, fmt)
                break
            except ValueError:
                continue
        
        if not birthday:
            await update.message.reply_text(localization.get_text("birthday_error", lang_code))
            return
        
        # Check if the birthday is in the future
        if birthday > datetime.now():
            await update.message.reply_text(localization.get_text("birthday_in_future_error", lang_code))
            return
        
        # Save birthday to database
        success = user_repo.set_user_birthday(user_id, birthday)
        if not success:
            await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            return
        
        # Clear awaiting_birthday flag
        context.user_data.pop('awaiting_birthday', None)
        
        # Format birthday for display
        birthday_str = birthday.strftime("%d.%m.%Y")
        
        # Get weekday info
        weekday_index = birthday.weekday()
        weekdays = localization.LOCALES.get("weekdays", {}).get(lang_code, [])
        if not weekdays:  # Fallback to English if the list is empty
            weekdays = localization.LOCALES.get("weekdays", {}).get("en", [])
        weekday_name = weekdays[weekday_index] if isinstance(weekdays, list) and weekday_index < len(weekdays) else "Unknown"
        
        # Get zodiac sign
        zodiac_sign_key = get_zodiac_sign(birthday.day, birthday.month)
        zodiac_signs = localization.LOCALES.get("zodiac_signs", {})
        zodiac_info = zodiac_signs.get(zodiac_sign_key, {})
        zodiac_name = zodiac_info.get("name", {}).get(lang_code, zodiac_sign_key)
        
        # Prepare success message
        birthday_saved_text = localization.get_text("birthday_saved", lang_code).format(birthday=birthday_str)
        weekday_info = localization.get_text("birthday_weekday_info", lang_code).format(weekday=weekday_name)
        zodiac_info_text = localization.get_text("zodiac_info", lang_code).format(zodiac_sign=zodiac_name)
        
        success_message = f"{birthday_saved_text}\n\n{weekday_info}\n{zodiac_info_text}"
        
        # Show main menu and reply keyboard
        await update.message.reply_text(
            text=success_message,
            reply_markup=get_main_reply_keyboard(lang_code)
        )
        await menu_command(update, context)
        
    except Exception as e:
        print(f"Error setting birthday: {e}")
        await update.message.reply_text(localization.get_text("birthday_error", lang_code))

async def handle_birthday_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('awaiting_birthday'):
        await set_birthday_command(update, context) 