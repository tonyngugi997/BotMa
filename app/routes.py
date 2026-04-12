from flask import Blueprint, render_template, request, jsonify

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
    per_page = request.args.get('per_page', 50, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    offset = (page - 1) * per_page
    
    conn = get_db()
    
    query = 'SELECT * FROM processed_emails WHERE 1=1'
    params = []
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    if search:
        query += ' AND (sender LIKE ? OR subject LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += ' ORDER BY processed_at DESC LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    
    emails = conn.execute(query, params).fetchall()
    
    # Get total count
    count_query = 'SELECT COUNT(*) FROM processed_emails WHERE 1=1'
    count_params = []
    if category:
        count_query += ' AND category = ?'
        count_params.append(category)
    if search:
        count_query += ' AND (sender LIKE ? OR subject LIKE ?)'
        count_params.extend([f'%{search}%', f'%{search}%'])
    
    total = conn.execute(count_query, count_params).fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'emails': [dict(email) for email in emails],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })


@bp.route('/emails')
def emails():
    return render_template('emails.html')


@bp.route('/analytics')
def analytics():
    return render_template('analytics.html')




@bp.route('/api/analytics')
def get_analytics():
    import sqlite3
    from datetime import datetime, timedelta
    
    range_param = request.args.get('range', '30d')
    conn = get_db()
    
    # Determine date filter
    if range_param == '7d':
        start_date = (datetime.now() - timedelta(days=7)).isoformat()
    elif range_param == '30d':
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
    elif range_param == '90d':
        start_date = (datetime.now() - timedelta(days=90)).isoformat()
    else:
        start_date = '2020-01-01'
    
    # Daily volume
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
        SELECT category, COUNT(*) as count
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
    
    # Hourly distribution
    hourly = conn.execute('''
        SELECT CAST(strftime('%H', processed_at) AS INTEGER) as hour, COUNT(*) as count
        FROM processed_emails
        WHERE processed_at > ?
        GROUP BY hour
        ORDER BY hour
    ''', (start_date,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'daily': [{'date': row[0], 'count': row[1]} for row in daily],
        'categories': {row[0] or 'OTHER': row[1] for row in categories},
        'top_senders': [{'sender': row[0], 'count': row[1]} for row in top_senders],
        'hourly': [{'hour': row[0], 'count': row[1]} for row in hourly]
    })