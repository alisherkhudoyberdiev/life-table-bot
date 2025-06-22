from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, time, date
import pytz
import random

from src.database.user_repository import UserRepository
from src.database.stats_repository import StatsRepository
from src.utils import localization
from src.utils.helpers import get_user_lang, get_zodiac_sign, calculate_weeks_passed
from src.utils.image_generator import generate_life_table_image
from src.handlers.commands import menu_command, choose_lang_command, ask_for_birthday
from src.handlers.admin import manual_weekly_update_callback

user_repo = UserRepository()
stats_repo = StatsRepository()

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    try:
        await query.answer()
    except Exception as e:
        print(f"Could not answer callback query: {e}")

    stats_repo.track_command_usage(query.data, update.effective_user.id)

    if query.data.startswith("lang_"):
        await set_language_callback(update, context)
        return

    routes = {
        "choose_lang": choose_lang_command,
        "main_menu": menu_command,
        "stats_menu": stats_menu_command,
        "info_menu": info_menu_command,
        "set_birthday_prompt": set_birthday_prompt,
        "cancel_birthday": cancel_birthday,
        "get_table": get_table_action,
        "contact_admin": contact_admin_callback,
        "other_projects": other_projects_callback,
        "about_bot": about_bot_callback,
        "admin_analytics": admin_analytics_callback,
        "admin_broadcast": admin_broadcast_callback,
        "admin_manual_weekly_update": manual_weekly_update_callback
    }

    handler = routes.get(query.data)
    if handler:
        await handler(update, context)

