from telegram.ext import ContextTypes
from datetime import datetime

def get_user_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Gets user language from user_data, chat_data, or database, falling back to 'uz'.
    """
    if context.user_data and 'lang' in context.user_data:
        return context.user_data['lang']
    if context.chat_data and 'lang' in context.chat_data:
        return context.chat_data['lang']
    
    # If not in context, try to get from database
    try:
        from src.database.user_repository import UserRepository
        user_repo = UserRepository()
        user = user_repo.get_user(context.effective_user.id)
        if user and user.get('language'):
            return user['language']
    except Exception as e:
        print(f"Error getting user language from database: {e}")
    
    return 'uz'

def calculate_weeks_passed(birthday: datetime) -> int:
    """
    Calculate the number of weeks passed since birthday.
    This function correctly calculates weeks by considering the birthday as week 0.
    Takes into account leap years for accurate calculation.
    """
    from datetime import date
    
    today = date.today()
    birth_date = birthday.date()
    
    # If birthday is today or in the future, return 0
    if birth_date >= today:
        return 0
    
    # Calculate days passed using date arithmetic (handles leap years automatically)
    days_passed = (today - birth_date).days
    
    # Calculate weeks passed (birthday is week 0)
    weeks_passed = days_passed // 7
    
    return weeks_passed

def get_zodiac_sign(day: int, month: int) -> str:
    """Determines the zodiac sign based on day and month."""
    if month == 12:
        return 'sagittarius' if (day < 22) else 'capricorn'
    elif month == 1:
        return 'capricorn' if (day < 20) else 'aquarius'
    elif month == 2:
        return 'aquarius' if (day < 19) else 'pisces'
    elif month == 3:
        return 'pisces' if (day < 21) else 'aries'
    elif month == 4:
        return 'aries' if (day < 20) else 'taurus'
    elif month == 5:
        return 'taurus' if (day < 21) else 'gemini'
    elif month == 6:
        return 'gemini' if (day < 21) else 'cancer'
    elif month == 7:
        return 'cancer' if (day < 23) else 'leo'
    elif month == 8:
        return 'leo' if (day < 23) else 'virgo'
    elif month == 9:
        return 'virgo' if (day < 23) else 'libra'
    elif month == 10:
        return 'libra' if (day < 23) else 'scorpio'
    elif month == 11:
        return 'scorpio' if (day < 22) else 'sagittarius'

def debug_calculation(birthday: datetime) -> dict:
    """
    Debug function to show detailed calculation steps.
    """
    from datetime import date
    
    today = date.today()
    birth_date = birthday.date()
    
    days_passed = (today - birth_date).days
    weeks_passed = days_passed // 7
    total_weeks = 90 * 52
    percentage_lived = (weeks_passed / total_weeks) * 100
    
    return {
        'birth_date': birth_date,
        'today': today,
        'days_passed': days_passed,
        'weeks_passed': weeks_passed,
        'total_weeks': total_weeks,
        'percentage_lived': percentage_lived,
        'years_passed': days_passed // 365,
        'leap_years_in_period': count_leap_years(birth_date.year, today.year)
    }

def count_leap_years(start_year: int, end_year: int) -> int:
    """
    Count leap years between two years.
    """
    leap_years = 0
    for year in range(start_year, end_year + 1):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            leap_years += 1
    return leap_years

# We can also move the image generation logic here to group all "utility" functions
# For now, let's keep it separate to not make files too large at once. 