# -*- coding: utf-8 -*-
import asyncio
import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy

# Botga kerakli modullarni import qilish
from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

# Proyekt ichidagi modullarni import qilish
# Path'ni to'g'ri sozlash kerak bo'lishi mumkin
import sys
# Bu web_admin papkasidan bir pog'ona yuqoriga chiqib, asosiy papkani qo'shadi
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import ADMIN_ID, TELEGRAM_TOKEN
from src.database.database import init_database
from src.database.sqlite_persistence import SQLitePersistence
from src.handlers import admin, callbacks, commands
from src.utils import localization

# --- Flask App Konfiguratsiyasi ---
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- Lokalizatsiya va Bot Boshlang'ich Sozlamalari ---
try:
    localization.LOCALES, localization.QUOTES = localization.load_locales()
except Exception as e:
    app.logger.error(f"Failed to load localization files: {e}")
    # Fallback ma'lumotlar
    localization.LOCALES = {"languages": {"en": "English"}, "welcome": {"en": "Hello!"}}
    localization.QUOTES = {"en": ["Time is passing"]}

init_database()


# --- Telegram Botni Sozlash (Webhook uchun) ---
persistence = SQLitePersistence(filepath='bot_database.db')
bot_app = (
    Application.builder()
    .token(TELEGRAM_TOKEN)
    .persistence(persistence)
    .build()
)

# Handlers (buyruqlar) ni ro'yxatdan o'tkazish
bot_app.add_handler(CommandHandler("start", commands.start_command))
bot_app.add_handler(CommandHandler("menu", commands.menu_command))
bot_app.add_handler(CommandHandler("help", commands.help_command))
bot_app.add_handler(CommandHandler("admin", admin.admin_command))
bot_app.add_handler(CallbackQueryHandler(callbacks.button_callback))
menu_texts = [v for k, v in localization.LOCALES.get("main_keyboard_menu_button", {}).items()]
bot_app.add_handler(MessageHandler(filters.Text(menu_texts), commands.menu_command))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, commands.handle_birthday_message))
bot_app.add_handler(MessageHandler(filters.Chat(ADMIN_ID) & ~filters.COMMAND, admin.handle_broadcast_message))


