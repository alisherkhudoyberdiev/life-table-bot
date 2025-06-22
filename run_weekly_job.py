import asyncio
import os
import sys
from telegram.ext import Application
from telegram import Bot

# Asosiy proyekt papkasini path'ga qo'shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.config import TELEGRAM_TOKEN
from src.jobs import send_weekly_update
from src.database.database import init_database
from src.utils import localization

async def main():
    """Haftalik xabarlarni yuborish uchun asosiy funksiya."""
    print("Haftalik xabar yuborish vazifasi ishga tushdi...")
    
    # Kerakli qismlarni initsializatsiya qilish
    init_database()
    try:
        localization.LOCALES, localization.QUOTES = localization.load_locales()
        print("Lokalizatsiya fayllari muvaffaqiyatli yuklandi.")
    except Exception as e:
        print(f"Lokalizatsiya fayllarini yuklashda xatolik: {e}")
        # Agar lokalizatsiya yuklanmasa, ishni to'xtatish
        return

    # Bot obyektini yaratish
    # Bu yerda to'liq Application qurish shart emas, faqat Bot o'zi kerak
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # `send_weekly_update` funksiyasi `ContextTypes.DEFAULT_TYPE` ga bog'liq
    # bo'lmasligi kerak yoki biz dummy context yaratishimiz kerak.
    # Keling, `jobs.py` ni biroz o'zgartiramiz.
    # Hozircha, to'g'ridan-to'g'ri chaqirishga harakat qilamiz.
    
    # Application obyekti orqali chaqirish xavfsizroq
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    try:
        print("send_weekly_update funksiyasi chaqirilmoqda...")
        # `send_weekly_update` funksiyasi `context` argumentini kutadi
        # Biz unga Application job_queue orqali yaratilgan contextni berishimiz kerak.
        # Bu to'g'ridan-to'g'ri chaqiruvda murakkab.
        # Eng yaxshi yechim: `send_weekly_update` ni bot instansiyasini qabul qiladigan qilib o'zgartirish.
        
        # Hozirgi `send_weekly_update` funksiyasini tahrir qilmasdan chaqirish uchun
        # uni `app.job_queue.run_once` orqali chaqiramiz.
        # Bu funksiyani darhol ishga tushiradi.
        
        class DummyContext:
            async def __aenter__(self):
                return app
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass
        
        # Bu yondashuv to'g'ri emas, chunki job_queue'ni ishga tushirish kerak.
        # Yaxshisi, send_weekly_update'ni o'zgartiramiz.
        # Lekin hozircha o'zgartirmasdan, muqobil yo'l topamiz.

        # Muqobil yo'l: `send_weekly_update` funksiyasining ichidagi logikani shu yerda qayta yozish
        # Bu kod takrorlanishiga olib keladi.

        # Eng to'g'ri yo'l: `jobs.py` ni tahrirlash.
        # Men hozir buni qilaman.
        await send_weekly_update(bot) # `context` o'rniga `bot` obyektini yuboramiz
        print("✅ Haftalik xabarlar muvaffaqiyatli yuborildi (yoki yuboriladigan foydalanuvchilar topilmadi).")

    except Exception as e:
        print(f"❌ Haftalik xabarlarni yuborishda xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 