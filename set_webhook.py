import requests
import os

# Atrof-muhit o'zgaruvchilaridan yoki to'g'ridan-to'g'ri o'rnatish
# PythonAnywhere'da environment variables'dan olinadi
TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")
# Domen nomingizni yozing
APP_NAME = os.environ.get("PYTHONANYWHERE_DOMAIN", "yourusername.pythonanywhere.com")

# Webhook URL'ni yaratish
WEBHOOK_URL = f"https://{APP_NAME}/webhook/{TOKEN}"

def set_webhook():
    """Telegram Bot uchun webhook'ni o'rnatadi."""
    print(f"Webhook o'rnatilmoqda: {WEBHOOK_URL}")

    # Telegram API ga so'rov yuborish
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP xatolarini tekshirish
        
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook muvaffaqiyatli o'rnatildi!")
            print(f"Natija: {result.get('description')}")
        else:
            print("❌ Webhook o'rnatishda xatolik yuz berdi.")
            print(f"Xato kodi: {result.get('error_code')}")
            print(f"Tavsif: {result.get('description')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ So'rov yuborishda xatolik: {e}")
    except Exception as e:
        print(f"❌ Kutilmagan xatolik: {e}")

if __name__ == "__main__":
    # Muhim! TOKEN va APP_NAME to'g'ri ekanligiga ishonch hosil qiling
    if "YOUR_TELEGRAM_TOKEN_HERE" in TOKEN or "yourusername" in APP_NAME:
        print("DIQQAT: Fayl ichidagi TOKEN yoki APP_NAME ni to'g'rilang!")
    else:
        set_webhook() 