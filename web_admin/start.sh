#!/bin/bash

# Life Table Bot Web Admin Startup Script

echo "🚀 Life Table Bot Web Admin ishga tushirilmoqda..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 o'rnatilmagan!"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py fayli topilmadi! Iltimos, web_admin papkasida ishlatishni tekshiring."
    exit 1
fi

# Check if bot database exists
if [ ! -f "../bot_database.db" ]; then
    echo "❌ Bot ma'lumotlar bazasi topilmadi! Iltimos, bot_database.db faylini tekshiring."
    exit 1
fi

# Copy bot database if needed
if [ ! -f "bot_database.db" ]; then
    echo "📋 Bot ma'lumotlar bazasi nusxalanmoqda..."
    cp ../bot_database.db .
fi

# Install requirements if needed
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment yaratilmoqda..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 .env fayli yaratilmoqda..."
    echo "SECRET_KEY=your-secret-key-change-this-in-production" > .env
fi

echo "✅ Barcha tayyorgarliklar tugadi!"
echo ""
echo "🌐 Web admin interfeysi: http://localhost:5000"
echo "👤 Default login: admin"
echo "🔑 Default parol: admin123"
echo ""
echo "⏹️  To'xtatish uchun Ctrl+C bosing"
echo ""

# Start the application
python3 app.py 