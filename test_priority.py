# test_priority.py
"""
Script to insert test emails with different priority scores
Run this to populate the database for testing
"""

import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "emails.db"

def insert_test_emails():
    """Insert fake emails with various priority scores"""
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # First, make sure the priority_score column exists
    try:
        cursor.execute('ALTER TABLE processed_emails ADD COLUMN priority_score INTEGER DEFAULT 50')
        print("✅ Added priority_score column")
    except sqlite3.OperationalError:
        print("✅ priority_score column already exists")
    
    # Test emails with different priority scores
    test_emails = [
        {
            'email_id': 'TEST_001',
            'sender': 'security@bankofamerica.com',
            'subject': 'SECURITY ALERT: New login detected',
            'body': 'Someone logged into your account from a new device. If this was not you, reset your password immediately.',
            'priority_score': 90,
            'category': 'SECURITY'
        },
        {
            'email_id': 'TEST_002',
            'sender': 'billing@amazon.com',
            'subject': 'URGENT: Payment failed for your order',
            'body': 'Your payment method was declined. Please update your payment info within 24 hours.',
            'priority_score': 85,
            'category': 'BUSINESS'
        },
        {
            'email_id': 'TEST_003',
            'sender': 'hr@company.com',
            'subject': 'Action Required: Complete your onboarding',
            'body': 'Please complete your new hire paperwork by Friday. This is time sensitive.',
            'priority_score': 75,
            'category': 'PERSONAL'
        },
        {
            'email_id': 'TEST_004',
            'sender': 'newsletter@techcrunch.com',
            'subject': 'Daily Tech News: AI Breakthrough',
            'body': 'Here are today top stories. Click here to unsubscribe.',
            'priority_score': 30,
            'category': 'PROMOTION'
        },
        {
            'email_id': 'TEST_005',
            'sender': 'promo@walmart.com',
            'subject': 'SALE: 50% off everything this weekend!',
            'body': 'Use code DEAL50 at checkout. Unsubscribe here if you no longer want these emails.',
            'priority_score': 20,
            'category': 'PROMOTION'
        },
        {
            'email_id': 'TEST_006',
            'sender': 'friend@gmail.com',
            'subject': 'Catch up this weekend?',
            'body': 'Hey! Been a while. Want to grab coffee on Saturday?',
            'priority_score': 60,
            'category': 'PERSONAL'
        },
        {
            'email_id': 'TEST_007',
            'sender': 'linkedin.com',
            'subject': '3 people viewed your profile',
            'body': 'See who viewed your profile and connect with recruiters.',
            'priority_score': 55,
            'category': 'SOCIAL'
        },
        {
            'email_id': 'TEST_008',
            'sender': 'noreply@twitter.com',
            'subject': 'Your tweet went viral!',
            'body': 'Your post got 10,000 likes. See the activity.',
            'priority_score': 65,
            'category': 'SOCIAL'
        },
        {
            'email_id': 'TEST_009',
            'sender': 'invoice@stripe.com',
            'subject': 'Invoice #INV-2024-001',
            'body': 'Your payment of $49.99 is due on March 1st.',
            'priority_score': 70,
            'category': 'BUSINESS'
        },
        {
            'email_id': 'TEST_010',
            'sender': 'alerts@google.com',
            'subject': 'Security verification code',
            'body': 'Your verification code is 123456. Do not share this with anyone.',
            'priority_score': 95,
            'category': 'SECURITY'
        },
        {
            'email_id': 'TEST_011',
            'sender': 'spam@unknown.com',
            'subject': 'You won $1,000,000!!!',
            'body': 'Click here to claim your prize. Limited time offer.',
            'priority_score': 10,
            'category': 'OTHER'
        },
        {
            'email_id': 'TEST_012',
            'sender': 'calendar@notifications.com',
            'subject': 'Reminder: Meeting in 1 hour',
            'body': 'Your meeting "Team Sync" starts at 2:00 PM.',
            'priority_score': 80,
            'category': 'BUSINESS'
        }
    ]
    
    # Insert each test email
    for email in test_emails:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO processed_emails 
                (email_id, sender, subject, body_preview, category, priority_score, processed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                email['email_id'],
                email['sender'],
                email['subject'],
                email['body'][:200],
                email['category'],
                email['priority_score'],
                datetime.now() - timedelta(hours=random.randint(1, 168))  # Random time in last week
            ))
            print(f"✅ Inserted: {email['email_id']} - {email['subject'][:30]}... (Score: {email['priority_score']})")
        except Exception as e:
            print(f"❌ Failed to insert {email['email_id']}: {e}")
    
    conn.commit()
    
    # Show summary
    print("\n" + "="*50)
    print("📊 DATABASE SUMMARY")
    print("="*50)
    
    # Count by priority level
    high = cursor.execute("SELECT COUNT(*) FROM processed_emails WHERE priority_score >= 70").fetchone()[0]
    medium = cursor.execute("SELECT COUNT(*) FROM processed_emails WHERE priority_score >= 40 AND priority_score < 70").fetchone()[0]
    low = cursor.execute("SELECT COUNT(*) FROM processed_emails WHERE priority_score < 40").fetchone()[0]
    
    print(f"🔴 High Priority (≥70): {high} emails")
    print(f"🟡 Medium Priority (40-69): {medium} emails")
    print(f"🟢 Low Priority (<40): {low} emails")
    print(f"📧 Total emails: {len(test_emails)}")
    
    # Show by category
    print("\n📂 By Category:")
    categories = cursor.execute("SELECT category, COUNT(*) FROM processed_emails GROUP BY category").fetchall()
    for cat, count in categories:
        print(f"   {cat}: {count}")
    
    conn.close()
    print("\n✅ Test data ready! Now run your Flask app and test the priority filter.")

def clear_test_emails():
    """Remove all test emails (IDs starting with TEST_)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processed_emails WHERE email_id LIKE 'TEST_%'")
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    print(f"🗑️ Deleted {deleted} test emails")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_test_emails()
    else:
        print("🚀 Inserting test emails...\n")
        insert_test_emails()
        print("\n" + "="*50)
        print("🧪 TO TEST THE PRIORITY FILTER:")
        print("="*50)
        print("1. Start your Flask app: python dashboard.py")
        print("2. Open browser: http://localhost:5000")
        print("3. Go to All Emails page")
        print("4. Add ?priority=high to URL or implement filter in UI")
        print("\n📡 API Test Commands:")
        print("   curl 'http://localhost:5000/api/emails?priority=high'")
        print("   curl 'http://localhost:5000/api/emails?priority=medium'")
        print("   curl 'http://localhost:5000/api/emails?priority=low'")
        print("   curl 'http://localhost:5000/api/emails?category=BUSINESS&priority=high'")