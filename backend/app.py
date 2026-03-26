from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
from datetime import datetime, timedelta
import os
from model import analyze_skin
from recommendations import get_recommendations  # Add this import

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'pure-and-flush-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skin_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            issues TEXT,
            recommendations TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized with users, history, and feedback tables")

init_db()

@app.route("/api/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "Username already exists"}), 400
        
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute(
            'INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)',
            (username, hashed, datetime.now().isoformat())
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        access_token = create_access_token(identity=str(user_id))
        
        return jsonify({
            "message": "User created successfully",
            "access_token": access_token,
            "user": {
                "id": user_id,
                "username": username
            }
        }), 201
        
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401
        
        if bcrypt.check_password_hash(user[2], password):
            access_token = create_access_token(identity=str(user[0]))
            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user[0],
                    "username": user[1]
                }
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== UPDATED ANALYZE ROUTE WITH RECOMMENDATIONS ====================
@app.route("/analyze", methods=["POST"])
@jwt_required()
def analyze():
    temp_path = None
    try:
        user_id = get_jwt_identity()
        print(f"✅ Analysis requested by user: {user_id}")
        
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400
        
        temp_path = f"temp_{datetime.now().timestamp()}_{file.filename}"
        file.save(temp_path)
        print(f"✅ Image saved: {temp_path}")
        
        try:
            # Get analysis from model
            result = analyze_skin(temp_path)
            
            # Add recommendations based on skin type and issues
            if 'recommendations' not in result:
                recommendations = get_recommendations(result['skin_type'], result.get('issues', []))
                result['recommendations'] = recommendations
            
            print(f"✅ Analysis complete: {result['skin_type']} ({result['confidence']:.2f})")
            
        except Exception as model_error:
            print(f"❌ Model error: {model_error}")
            result = {
                "skin_type": "Unknown",
                "confidence": 0.5,
                "issues": [{"issue": "Analysis failed", "severity": "High"}],
                "recommendations": get_recommendations("normal", [])
            }
        
        # Save to database
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO analysis_history 
                (user_id, skin_type, confidence, issues, recommendations, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                int(user_id), 
                result['skin_type'], 
                result['confidence'], 
                str(result.get('issues', [])), 
                str(result.get('recommendations', {})),
                datetime.now().isoformat()
            ))
            conn.commit()
            conn.close()
            print("✅ Analysis saved to database")
        except Exception as db_error:
            print(f"⚠️ Database save error: {db_error}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return jsonify({"error": str(e)}), 500
        
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                print("✅ Temp file removed")
            except:
                pass

@app.route("/api/history", methods=["GET"])
@jwt_required()
def get_history():
    try:
        user_id = get_jwt_identity()
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT skin_type, confidence, issues, recommendations, created_at 
            FROM analysis_history 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 20
        ''', (int(user_id),))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            issues = []
            recommendations = {}
            
            try:
                if row[2]:
                    issues = eval(row[2]) if isinstance(row[2], str) else row[2]
            except:
                issues = []
                
            try:
                if row[3]:
                    rec_data = eval(row[3]) if isinstance(row[3], str) else row[3]
                    if isinstance(rec_data, dict):
                        recommendations = rec_data
            except:
                recommendations = {}
            
            history.append({
                "skin_type": row[0],
                "confidence": row[1],
                "issues": issues,
                "recommendations": recommendations,
                "date": row[4]
            })
        
        return jsonify({"history": history})
        
    except Exception as e:
        print(f"History error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== FEEDBACK AND REPORT ROUTE ====================
@app.route("/api/feedback", methods=["POST"])
@jwt_required()
def submit_feedback():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        feedback_type = data.get('type')
        message = data.get('message')
        
        print(f"📝 Received - Type: {feedback_type}, Message: {message}, User: {user_id}")
        
        if not feedback_type:
            return jsonify({"error": "Feedback type is required"}), 400
            
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        if feedback_type not in ['feedback', 'report']:
            return jsonify({"error": "Type must be 'feedback' or 'report'"}), 400
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (user_id, type, message, created_at)
            VALUES (?, ?, ?, ?)
        ''', (
            int(user_id),
            feedback_type,
            message,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        
        print(f"✅ {feedback_type} saved to database successfully")
        
        return jsonify({
            "message": f"Thank you for your {feedback_type}!",
            "status": "success"
        }), 201
        
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== ADMIN VIEW FEEDBACK ====================
@app.route("/api/admin/feedback", methods=["GET"])
@jwt_required()
def admin_get_feedback():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.id, f.user_id, f.type, f.message, f.created_at, u.username
            FROM feedback f
            LEFT JOIN users u ON f.user_id = u.id
            ORDER BY f.created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        feedback_list = []
        for row in rows:
            feedback_list.append({
                "id": row[0],
                "user_id": row[1],
                "type": row[2],
                "message": row[3],
                "created_at": row[4],
                "username": row[5] if row[5] else "Unknown"
            })
        
        return jsonify({"feedback": feedback_list})
        
    except Exception as e:
        print(f"Admin feedback error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== DELETE FEEDBACK ====================
@app.route("/api/admin/feedback/<int:feedback_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_feedback(feedback_id):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        
        if deleted > 0:
            return jsonify({"message": "Feedback deleted successfully"}), 200
        else:
            return jsonify({"error": "Feedback not found"}), 404
            
    except Exception as e:
        print(f"Delete error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== USER PROFILE ====================
@app.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, created_at FROM users WHERE id = ?', (int(user_id),))
        user = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*) FROM analysis_history WHERE user_id = ?', (int(user_id),))
        count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM feedback WHERE user_id = ?', (int(user_id),))
        feedback_count = cursor.fetchone()[0]
        
        conn.close()
        
        if user:
            return jsonify({
                "username": user[0],
                "joined": user[1],
                "total_analyses": count,
                "total_feedback": feedback_count
            })
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        print(f"Profile error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== TEST ROUTE ====================
@app.route("/")
def home():
    return jsonify({
        "status": "Pure & Flush API Running 🚀",
        "version": "1.0.0",
        "endpoints": {
            "signup": "/api/signup (POST)",
            "login": "/api/login (POST)",
            "analyze": "/analyze (POST, requires token)",
            "history": "/api/history (GET, requires token)",
            "feedback": "/api/feedback (POST, requires token) - use type='feedback' or 'report'",
            "admin_feedback": "/api/admin/feedback (GET, requires token)",
            "profile": "/api/profile (GET, requires token)"
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("="*60)
    print("🚀 Pure & Flush Backend Server")
    print("="*60)
    print("✅ Database: users.db")
    print("✅ JWT Authentication: Enabled")
    print("✅ CORS: Enabled")
    print("✅ Server: http://localhost:5000")
    print("="*60)
    print("\n📡 Available Endpoints:")
    print("   • POST  /api/signup           - Create new account")
    print("   • POST  /api/login            - Login to account")
    print("   • POST  /analyze              - Analyze skin (needs token)")
    print("   • GET   /api/history          - View analysis history")
    print("   • POST  /api/feedback         - Submit feedback (type='feedback')")
    print("   • POST  /api/feedback         - Submit report (type='report')")
    print("   • GET   /api/admin/feedback   - View all feedback (admin)")
    print("   • GET   /api/profile          - View user profile")
    print("="*60)
    
    app.run(debug=True, port=5000)