# 🚀 Life Table Bot - PythonAnywhere Deployment Guide

Bu qo'llanma PythonAnywhere'da doimiy ishlovchi bot va admin panelni yuklash uchun.

## 📋 Tayyorgarlik

### 1. PythonAnywhere Account
- [PythonAnywhere](https://www.pythonanywhere.com) ga kiring
- Bepul yoki to'lovli account yarating
- Hacker plan ($5/oy) tavsiya etiladi

### 2. Kerakli Fayllar
Barcha kerakli fayllar yaratildi:
- `bot_pythonanywhere.py` - Doimiy ishlovchi bot
- `web_admin/app_pythonanywhere.py` - Admin panel
- `wsgi_pythonanywhere.py` - WSGI konfiguratsiyasi
- `requirements_pythonanywhere.txt` - Dependencies

## 🔐 Maxfiylik Sozlamalari

### Environment Variables
PythonAnywhere'da quyidagi o'zgaruvchilarni o'rnating:

```python
# wsgi_pythonanywhere.py faylida
os.environ['TELEGRAM_TOKEN'] = '7801647602:AAFFS4YxnQSTzF4Kj1_dHkJWBoXXdcRNyUY'
os.environ['ADMIN_ID'] = '5509505276'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'your_secure_password_here'
os.environ['SECRET_KEY'] = 'your-secret-key-change-this'
os.environ['TZ'] = 'Asia/Tashkent'
```

**⚠️ Eslatma:** `ADMIN_PASSWORD` va `SECRET_KEY` ni o'zgartiring!

## 🚀 Deployment Qadamlari

### 1. Kodni Yuklash

PythonAnywhere'da **Files** tab'iga o'ting va terminal'da:

```bash
git clone https://github.com/alisherkhudoyberdiev/life-table-bot.git
cd life-table-bot
```

### 2. Dependencies O'rnatish

**Consoles** tab'iga o'ting va yangi Bash console yarating:

```bash
cd life-table-bot
pip install -r requirements_pythonanywhere.txt
```

### 3. Web App Yaratish

**Web** tab'iga o'ting va:

1. **"Add a new web app"** tugmasini bosing
2. **"Manual configuration"** tanlang
3. **Python version:** 3.11 tanlang
4. **Source code:** `/home/yourusername/life-table-bot`
5. **Working directory:** `/home/yourusername/life-table-bot`

### 4. WSGI Konfiguratsiyasi

**Web** tab'ida **WSGI configuration file** ni tahrirlang:

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/life-table-bot'
if path not in sys.path:
    sys.path.append(path)

# Environment variables'ni o'rnatish
os.environ['TELEGRAM_TOKEN'] = '7801647602:AAFFS4YxnQSTzF4Kj1_dHkJWBoXXdcRNyUY'
os.environ['ADMIN_ID'] = '5509505276'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'your_secure_password_here'
os.environ['SECRET_KEY'] = 'your-secret-key-change-this'
os.environ['TZ'] = 'Asia/Tashkent'

# Import your Flask app from admin panel
from web_admin.app_pythonanywhere import app

# For PythonAnywhere
application = app
```

### 5. Doimiy Bot Ishga Tushirish

**Consoles** tab'ida yangi Bash console yarating:

```bash
cd life-table-bot
python bot_pythonanywhere.py
```

**⚠️ Muhim:** Bu console'ni yopmang! Bot doimiy ishlashi uchun console ochiq bo'lishi kerak.

### 6. Web App'ni Reload Qilish

**Web** tab'ida **"Reload"** tugmasini bosing.

## 📊 Admin Panel

### Kirish Ma'lumotlari
- **URL:** `https://yourusername.pythonanywhere.com`
- **Login:** `admin` (yoki o'zgartirgan login)
- **Parol:** `your_secure_password_here` (o'zgartirgan parol)

### Admin Panel Xususiyatlari
- ✅ Dashboard - Umumiy statistika
- ✅ Users - Foydalanuvchilar ro'yxati
- ✅ Statistics - Batafsil statistika
- ✅ Broadcast - Xabar yuborish

## 🔧 Monitoring va Logs

### Bot Logs
```bash
# Console'da bot logs'ni ko'rish
tail -f bot.log
```

### Web App Logs
PythonAnywhere **Web** tab'ida **Log files** bo'limida:
- **Error log** - Xatolar
- **Server log** - Server logs

### Bot Holatini Tekshirish
```bash
# Bot ishlayotganini tekshirish
ps aux | grep python
```

## 🛠️ Troubleshooting

### Bot Ishlamayapti
1. Console'da bot ishlayotganini tekshiring
2. Environment variables'ni tekshiring
3. Bot token'ni to'g'riligini tekshiring

### Admin Panel Ochilmayapti
1. WSGI configuration'ni tekshiring
2. Web app'ni reload qiling
3. Error logs'ni ko'ring

### Database Muammolari
1. Database fayli yaratilganini tekshiring
2. Permissions'ni tekshiring
3. Path'ni to'g'riligini tekshiring

## 🔄 Yangilashlar

### Bot Yangilash
1. GitHub'dan yangi kod o'zgartiring:
```bash
git pull origin main
```

2. Bot'ni qayta ishga tushiring:
```bash
# Eski console'ni yoping
# Yangi console yarating
python bot_pythonanywhere.py
```

### Admin Panel Yangilash
1. Web app'ni reload qiling
2. Yangi kod avtomatik yuklanadi

## 💰 Narxlar

### Bepul Plan
- ✅ 512 MB RAM
- ✅ 1 GB disk
- ✅ 1 web app
- ❌ Doimiy ishlovchi bot (console yopilganda to'xtaydi)

### Hacker Plan ($5/oy)
- ✅ 1 GB RAM
- ✅ 5 GB disk
- ✅ 2 web app
- ✅ Doimiy ishlovchi bot
- ✅ Custom domains

## 🎯 Tavsiyalar

### Xavfsizlik
1. **Kuchli parol** ishlatish
2. **SECRET_KEY** ni o'zgartirish
3. **ADMIN_PASSWORD** ni maxfiy saqlash
4. **Muntazam backup** olish

### Performance
1. **Hacker plan** ishlatish (doimiy bot uchun)
2. **Logs'ni** muntazam tozalash
3. **Database'ni** backup qilish

### Monitoring
1. **Bot logs'ni** kuzatib boring
2. **Web app logs'ni** tekshiring
3. **Database hajmini** kuzating

## 📞 Yordam

Muammolar bo'lsa:
1. PythonAnywhere **Help** bo'limiga o'ting
2. **Community forum** da savol bering
3. **Error logs'ni** ko'ring

---

**🎉 Tayyor!** Bot va admin panel PythonAnywhere'da ishga tushdi! 