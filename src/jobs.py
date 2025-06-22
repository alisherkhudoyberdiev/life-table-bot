import logging
import random
from datetime import datetime

from telegram import Bot

from .database.user_repository import UserRepository
from .utils import localization
from .utils.image_generator import generate_life_table_image

logger = logging.getLogger(__name__)
user_repo = UserRepository()

async def send_weekly_update(bot: Bot) -> tuple[int, int]:
    """
    Sends a weekly life table update to all users who have set their birthday.
    Returns a tuple of (successful_sends, total_users).
    """
    logger.info("Running weekly update job...")
    
    users_with_birthday = user_repo.get_users_with_birthday()
    total_users = len(users_with_birthday)
    successful_sends = 0
    
    if not total_users:
        logger.info("No users with birthdays found. Skipping weekly update.")
        return 0, 0

    for user in users_with_birthday:
        try:
            user_id = user['telegram_id']
            lang_code = user.get('language', 'uz')
            birthday_str = user.get('birthday')
            
            if not birthday_str:
                continue

            birthday = datetime.fromisoformat(birthday_str.split(" ")[0])

            # Generate image
            image_bytes = generate_life_table_image(
                birthday=birthday,
                lang_code=lang_code,
                locales=localization.LOCALES,
                quotes=localization.QUOTES
            )
            
            # Prepare caption
            weeks_passed = (datetime.now() - birthday).days // 7
            caption = localization.get_text("table_caption", lang_code).format(weeks_passed=weeks_passed)
            
            # Add a random quote to the caption
            lang_quotes = localization.QUOTES.get(lang_code, [])
            if lang_quotes:
                quote = random.choice(lang_quotes)
                quote_title = localization.get_text("weekly_update.quote_of_the_week", lang_code)
                caption += f"\n\n{quote_title}:\n{quote}"

            await bot.send_photo(chat_id=user_id, photo=image_bytes, caption=caption)
            logger.info(f"Sent weekly update to user {user_id}")
            successful_sends += 1
            
        except Exception as e:
            logger.error(f"Failed to send weekly update to user {user.get('telegram_id')}: {e}")
            
    logger.info(f"Weekly update job finished. Sent to {successful_sends}/{total_users} users.")
    return successful_sends, total_users 