#!/bin/bash

# Life Table Bot - Railway Deployment Script
# Bu script Railway'ga joylashtirish uchun maxfiylik tekshiruvlarini amalga oshiradi

echo "🚀 Life Table Bot - Railway Deployment Script"
echo "=============================================="

# Check if .env file exists and warn about security
if [ -f ".env" ]; then
    echo "⚠️  WARNING: .env file found!"
    echo "   This file contains sensitive information and should NOT be committed to Git."
    echo "   Make sure .env is in your .gitignore file."
    echo ""
fi

# Check if database file exists
if [ -f "bot_database.db" ]; then
    echo "📊 Database file found: bot_database.db"
    echo "   This will be automatically handled by Railway."
    echo ""
fi

# Check required files
echo "📋 Checking required files..."
required_files=("bot.py" "requirements.txt" "railway.json" "Procfile" "runtime.txt")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - Found"
    else
        echo "❌ $file - Missing"
        exit 1
    fi
done

echo ""
echo "🔍 Security Checklist:"
echo "======================"

# Check .gitignore for sensitive files
if grep -q "\.env" .gitignore; then
    echo "✅ .env files are ignored in .gitignore"
else
    echo "❌ .env files are NOT ignored in .gitignore"
fi

if grep -q "\.db" .gitignore; then
    echo "✅ Database files are ignored in .gitignore"
else
    echo "❌ Database files are NOT ignored in .gitignore"
fi

echo ""
echo "📝 Railway Deployment Instructions:"
echo "==================================="
echo "1. Go to https://railway.app"
echo "2. Connect your GitHub repository"
echo "3. Create a new service"
echo "4. Add environment variables:"
echo "   - TELEGRAM_TOKEN=your_bot_token"
echo "   - ADMIN_ID=your_admin_id"
echo "5. Deploy!"
echo ""
echo "🔐 Security Reminders:"
echo "======================"
echo "• Never commit .env files to Git"
echo "• Keep your bot token secret"
echo "• Only share admin ID with trusted people"
echo "• Monitor logs regularly"
echo "• Take regular backups"
echo ""
echo "✅ Deployment script completed successfully!"
echo "   Your bot is ready for Railway deployment." 