# Life Table Bot

Bu Telegram boti foydalanuvchilarga ularning hayotini haftalarda ko'rsatadigan shaxsiy jadval yuboradi.

![Example Image](https://i.imgur.com/7A5zZtS.png)

## 🌟 Xususiyatlar

- **Shaxsiy jadval** - 90 yillik hayotni 52x90 haftalik jadval ko'rinishida
- **Avtomatik yangilanish** - Har yakshanba avtomatik jadval yuborish
- **Ko'p tillilik** - 4 ta til: O'zbekcha, Ўзбекча, Русский, English
- **Web Admin Panel** - To'liq boshqaruv interfeysi
- **Statistika** - Batafsil foydalanuvchilar va buyruqlar statistikasi
- **Broadcast** - Barcha foydalanuvchilarga xabar yuborish

## 🚀 Tez boshlash

### 1. Bot o'rnatish

```bash
# Repository'ni klonlash
git clone https://github.com/yourusername/life-table-bot.git
cd life-table-bot

# Virtual environment yaratish
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env faylini yaratish
echo "TELEGRAM_TOKEN=your_bot_token_here" > .env
echo "ADMIN_ID=your_telegram_id" >> .env

# Botni ishga tushirish
python3 bot.py
```

### 2. Web Admin Panel

```bash
# Web admin papkasiga o'tish
cd web_admin

# Avtomatik o'rnatish
./start.sh

# Yoki qo'lda
python3 -m pip install -r requirements.txt
python3 app.py
```

**Web Admin URL:** `http://localhost:5000`
- **Login:** `admin`
- **Parol:** `admin123`

## 📁 Loyiha tuzilishi

```
Life Table Bot/
├── bot.py                 # Asosiy bot fayli
├── requirements.txt       # Bot kutubxonalari
├── .env                  # Muhit o'zgaruvchilari
│   └── NotoSans-Regular.ttf
├── src/                 # Bot kodi
│   ├── config.py        # Konfiguratsiya
│   ├── database/        # Ma'lumotlar bazasi
│   ├── handlers/        # Bot buyruqlari
│   ├── jobs.py          # Avtomatik vazifalar
│   └── utils/           # Yordamchi funksiyalar
├── web_admin/           # Web admin panel
│   ├── app.py           # Flask ilovasi
│   ├── templates/       # HTML shablonlar
│   ├── requirements.txt # Web admin kutubxonalari
│   ├── start.sh         # Ishga tushirish scripti
│   └── Dockerfile       # Docker image
├── locales.json         # Ko'p tillilik
├── quotes.json          # Motivatsion iqtiboslar
└── README.md           # Hujjat
```

## 🔧 Konfiguratsiya

### Bot Token olish

1. [@BotFather](https://t.me/botfather) ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username bering
4. Olingan token'ni `.env` fayliga saqlang

### .env fayli

```env
TELEGRAM_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
```

## 📊 Web Admin Panel

### Xususiyatlar

- **Dashboard** - Umumiy statistika va so'nggi foydalanuvchilar
- **Foydalanuvchilar** - Barcha foydalanuvchilarni boshqarish
- **Statistika** - Buyruqlar va tillar statistikasi
- **Broadcast** - Barcha foydalanuvchilarga xabar yuborish

### Docker bilan ishga tushirish

```bash
cd web_admin
docker-compose up -d
```

## 🛠️ Texnik ma'lumotlar

### Bot texnologiyalari
- **python-telegram-bot** - Telegram API
- **SQLAlchemy** - Ma'lumotlar bazasi ORM
- **Pillow** - Rasm yaratish
- **APScheduler** - Rejalashtirish

### Web Admin texnologiyalari
- **Flask** - Web framework
- **Bootstrap 5** - UI framework
- **Chart.js** - Interaktiv grafiklar
- **SQLite** - Ma'lumotlar bazasi

## 📈 Statistika

Bot quyidagi ma'lumotlarni saqlaydi:
- Foydalanuvchilar ma'lumotlari
- Buyruqlar statistikasi
- Bot ma'lumotlari
- Avtomatik yangilanishlar

## 🌐 Ko'p tillilik

Qo'llab-quvvatlanadigan tillar:
- 🇺🇿 O'zbekcha
- 🇺🇿 Ўзбекча  
- 🇷🇺 Русский
- 🇬🇧 English

## 🔒 Xavfsizlik

- Admin tizimi
- Session-based autentifikatsiya
- Password hashing
- CSRF himoyasi
- XSS himoyasi

## 🚀 Deployment

### Lokal ishga tushirish
```bash
# Bot
python3 bot.py

# Web Admin
cd web_admin
python3 app.py
```

### Production
```bash
# Docker
cd web_admin
docker-compose up -d

# Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 API

### Bot buyruqlari
- `/start` - Botni boshlash
- `/menu` - Asosiy menyu
- `/help` - Yordam

### Web Admin API
- `GET /api/stats` - Real-time statistika
- `POST /user/{id}/toggle_status` - Foydalanuvchi holatini o'zgartirish

## 🤝 Hissa qo'shish

1. Repository'ni fork qiling
2. Feature branch yarating (`git checkout -b feature/amazing-feature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add amazing feature'`)
4. Branch'ga push qiling (`git push origin feature/amazing-feature`)
5. Pull Request yarating

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun `LICENSE` faylini ko'ring.

## 📞 Aloqa

- **Telegram:** [@your_username](https://t.me/your_username)
- **Email:** your.email@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)

## 🙏 Minnatdorchilik

Bu bot AI yordamida yaratilgan va open source jamiyatining hissasi hisoblanadi.

---

⭐ Agar bu loyiha sizga foydali bo'lsa, uni yulduz bilan belgilang! 