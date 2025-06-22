# Life Table Bot Web Admin Interface

Bu Life Table Bot uchun web admin interfeysi. Flask yordamida yaratilgan va bot ma'lumotlarini boshqarish imkonini beradi.

## Xususiyatlar

### 🔐 **Autentifikatsiya**
- Admin login tizimi
- Xavfsiz parol hash
- Session boshqaruvi

### 📊 **Dashboard**
- Umumiy statistika
- Faol foydalanuvchilar soni
- So'nggi qo'shilgan foydalanuvchilar
- Tez amallar paneli

### 👥 **Foydalanuvchilar Boshqaruvi**
- Barcha foydalanuvchilar ro'yxati
- Qidiruv va filtrlash
- Foydalanuvchi holatini o'zgartirish
- Batafsil ma'lumotlar

### 📈 **Statistika**
- Buyruqlar statistikasi (Chart.js)
- Tillar bo'yicha taqsimot
- Interaktiv grafiklar
- Avtomatik yangilanish

### 📢 **Broadcast**
- Barcha foydalanuvchilarga xabar yuborish
- Xabar turi tanlash
- Ko'rinish oldindan ko'rish
- Broadcast tarixi

## O'rnatish

### 1. **Kutubxonalarni o'rnatish**
```bash
cd web_admin
pip install -r requirements.txt
```

### 2. **Muhit o'zgaruvchilarini sozlash**
```bash
# .env faylini yarating
echo "SECRET_KEY=your-secret-key-here" > .env
```

### 3. **Bot ma'lumotlar bazasini ulash**
```bash
# Bot ma'lumotlar bazasi faylini nusxalang
cp ../bot_database.db .
```

### 4. **Ishga tushirish**
```bash
python app.py
```

## Foydalanish

### **Default Login:**
- **Username:** `admin`
- **Password:** `admin123`

### **URL:**
- **Local:** `http://localhost:5000`
- **Login:** `http://localhost:5000/login`

## Tuzilishi

```
web_admin/
├── app.py                 # Asosiy Flask ilovasi
├── requirements.txt       # Python kutubxonalari
├── templates/            # HTML shablonlar
│   ├── base.html         # Asosiy shablon
│   ├── login.html        # Login sahifasi
│   ├── dashboard.html    # Dashboard
│   ├── users.html        # Foydalanuvchilar
│   ├── statistics.html   # Statistika
│   └── broadcast.html    # Broadcast
└── README.md            # Bu fayl
```

## API Endpoints

### **Asosiy sahifalar:**
- `GET /` - Dashboard
- `GET /login` - Login sahifasi
- `GET /users` - Foydalanuvchilar
- `GET /statistics` - Statistika
- `GET /broadcast` - Broadcast

### **API:**
- `GET /api/stats` - Real-time statistika
- `POST /user/{id}/toggle_status` - Foydalanuvchi holatini o'zgartirish

## Xavfsizlik

### **Autentifikatsiya:**
- Session-based login
- Password hashing (Werkzeug)
- Login required decorator

### **Ma'lumotlar himoyasi:**
- SQLite ma'lumotlar bazasi
- Read-only bot ma'lumotlari
- Admin faqat o'qish va ba'zi o'zgartirishlar

## Rivojlantirish

### **Qo'shiladigan xususiyatlar:**
- [ ] Real-time notifications
- [ ] Export ma'lumotlar
- [ ] Ko'proq grafiklar
- [ ] Foydalanuvchi guruhlari
- [ ] Avtomatik hisobotlar

### **Texnik yaxshilanishlar:**
- [ ] Redis cache
- [ ] Celery background tasks
- [ ] Docker containerization
- [ ] Production deployment

## Muammolarni hal qilish

### **Ma'lumotlar bazasi ulanish xatosi:**
```bash
# Bot ma'lumotlar bazasi mavjudligini tekshiring
ls -la ../bot_database.db
```

### **Port band:**
```bash
# Boshqa port ishlatish
python app.py --port 5001
```

### **Login muammosi:**
```bash
# Admin foydalanuvchini qayta yarating
rm admin_users.db
python app.py
```

## Litsenziya

Bu loyiha Life Table Bot bilan birga ishlaydi va shu loyihaning bir qismi hisoblanadi. 