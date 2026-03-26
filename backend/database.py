import sqlite3
import json
from datetime import datetime

DB_NAME = "users.db"

def init_db():
    """Create database tables if they don't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Analysis history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skin_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            issues TEXT,
            recommendations TEXT,
            image_path TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def add_user(username, password, email=None):
    """Add new user to database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password, email, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, password, email, datetime.now().isoformat()))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None  # Username already exists
    finally:
        conn.close()

def get_user_by_username(username):
    """Get user by username"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'email': user[3],
            'created_at': user[4]
        }
    return None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[3],
            'created_at': user[4]
        }
    return None

def save_analysis(user_id, skin_type, confidence, issues, recommendations):
    """Save skin analysis result to history"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO analysis_history 
        (user_id, skin_type, confidence, issues, recommendations, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id, 
        skin_type, 
        confidence, 
        json.dumps(issues), 
        json.dumps(recommendations),
        datetime.now().isoformat()
    ))
    
    conn.commit()
    analysis_id = cursor.lastrowid
    conn.close()
    return analysis_id

def get_user_history(user_id, limit=10):
    """Get user's analysis history"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM analysis_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (user_id, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'skin_type': row[2],
            'confidence': row[3],
            'issues': json.loads(row[4]),
            'recommendations': json.loads(row[5]),
            'created_at': row[7]
        })
    
    return history

# Initialize database when this file is imported
init_db()