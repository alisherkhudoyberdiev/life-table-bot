#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def set_webhook():
    """Set webhook URL for the bot"""
    token = os.getenv('TELEGRAM_TOKEN')
    
    # Webhook URL - o'zgartiring
    webhook_url = "https://your-domain.com/webhook"  # O'z domain'ingizni yozing
    
    # Set webhook
    url = f"https://api.telegram.org/bot{token}/setWebhook"
    data = {
        'url': webhook_url,
        'allowed_updates': ['message', 'callback_query']
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print(f"✅ Webhook muvaffaqiyatli o'rnatildi!")
            print(f"🌐 URL: {webhook_url}")
        else:
            print(f"❌ Xatolik: {result.get('description')}")
    else:
        print(f"❌ HTTP xatolik: {response.status_code}")

def delete_webhook():
    """Delete webhook and switch to polling"""
    token = os.getenv('TELEGRAM_TOKEN')
    
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    response = requests.post(url)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ Webhook o'chirildi, polling'ga o'tildi")
        else:
            print(f"❌ Xatolik: {result.get('description')}")
    else:
        print(f"❌ HTTP xatolik: {response.status_code}")

def get_webhook_info():
    """Get current webhook info"""
    token = os.getenv('TELEGRAM_TOKEN')
    
    url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            info = result.get('result', {})
            print("📊 Webhook ma'lumotlari:")
            print(f"URL: {info.get('url', 'O\'rnatilmagan')}")
            print(f"Has custom certificate: {info.get('has_custom_certificate', False)}")
            print(f"Pending update count: {info.get('pending_update_count', 0)}")
            print(f"Last error date: {info.get('last_error_date')}")
            print(f"Last error message: {info.get('last_error_message')}")
        else:
            print(f"❌ Xatolik: {result.get('description')}")
    else:
        print(f"❌ HTTP xatolik: {response.status_code}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "set":
            set_webhook()
        elif command == "delete":
            delete_webhook()
        elif command == "info":
            get_webhook_info()
        else:
            print("❌ Noto'g'ri buyruq!")
            print("Foydalanish: python3 set_webhook.py [set|delete|info]")
    else:
        print("📋 Webhook boshqaruvi:")
        print("1. O'rnatish: python3 set_webhook.py set")
        print("2. O'chirish: python3 set_webhook.py delete")
        print("3. Ma'lumot: python3 set_webhook.py info") 