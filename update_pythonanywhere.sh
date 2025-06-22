#!/bin/bash

echo "🔄 Life Table Bot yangilanmoqda..."

# Bot'ni to'xtatish
echo "⏹️  Bot to'xtatilmoqda..."
pkill -f "python bot_pythonanywhere.py"

# Yangi kodni yuklash
echo "📥 Yangi kod yuklanmoqda..."
git pull origin main

# Dependencies yangilash
echo "📦 Dependencies yangilanmoqda..."
pip install -r requirements_pythonanywhere.txt

# Bot'ni qayta ishga tushirish
echo "🚀 Bot qayta ishga tushirilmoqda..."
nohup python bot_pythonanywhere.py > bot.log 2>&1 &

echo "✅ Yangilash tugallandi!"
echo "📊 Bot logs: tail -f bot.log"
echo "🌐 Web app'ni reload qiling" 