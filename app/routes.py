from flask import Blueprint, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta


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
    
    return jsonify({
        'total_emails': total,
        'unique_senders': senders,
        'last_7_days': last_week,
        'today_count': today_count
    })



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


@bp.route('/api/emails')
def get_emails():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'desc')
    priority = request.args.get('priority', '')  # 'high', 'medium', 'low'
    
    offset = (page - 1) * per_page
    
    conn = get_db()
    
    query = 'SELECT * FROM processed_emails WHERE 1=1'
    params = []
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    # Priority filter
    if priority == 'high':
        query += ' AND priority_score >= 70'
    elif priority == 'medium':
        query += ' AND priority_score >= 40 AND priority_score < 70'
    elif priority == 'low':
        query += ' AND priority_score < 40'
    
    if search:
        query += ' AND (sender LIKE ? OR subject LIKE ? OR body_preview LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    if priority:
        query += f' ORDER BY priority_score DESC, processed_at {sort} LIMIT ? OFFSET ?'
    else:
        query += f' ORDER BY processed_at {sort} LIMIT ? OFFSET ?'
    
    params.extend([per_page, offset])
    
    emails = conn.execute(query, params).fetchall()
    
    # Count total with same filters
    count_query = 'SELECT COUNT(*) FROM processed_emails WHERE 1=1'
    count_params = []
    
    if category:
        count_query += ' AND category = ?'
        count_params.append(category)
    
    if priority == 'high':
        count_query += ' AND priority_score >= 70'
    elif priority == 'medium':
        count_query += ' AND priority_score >= 40 AND priority_score < 70'
    elif priority == 'low':
        count_query += ' AND priority_score < 40'
    
    if search:
        count_query += ' AND (sender LIKE ? OR subject LIKE ? OR body_preview LIKE ?)'
        count_params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    total = conn.execute(count_query, count_params).fetchone()[0]
    conn.close()
    
    return jsonify({
        'emails': [dict(email) for email in emails],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page if total > 0 else 1
    })    


@bp.route('/analytics')
def analytics():
    return render_template('analytics.html')




@bp.route('/api/analytics')
def get_analytics():
    range_param = request.args.get('range', '30d')
    conn = get_db()
    
    if range_param == '7d':
        start_date = (datetime.now() - timedelta(days=7)).isoformat()
    elif range_param == '30d':
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
    elif range_param == '90d':
        start_date = (datetime.now() - timedelta(days=90)).isoformat()
    else:
        start_date = '2020-01-01'
    
    # Daily volume (last 30 days max)
    daily = conn.execute('''
        SELECT DATE(processed_at) as date, COUNT(*) as count
        FROM processed_emails
        WHERE processed_at > ?
        GROUP BY DATE(processed_at)
        ORDER BY date DESC
        LIMIT 30
    ''', (start_date,)).fetchall()
    
    # Category distribution
    categories = conn.execute('''
        SELECT COALESCE(category, 'OTHER') as category, COUNT(*) as count
        FROM processed_emails
        WHERE processed_at > ?
        GROUP BY category
    ''', (start_date,)).fetchall()
    
    # Top senders
    top_senders = conn.execute('''
        SELECT sender, COUNT(*) as count
        FROM processed_emails
        WHERE processed_at > ?
        GROUP BY sender
        ORDER BY count DESC
        LIMIT 10
    ''', (start_date,)).fetchall()
    
    # Hourly distribution (using strftime for SQLite)
    hourly = conn.execute('''
        SELECT CAST(strftime('%H', processed_at) AS INTEGER) as hour, COUNT(*) as count
        FROM processed_emails
        WHERE processed_at > ?
        GROUP BY hour
        ORDER BY hour
    ''', (start_date,)).fetchall()
    
    # Total and unique senders for stats
    total_emails = conn.execute('SELECT COUNT(*) FROM processed_emails WHERE processed_at > ?', (start_date,)).fetchone()[0]
    unique_senders = conn.execute('SELECT COUNT(DISTINCT sender) FROM processed_emails WHERE processed_at > ?', (start_date,)).fetchone()[0]
    
    # Daily average (over days with data)
    daily_avg = int(round(total_emails / max(len(daily), 1)))
    
    conn.close()
    
    return jsonify({
        'daily': [{'date': row[0], 'count': row[1]} for row in daily][::-1],  # reverse to ascending
        'categories': {row[0]: row[1] for row in categories},
        'top_senders': [{'sender': row[0], 'count': row[1]} for row in top_senders],
        'hourly': [{'hour': row[0], 'count': row[1]} for row in hourly],
        'total_emails': total_emails,
        'unique_senders': unique_senders,
        'daily_avg': daily_avg
    })