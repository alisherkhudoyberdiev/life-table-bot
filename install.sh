#!/bin/bash
# Life Table Bot Installation Script

echo "🚀 Installing Life Table Bot..."

# Install Python dependencies
pip install -r requirements.txt

# Set proper permissions
chmod +x bot.py
chmod +x wsgi.py
chmod +x app.py

# Create logs directory
mkdir -p logs

echo "✅ Installation completed!"
echo "📝 Don't forget to:"
echo "   1. Set your BOT_TOKEN environment variable"
echo "   2. Set your ADMIN_ID environment variable"
echo "   3. Configure your hosting provider to use wsgi.py or app.py"
