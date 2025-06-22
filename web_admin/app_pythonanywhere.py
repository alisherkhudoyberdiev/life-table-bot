from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Admin User Model
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Database connection for bot data
def get_bot_db():
    # PythonAnywhere uchun to'g'ri path
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bot_database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def parse_date(date_str):
    """Convert string date to datetime object"""
    if not date_str:
        return None
    try:
        if isinstance(date_str, str):
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_str
    except:
        return None

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
        
        # Environment variables'dan admin ma'lumotlarini olish
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        # To'g'ridan-to'g'ri tekshirish (environment variables bilan)
        if username == admin_username and password == admin_password:
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
        ORDER BY usage_count DESC
    """, (user_id,))
    command_usage = cursor.fetchall()
    
    # Convert dates
    user = dict(user)
    user['join_date'] = parse_date(user['join_date'])
    user['birthday'] = parse_date(user['birthday'])
    
    for cmd in command_usage:
        cmd = dict(cmd)
        cmd['last_used'] = parse_date(cmd['last_used'])
    
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
        new_status = 0 if user['is_active'] else 1
        cursor.execute("UPDATE users SET is_active = ? WHERE telegram_id = ?", (new_status, user_id))
        conn.commit()
        flash(f'Foydalanuvchi holati o\'zgartirildi!', 'success')
    else:
        flash('Foydalanuvchi topilmadi!', 'error')
    
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
    
    # Get language distribution
    cursor.execute("""
        SELECT language, COUNT(*) as count 
        FROM users 
        GROUP BY language 
        ORDER BY count DESC
    """)
    language_stats = cursor.fetchall()
    
    # Get command usage statistics
    cursor.execute("""
        SELECT command_name, SUM(usage_count) as total_usage 
        FROM command_usage 
        GROUP BY command_name 
        ORDER BY total_usage DESC
    """)
    command_stats = cursor.fetchall()
    
    conn.close()
    
    return render_template('statistics.html', 
                         daily_registrations=daily_registrations,
                         language_stats=language_stats,
                         command_stats=command_stats)

@app.route('/broadcast', methods=['GET', 'POST'])
@login_required
def broadcast():
    if request.method == 'POST':
        message = request.form['message']
        language = request.form.get('language', 'all')
        
        if not message.strip():
            flash('Xabar bo\'sh bo\'lishi mumkin emas!', 'error')
            return redirect(url_for('broadcast'))
        
        # Here you would implement the actual broadcast logic
        # For now, we'll just show a success message
        flash(f'Xabar {language} tilida yuborildi! (Demo)', 'success')
        return redirect(url_for('broadcast'))
    
    return render_template('broadcast.html')

@app.route('/api/stats')
@login_required
def api_stats():
    conn = get_bot_db()
    cursor = conn.cursor()
    
    # Get basic stats
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as active FROM users WHERE is_active = 1")
    active_users = cursor.fetchone()['active']
    
    cursor.execute("SELECT COUNT(*) as with_birthday FROM users WHERE birthday IS NOT NULL")
    users_with_birthday = cursor.fetchone()['with_birthday']
    
    # Get recent registrations
    cursor.execute("""
        SELECT DATE(join_date) as date, COUNT(*) as count 
        FROM users 
        WHERE join_date >= date('now', '-7 days')
        GROUP BY DATE(join_date)
        ORDER BY date
    """)
    recent_registrations = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'users_with_birthday': users_with_birthday,
        'recent_registrations': [dict(r) for r in recent_registrations]
    })

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    app.run(debug=False, host='0.0.0.0', port=5000) 