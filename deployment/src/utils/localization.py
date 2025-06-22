import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_locales():
    """Loads locales and quotes from JSON files and returns them."""
    try:
        locales_path = BASE_DIR / "locales.json"
        quotes_path = BASE_DIR / "quotes.json"
        
        with open(locales_path, "r", encoding="utf-8") as f:
            locales_data = json.load(f)
        with open(quotes_path, "r", encoding="utf-8") as f:
            quotes_data = json.load(f)
        
        return locales_data, quotes_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading localization files: {e}")
        exit()

# These will be populated by bot.py
LOCALES = {}
QUOTES = {}

def get_text(key: str, lang_code: str, default: str = None) -> str:
    """
    Retrieves a localized string from the LOCALES dictionary.
    Loads locales if they haven't been loaded yet.
    """
    if not LOCALES:
        print("ERROR: LOCALES dictionary is empty. Localization will not work.")
        return default or f"_{key}_"

    try:
        # Navigate through nested keys
        keys = key.split('.')
        value = LOCALES
        for k in keys:
            value = value[k]
        
        # Try to get the text for the specified language.
        # If not found, fall back to 'uz'.
        # If 'uz' is also not found, fall back to the default value or the key itself.
        return value.get(lang_code, value.get('uz', default or f"_{key}_"))
    except KeyError:
        return default or f"_{key}_"

def get_random_quote(lang_code: str) -> str:
    """Returns a random quote for the given language."""
    import random
    # Use 'uz' as a fallback language
    lang_quotes = QUOTES.get(lang_code) or QUOTES.get('uz', ["-"])
    return random.choice(lang_quotes) 