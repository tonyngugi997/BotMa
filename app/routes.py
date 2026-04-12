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