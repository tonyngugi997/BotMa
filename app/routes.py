from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    return render_template('dashboard.html')

import sqlite3
from datetime import datetime, timedelta

def get_db():
    conn = sqlite3.connect('emails.db')
    conn.row_factory = sqlite3.Row
    return conn

@bp.route('/api/stats')
def get_stats():
    conn = get_db()
    
    total = conn.execute('SELECT COUNT(*) FROM processed_emails').fetchone()[0]
    senders = conn.execute('SELECT COUNT(DISTINCT sender) FROM processed_emails').fetchone()[0]
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    last_week = conn.execute('SELECT COUNT(*) FROM processed_emails WHERE processed_at > ?', (week_ago,)).fetchone()[0]
    today = datetime.now().date().isoformat()
    today_count = conn.execute('SELECT COUNT(*) FROM processed_emails WHERE DATE(processed_at) = ?', (today,)).fetchone()[0]
    
    conn.close()
    
    return {
        'total_emails': total,
        'unique_senders': senders,
        'last_7_days': last_week,
        'today_count': today_count
    }



@bp.route('/api/categories')
def get_categories():
    conn = get_db()
    
    # Check if category column exists
    columns = conn.execute("PRAGMA table_info(processed_emails)").fetchall()
    has_category = any(col[1] == 'category' for col in columns)
    
    if not has_category:
        conn.close()
        return {'SECURITY': 0, 'PROMOTION': 0, 'PERSONAL': 0, 'BUSINESS': 0, 'SOCIAL': 0, 'OTHER': 0}
    
    rows = conn.execute('SELECT category, COUNT(*) as count FROM processed_emails GROUP BY category').fetchall()
    conn.close()
    
    return {row['category']: row['count'] for row in rows}