async def set_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = update.callback_query.data.replace("lang_", "")
    context.user_data["lang"] = lang_code
    user_repo.update_user_language(update.effective_user.id, lang_code)

    user = user_repo.get_user(update.effective_user.id)

    if not user or not user.get('birthday'):
        await ask_for_birthday_after_lang(update, context)
    else:
        lang_code = get_user_lang(context)
        keyboard = [
            [InlineKeyboardButton(localization.get_text("stats_menu_button", lang_code), callback_data="stats_menu")],
            [InlineKeyboardButton(localization.get_text("info_menu_button", lang_code), callback_data="info_menu")],
            [InlineKeyboardButton(localization.get_text("choose_lang_button", lang_code), callback_data="choose_lang")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        start_text = localization.get_text("start_text", lang_code)
        await update.callback_query.edit_message_text(text=start_text, reply_markup=reply_markup)

async def ask_for_birthday_after_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang_code = update.callback_query.data.replace("lang_", "")
    context.user_data['awaiting_birthday'] = True

    welcome_text = localization.get_text("language_selected", lang_code)
    birthday_prompt = localization.get_text("birthday_prompt", lang_code)

    keyboard = [[InlineKeyboardButton(localization.get_text("cancel_button", lang_code), callback_data="cancel_birthday")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    full_text = f"{welcome_text}\n\n{birthday_prompt}"
    await update.callback_query.edit_message_text(text=full_text, reply_markup=reply_markup)

async def set_birthday_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = get_user_lang(context)
    context.user_data['awaiting_birthday'] = True
    keyboard = [[InlineKeyboardButton(localization.get_text("cancel_button", lang_code), callback_data="cancel_birthday")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=localization.get_text("birthday_prompt", lang_code), reply_markup=reply_markup)

async def cancel_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop('awaiting_birthday', None)
    lang_code = get_user_lang(context)
    keyboard = [
        [InlineKeyboardButton(localization.get_text("stats_menu_button", lang_code), callback_data="stats_menu")],
        [InlineKeyboardButton(localization.get_text("info_menu_button", lang_code), callback_data="info_menu")],
        [InlineKeyboardButton(localization.get_text("choose_lang_button", lang_code), callback_data="choose_lang")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=localization.get_text("start_text", lang_code), reply_markup=reply_markup)

async def get_table_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang_code = get_user_lang(context)
    user_id = update.effective_user.id
    user = user_repo.get_user(user_id)

    if not user or not user.get('birthday'):
        error_message = localization.get_text("birthday_not_set_error", lang_code)
        if update.callback_query:
            await update.callback_query.answer(error_message, show_alert=True)
        else:
            await update.message.reply_text(error_message)
        return

    birthday_str = user.get('birthday')
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d") if isinstance(birthday_str, str) else birthday_str

    # --- Generate Image ---
    image_bytes = generate_life_table_image(
        birthday=birthday,
        lang_code=lang_code,
        locales=localization.LOCALES,
        quotes=localization.QUOTES
    )

    # --- Calculations ---
    now = datetime.now()
    delta = now - birthday
    weeks_passed = delta.days // 7
    days_passed = delta.days
    hours_passed = days_passed * 24
    minutes_passed = hours_passed * 60

    # --- Get Localized Info ---
    # Birthday string
    month_names = localization.LOCALES.get("months", {}).get(lang_code, [])
    birthday_formatted = f"{birthday.day} {month_names[birthday.month - 1]} {birthday.year}"
    if lang_code == "ru":
         birthday_formatted = f"{birthday.day} {month_names[birthday.month - 1]} {birthday.year} г."

    # Weekday
    weekdays = localization.LOCALES.get("weekdays", {}).get(lang_code, [])
    if not weekdays: # Fallback to English if the list is empty
        weekdays = localization.LOCALES.get("weekdays", {}).get("en", [])
    weekday_name = weekdays[birthday.weekday()] if weekdays else "N/A"

    # Zodiac
    zodiac_signs = localization.LOCALES.get("zodiac_signs", {})
    zodiac_key = get_zodiac_sign(birthday.day, birthday.month)
    zodiac_info = zodiac_signs.get(zodiac_key, {})
    zodiac_name = zodiac_info.get("name", {}).get(lang_code, zodiac_key)
    zodiac_dates = zodiac_info.get("dates", "")

    # Quote
    lang_quotes = localization.QUOTES.get(lang_code, ["-"])
    quote = random.choice(lang_quotes)

    # --- Assemble Text ---
    text = (
        f'{localization.get_text("table_text_details.header", lang_code)}\n'
        f'{localization.get_text("table_text_details.weeks_passed", lang_code).format(weeks=weeks_passed)}\n\n'
        f'{localization.get_text("table_text_details.personal_info_header", lang_code)}\n'
        f'--------------------\n'
        f'{localization.get_text("table_text_details.birthday_line", lang_code).format(birthday=birthday_formatted)}\n'
        f'{localization.get_text("table_text_details.weekday_line", lang_code).format(weekday=weekday_name)}\n'
        f'{localization.get_text("table_text_details.zodiac_line", lang_code).format(zodiac_name=zodiac_name, zodiac_dates=zodiac_dates)}\n\n'
        f'{localization.get_text("table_text_details.life_in_numbers_header", lang_code)}\n'
        f'--------------------\n'
        f'{localization.get_text("table_text_details.days_line", lang_code).format(days=f"{days_passed:,}")}\n'
        f'{localization.get_text("table_text_details.hours_line", lang_code).format(hours=f"{hours_passed:,}")}\n'
        f'{localization.get_text("table_text_details.minutes_line", lang_code).format(minutes=f"{minutes_passed:,}")}\n\n'
        f'{localization.get_text("table_text_details.wisdom_prefix", lang_code)}: {quote}'
    )

    message = update.callback_query.message if update.callback_query else update.message
    await message.reply_photo(photo=image_bytes, caption=text)

async def stats_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang_code = get_user_lang(context)
    keyboard = [
        [InlineKeyboardButton(localization.get_text("get_table_button", lang_code), callback_data="get_table")],
        [InlineKeyboardButton(localization.get_text("set_birthday_button", lang_code), callback_data="set_birthday_prompt")],
        [InlineKeyboardButton(localization.get_text("main_menu_button", lang_code), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(text=localization.get_text("stats_menu_button", lang_code), reply_markup=reply_markup)

async def info_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang_code = get_user_lang(context)
    keyboard = [
        [
            InlineKeyboardButton(localization.get_text("contact_admin_button", lang_code), callback_data="contact_admin"),
            InlineKeyboardButton(localization.get_text("other_projects_button", lang_code), callback_data="other_projects")
        ],
        [
            InlineKeyboardButton(localization.get_text("about_bot_button", lang_code), callback_data="about_bot"),
            InlineKeyboardButton(localization.get_text("donate_button", lang_code), url="https://tirikchilik.uz/alisherxudoyberdiyev")
        ],
        [InlineKeyboardButton(localization.get_text("main_menu_button", lang_code), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(text=localization.get_text("info_menu_button", lang_code), reply_markup=reply_markup)

async def contact_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = get_user_lang(context)
    await update.callback_query.edit_message_text(text=localization.get_text("contact_admin_text", lang_code))

async def other_projects_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = get_user_lang(context)
    await update.callback_query.edit_message_text(text=localization.get_text("other_projects_text", lang_code))

async def about_bot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = get_user_lang(context)
    await update.callback_query.edit_message_text(text=localization.get_text("help_text", lang_code))

async def admin_analytics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.handlers.admin import admin_only

    @admin_only
    async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
        all_users = user_repo.get_all_users()
        total_users = len(all_users)
        users_with_bd = len([user for user in all_users if user['birthday']])
        percentage_with_bd = (users_with_bd / total_users * 100) if total_users > 0 else 0
        new_users_stats = user_repo.get_new_users_stats()
        usage_stats = stats_repo.get_command_usage_stats()
        sorted_usage = sorted(usage_stats.items(), key=lambda item: item[1], reverse=True)
        usage_text = "\n".join([f"- `{cmd}`: {count}" for cmd, count in sorted_usage])
        analytics_text = (
            f"📊 *Bot Analytics*\n\n"
            f"*User Base:*\n- Total Users: {total_users}\n"
            f"- Users with Birthday: {users_with_bd} ({percentage_with_bd:.2f}%)\n\n"
            f"*New Users:*\n- Last 24h: {new_users_stats['24h']}\n"
            f"- Last 7d: {new_users_stats['7d']}\n- Last 30d: {new_users_stats['30d']}\n\n"
            f"*Command/Button Usage:*\n{usage_text}"
        )
        await update.callback_query.edit_message_text(text=analytics_text, parse_mode="Markdown")

    await analytics(update, context)

async def admin_broadcast_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_broadcast'] = True
    broadcast_instructions = (
        "📣 *Broadcast Message*\n\n"
        "Send the message you want to broadcast now. It can be text, photo, video, etc.\n\n"
        "To cancel, use the /menu command."
    )
    await update.callback_query.edit_message_text(text=broadcast_instructions, parse_mode="Markdown")
