# Life Table Bot - Railway Deployment Guide

Bu bot Railway platformasiga maxfiy tarzda joylashtirish uchun qo'llanma.

## 🚀 Railway'ga Joylashtirish

### 1. Tayyorgarlik

1. [Railway](https://railway.app) hisobingizga kiring
2. GitHub repositoryingizni Railway'ga ulang
3. Yangi service yarating

### 2. Environment Variables (Maxfiy Ma'lumotlar)

Railway dashboard'da quyidagi environment variables'larni qo'shing:

#### Majburiy o'zgaruvchilar:
```
TELEGRAM_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_user_id_here
```

#### Ixtiyoriy o'zgaruvchilar:
```
TZ=Asia/Tashkent
LOG_LEVEL=INFO
```

### 3. Maxfiylik Choralari

#### Bot Token Maxfiyligi:
- Bot token'ni hech kimga bermang
- GitHub'ga hech qachon yuklamang
- Railway environment variables orqali boshqaring

#### Admin ID Maxfiyligi:
- Admin ID'ni faqat ishonchli odamlarga bering
- Bu ID orqali admin buyruqlarini boshqarish mumkin

#### Database Maxfiyligi:
- SQLite fayli avtomatik ravishda Railway'da saqlanadi
- Database backup'larini maxfiy saqlang

### 4. Deployment Jarayoni

1. **Repository'ni ulash:**
   - Railway'da "Deploy from GitHub repo" tanlang
   - Repository'ni tanlang

2. **Environment variables'ni sozlash:**
   - Variables tab'iga o'ting
   - Yuqoridagi o'zgaruvchilarni qo'shing

3. **Deploy qilish:**
   - "Deploy Now" tugmasini bosing
   - Build jarayonini kuzating

### 5. Monitoring va Logs

#### Health Check:
- `/health` endpoint orqali bot holatini tekshirish
- Railway avtomatik ravishda health check'ni amalga oshiradi

#### Logs:
- Railway dashboard'da logs'ni ko'rish
- Xatolarni va bot faoliyatini kuzatish

### 6. Xavfsizlik Maslahatlari

#### Environment Variables:
- ✅ Faqat Railway'da saqlang
- ❌ GitHub'ga yuklamang
- ❌ .env faylini commit qilmang

#### Bot Token:
- ✅ Telegram @BotFather orqali oling
- ✅ Railway environment'da saqlang
- ❌ Hech kimga bermang

#### Admin Access:
- ✅ Faqat ishonchli odamlarga bering
- ✅ Admin ID'ni maxfiy saqlang

### 7. Troubleshooting

#### Bot ishlamayapti:
1. Environment variables'ni tekshiring
2. Logs'ni ko'ring
3. Bot token'ni to'g'riligini tekshiring

#### Database muammolari:
1. SQLite fayli yaratilganini tekshiring
2. Database permissions'ni tekshiring

#### Web server muammolari:
1. PORT environment variable'ni tekshiring
2. Health check endpoint'ini tekshiring

### 8. Backup va Recovery

#### Database Backup:
```bash
# Local backup
cp bot_database.db backup_$(date +%Y%m%d_%H%M%S).db
```

#### Environment Variables Backup:
- Railway dashboard'dan export qiling
- Maxfiy joyda saqlang

### 9. Yangilashlar

#### Bot yangilash:
1. GitHub'ga yangi kod push qiling
2. Railway avtomatik ravishda yangilaydi
3. Environment variables'ni tekshiring

#### Environment variables yangilash:
1. Railway dashboard'da o'zgartiring
2. Service'ni restart qiling

### 10. Monitoring

#### Bot holatini tekshirish:
- `/health` endpoint
- Railway dashboard logs
- Telegram bot javob berishini tekshirish

#### Performance monitoring:
- Railway metrics
- Database hajmi
- Memory usage

## 🔐 Maxfiylik Eslatmalari

1. **Hech qachon maxfiy ma'lumotlarni GitHub'ga yuklamang**
2. **Bot token'ni maxfiy saqlang**
3. **Admin ID'ni faqat ishonchli odamlarga bering**
4. **Muntazam ravishda backup oling**
5. **Logs'ni kuzatib boring**

## 📞 Yordam

Muammolar bo'lsa:
1. Railway logs'ni tekshiring
2. Environment variables'ni tekshiring
3. Bot token'ni to'g'riligini tekshiring
4. Database faylini tekshiring

---

**Eslatma:** Bu bot maxfiy ma'lumotlar bilan ishlaydi. Barcha maxfiylik choralarini bajaring! 