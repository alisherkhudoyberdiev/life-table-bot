#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Deployment script for Life Table Bot
This script prepares the bot for hosting deployment
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_deployment_package():
    """Create a deployment package with all necessary files"""
    
    print("🚀 Creating deployment package for Life Table Bot...")
    
    # Files to include in deployment
    essential_files = [
        'bot.py',
        'wsgi.py',
        'app.py',
        'requirements.txt',
        'locales.json',
        'quotes.json',
        '.htaccess',
        'README.md'
    ]
    
    # Directories to include
    essential_dirs = [
        'src',
        'assets'
    ]
    
    # Create deployment directory
    deploy_dir = Path('deployment')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy essential files
    for file_name in essential_files:
        if Path(file_name).exists():
            shutil.copy2(file_name, deploy_dir)
            print(f"✅ Copied: {file_name}")
        else:
            print(f"⚠️  Warning: {file_name} not found")
    
    # Copy essential directories
    for dir_name in essential_dirs:
        if Path(dir_name).exists():
            shutil.copytree(dir_name, deploy_dir / dir_name)
            print(f"✅ Copied directory: {dir_name}")
        else:
            print(f"⚠️  Warning: {dir_name} directory not found")
    
    # Create .gitignore for deployment
    gitignore_content = """# Deployment .gitignore
*.pyc
__pycache__/
*.log
.env
*.db-journal
test_*.png
"""
    
    with open(deploy_dir / '.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print(f"✅ Deployment package created in: {deploy_dir}")
    return deploy_dir

def create_installation_script():
    """Create installation script for hosting"""
    
    install_script = """#!/bin/bash
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
"""
    
    with open('install.sh', 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    # Make it executable
    os.chmod('install.sh', 0o755)
    print("✅ Created install.sh script")

def main():
    """Main deployment function"""
    
    print("🎯 Life Table Bot Deployment Tool")
    print("=" * 40)
    
    # Create deployment package
    deploy_dir = create_deployment_package()
    
    # Create installation script
    create_installation_script()
    
    print("\n📋 Deployment Summary:")
    print(f"📁 Deployment package: {deploy_dir}")
    print("📄 Installation script: install.sh")
    print("\n📝 Next steps:")
    print("1. Upload the 'deployment' folder to your hosting")
    print("2. Run 'install.sh' on your hosting server")
    print("3. Set environment variables (BOT_TOKEN, ADMIN_ID)")
    print("4. Configure your hosting to use wsgi.py or app.py")
    print("\n🔧 Hosting Configuration:")
    print("- Python version: 3.8+")
    print("- Entry point: wsgi.py or app.py")
    print("- Requirements: requirements.txt")

if __name__ == "__main__":
    main() 