# --- Admin Panel Modellari va Funksiyalari ---
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_bot_db():
    # Path'ni to'g'rilash
    db_path = os.path.join(os.path.dirname(app.root_path), '..', 'bot_database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def parse_date(date_str):
    if not date_str: return None
    try:
        return datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
    except: return None


# --- Webhook uchun Asosiy Yo'l (Route) ---
@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
async def webhook():
    """Telegramdan kelgan xabarlarni qabul qiladi"""
    if request.is_json:
        update_data = request.get_json()
        update = Update.de_json(update_data, bot_app.bot)
        await bot_app.process_update(update)
        return "ok", 200
    return "Bad Request", 400


# --- Admin Panel Yo'llari (Routes) ---
@app.route('/')
@login_required
def dashboard():
    conn = get_bot_db()
    cursor = conn.cursor()
    
    # Get basic statistics
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as active FROM users WHERE is_active = 1")
    active_users = cursor.fetchone()['active']
    
    cursor.execute("SELECT COUNT(*) as with_birthday FROM users WHERE birthday IS NOT NULL")
    users_with_birthday = cursor.fetchone()['with_birthday']
    
    # Get recent users
    cursor.execute("""
        SELECT telegram_id, username, first_name, last_name, language, join_date, is_active 
        FROM users 
        ORDER BY join_date DESC 
        LIMIT 10
    """)
    recent_users = cursor.fetchall()
    
    # Convert dates to datetime objects
    for user in recent_users:
        user = dict(user)
        user['join_date'] = parse_date(user['join_date'])
    
    # Get command usage statistics
    cursor.execute("""
        SELECT command_name, SUM(usage_count) as total_usage 
        FROM command_usage 
        GROUP BY command_name 
        ORDER BY total_usage DESC 
        LIMIT 10
    """)
    command_stats = cursor.fetchall()
    
    # Get language distribution
    cursor.execute("""
        SELECT language, COUNT(*) as count 
        FROM users 
        GROUP BY language 
        ORDER BY count DESC
    """)
    language_stats = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_users=total_users,
                         active_users=active_users,
                         users_with_birthday=users_with_birthday,
                         recent_users=recent_users,
                         command_stats=command_stats,
                         language_stats=language_stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin_user = AdminUser.query.filter_by(username=username).first()
        
        if admin_user and check_password_hash(admin_user.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Muvaffaqiyatli kirildi!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Noto\'g\'ri login yoki parol!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Tizimdan chiqildi!', 'info')
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def users():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    search = request.args.get('search', '')
    
    conn = get_bot_db()
    cursor = conn.cursor()
    
    if search:
        cursor.execute("""
            SELECT * FROM users 
            WHERE username LIKE ? OR first_name LIKE ? OR last_name LIKE ?
            ORDER BY join_date DESC
            LIMIT ? OFFSET ?
        """, (f'%{search}%', f'%{search}%', f'%{search}%', per_page, (page - 1) * per_page))
    else:
        cursor.execute("""
            SELECT * FROM users 
            ORDER BY join_date DESC
            LIMIT ? OFFSET ?
        """, (per_page, (page - 1) * per_page))
    
    users = cursor.fetchall()
    
    # Convert dates to datetime objects
    for user in users:
        user = dict(user)
        user['join_date'] = parse_date(user['join_date'])
        user['birthday'] = parse_date(user['birthday'])
    
    # Get total count for pagination
    if search:
        cursor.execute("""
            SELECT COUNT(*) as count FROM users 
            WHERE username LIKE ? OR first_name LIKE ? OR last_name LIKE ?
        """, (f'%{search}%', f'%{search}%', f'%{search}%'))
    else:
        cursor.execute("SELECT COUNT(*) as count FROM users")
    
    total = cursor.fetchone()['count']
    conn.close()
    
    return render_template('users.html', 
                         users=users, 
                         page=page, 
                         per_page=per_page, 
                         total=total,
                         search=search)

@app.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    conn = get_bot_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        flash('Foydalanuvchi topilmadi!', 'error')
        return redirect(url_for('users'))
    
    # Get user's command usage
    cursor.execute("""
        SELECT command_name, usage_count, last_used 
        FROM command_usage 
        WHERE user_id = ? 
        ORDER BY last_used DESC
    """, (user_id,))
    command_usage = cursor.fetchall()
    
    conn.close()
    
    return render_template('user_detail.html', user=user, command_usage=command_usage)

@app.route('/user/<int:user_id>/toggle_status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    conn = get_bot_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT is_active FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        new_status = not user['is_active']
        cursor.execute("UPDATE users SET is_active = ? WHERE telegram_id = ?", (new_status, user_id))
        conn.commit()
        flash(f'Foydalanuvchi holati o\'zgartirildi!', 'success')
    
    conn.close()
    return redirect(url_for('user_detail', user_id=user_id))

@app.route('/statistics')
@login_required
def statistics():
    conn = get_bot_db()
    cursor = conn.cursor()
    
    # Get daily user registrations for the last 30 days
    cursor.execute("""
        SELECT DATE(join_date) as date, COUNT(*) as count 
        FROM users 
        WHERE join_date >= date('now', '-30 days')
        GROUP BY DATE(join_date)
        ORDER BY date
    """)
    daily_registrations = cursor.fetchall()
    
    # Get command usage over time
    cursor.execute("""
        SELECT DATE(last_used) as date, command_name, SUM(usage_count) as count
        FROM command_usage 
        WHERE last_used >= date('now', '-30 days')
        GROUP BY DATE(last_used), command_name
        ORDER BY date
    """)
    command_usage_time = cursor.fetchall()
    
    # Get age distribution
    cursor.execute("""
        SELECT 
            CASE 
                WHEN birthday IS NULL THEN 'Tug\'ilgan kun o\'rnatilmagan'
                WHEN julianday('now') - julianday(birthday) < 6570 THEN '0-18 yosh'
                WHEN julianday('now') - julianday(birthday) < 14600 THEN '18-40 yosh'
                WHEN julianday('now') - julianday(birthday) < 23725 THEN '40-65 yosh'
                ELSE '65+ yosh'
            END as age_group,
            COUNT(*) as count
        FROM users 
        GROUP BY age_group
        ORDER BY count DESC
    """)
    age_distribution = cursor.fetchall()
    
    conn.close()
    
    return render_template('statistics.html',
                         daily_registrations=daily_registrations,
                         command_usage_time=command_usage_time,
                         age_distribution=age_distribution)

@app.route('/broadcast', methods=['GET', 'POST'])
@login_required
def broadcast():
    if request.method == 'POST':
        message = request.form['message']
        message_type = request.form['message_type']
        
        if not message.strip():
            flash('Xabar bo\'sh bo\'lishi mumkin emas!', 'error')
            return redirect(url_for('broadcast'))
        
        # Here you would integrate with your bot's broadcast functionality
        # For now, we'll just show a success message
        flash(f'Broadcast xabar tayyorlandi! Xabar turi: {message_type}', 'success')
        return redirect(url_for('broadcast'))
    
    conn = get_bot_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_active = 1")
    active_users = cursor.fetchone()['count']
    conn.close()
    
    return render_template('broadcast.html', active_users=active_users)

@app.route('/api/stats')
@login_required
def api_stats():
    conn = get_bot_db()
    cursor = conn.cursor()
    
    # Get real-time statistics
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as active FROM users WHERE is_active = 1")
    active_users = cursor.fetchone()['active']
    
    cursor.execute("SELECT COUNT(*) as with_birthday FROM users WHERE birthday IS NOT NULL")
    users_with_birthday = cursor.fetchone()['with_birthday']
    
    # Get today's registrations
    cursor.execute("SELECT COUNT(*) as today FROM users WHERE DATE(join_date) = DATE('now')")
    today_registrations = cursor.fetchone()['today']
    
    conn.close()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'users_with_birthday': users_with_birthday,
        'today_registrations': today_registrations
    })

if __name__ == '__main__':
    # Lokal test uchun (PythonAnywhere'da ishlatilmaydi)
    with app.app_context():
        db.create_all() # Admin DB yaratish
    app.run(debug=True, host='0.0.0.0', port=5001) 