# Life Table Bot - Hosting Deployment Guide

## 🚀 AHOST Hosting uchun joylashtirish ko'rsatmalari

### 1. Tayyorgarlik

Avval deployment paketini yarating:
```bash
python deploy.py
```

Bu sizga `deployment` papkasini yaratadi.

### 2. AHOST Hosting'ga yuklash

1. **FTP/File Manager orqali:**
   - `deployment` papkasidagi barcha fayllarni hosting'ingizning asosiy papkasiga yuklang
   - `bot_database.db` faylini ham yuklang (agar mavjud bo'lsa)

2. **Papka tuzilishi:**
   ```
   public_html/
   ├── bot.py
   ├── wsgi.py
   ├── app.py
   ├── requirements.txt
   ├── locales.json
   ├── quotes.json
   ├── .htaccess
   ├── src/
   ├── assets/
   └── bot_database.db
   ```

### 3. Muhit o'zgaruvchilarini o'rnatish

AHOST hosting panelida quyidagi environment variable'larni o'rnating:

- `BOT_TOKEN` = sizning bot token'ingiz
- `ADMIN_ID` = sizning Telegram ID'ingiz

### 4. Python kutubxonalarini o'rnatish

AHOST hosting panelida:
1. **Python Apps** bo'limiga o'ting
2. **Create App** tugmasini bosing
3. **Python version:** 3.8 yoki undan yuqori tanlang
4. **Entry point:** `wsgi.py` yoki `app.py` kiriting
5. **Requirements file:** `requirements.txt` tanlang

### 5. Botni ishga tushirish

Hosting panelida:
1. **Start App** tugmasini bosing
2. Loglarni tekshiring - xatoliklar yo'qligiga ishonch hosil qiling

### 6. Webhook sozlash (ixtiyoriy)

Agar webhook ishlatmoqchi bo'lsangiz:

```python
# bot.py faylida webhook qo'shish
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Webhook URL
WEBHOOK_URL = "https://yourdomain.com/webhook"

# Webhook sozlash
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

# Webhook handler
async def webhook_handler(request):
    return await SimpleRequestHandler(dispatcher).handle(request)

# App yaratish
app = web.Application()
app.router.add_post("/webhook", webhook_handler)
app.on_startup.append(on_startup)
```

### 7. Xavfsizlik sozlamalari

`.htaccess` fayli allaqachon yaratilgan va quyidagi xavfsizlik choralarini o'z ichiga oladi:
- Ma'lumotlar bazasi fayllariga kirishni bloklash
- Python cache fayllarini yashirish
- XSS va boshqa hujumlardan himoya

### 8. Monitoring va loglar

Bot ishlayotganini tekshirish uchun:
1. Hosting panelidagi loglarni tekshiring
2. Telegram'da botga `/start` yuboring
3. Admin panelga kirib (`/admin`) statistikalarni ko'ring

### 9. Muammolarni hal qilish

**Xatolik:** "Module not found"
- **Yechim:** `requirements.txt` faylini to'g'ri yuklang

**Xatolik:** "Bot token not found"
- **Yechim:** Environment variable `BOT_TOKEN` ni to'g'ri o'rnating

**Xatolik:** "Database error"
- **Yechim:** `bot_database.db` faylini yuklang va ruxsatlarni to'g'rilang

**Xatolik:** "Permission denied"
- **Yechim:** Fayllarga yozish ruxsatini bering (755 yoki 644)

### 10. Yangilashlar

Botni yangilash uchun:
1. Yangi kodlarni yuklang
2. `requirements.txt` ni yangilang (agar kerak bo'lsa)
3. Botni qayta ishga tushiring

### 11. Backup

Muntazam ravishda:
- `bot_database.db` faylini zaxiralang
- `locales.json` va `quotes.json` fayllarini zaxiralang

### 12. Texnik qo'llab-quvvatlash

Muammolar bo'lsa:
- Hosting loglarini tekshiring
- Telegram: @alisher_khudoyberdiev
- Email: support@lionsoft.uz

---

**🎉 Tabriklaymiz!** Botingiz endi AHOST hosting'da ishlaydi va 24/7 mavjud bo'ladi. 