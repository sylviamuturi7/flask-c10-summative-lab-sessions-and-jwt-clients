from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, User, JournalEntry

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password_hash=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        
        return jsonify({
            "id": user.id,
            "username": user.username,
            "message": "User created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return jsonify({
                "id": user.id,
                "username": user.username,
                "message": "Login successful"
            }), 200
        
        return jsonify({"error": "Invalid username or password"}), 401
        
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500

@app.route('/check_session', methods=['GET'])
def check_session():
    try:
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user:
                return jsonify({
                    "id": user.id,
                    "username": user.username,
                    "logged_in": True
                }), 200
        
        return jsonify({"logged_in": False}), 200
        
    except Exception as e:
        return jsonify({"logged_in": False}), 200

@app.route('/logout', methods=['DELETE'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/journal', methods=['GET'])
def get_journal_entries():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    entries = JournalEntry.query.filter_by(user_id=session['user_id']).all()
    
    return jsonify([{
        "id": entry.id,
        "title": entry.title,
        "content": entry.content
    } for entry in entries]), 200

@app.route('/journal', methods=['POST'])
def create_journal_entry():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title or not content:
            return jsonify({"error": "Title and content required"}), 400
        
        if len(title) > 200:
            return jsonify({"error": "Title must be less than 200 characters"}), 400
        
        entry = JournalEntry(
            title=title,
            content=content,
            user_id=session['user_id']
        )
        
        db.session.add(entry)
        db.session.commit()
        
        return jsonify({
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "message": "Journal entry created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create journal entry"}), 500

@app.route('/journal/<int:entry_id>', methods=['GET'])
def get_journal_entry(entry_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first()
    
    if not entry:
        return jsonify({"error": "Entry not found"}), 404
    
    return jsonify({
        "id": entry.id,
        "title": entry.title,
        "content": entry.content
    }), 200

@app.route('/journal/<int:entry_id>', methods=['PATCH'])
def update_journal_entry(entry_id):
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        entry = JournalEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first()
        
        if not entry:
            return jsonify({"error": "Entry not found"}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({"error": "Title cannot be empty"}), 400
            if len(title) > 200:
                return jsonify({"error": "Title must be less than 200 characters"}), 400
            entry.title = title
        
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return jsonify({"error": "Content cannot be empty"}), 400
            entry.content = content
        
        db.session.commit()
        
        return jsonify({
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "message": "Journal entry updated successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update journal entry"}), 500

@app.route('/journal/<int:entry_id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        entry = JournalEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first()
        
        if not entry:
            return jsonify({"error": "Entry not found"}), 404
        
        db.session.delete(entry)
        db.session.commit()
        
        return jsonify({"message": "Journal entry deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete journal entry"}), 500

if __name__ == '__main__':
    app.run(debug=True)
