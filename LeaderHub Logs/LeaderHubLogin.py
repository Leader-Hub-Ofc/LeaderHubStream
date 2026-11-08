from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- User Database Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# --- 1. Register Route (Save login details securely) ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and Password are required!"}), 400

    username = data['username']
    password = data['password']

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists!"}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    try:
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- 2. Login Route (Verify credentials from database) ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and Password are required!"}), 400

    username = data['username']
    password = data['password']

    # Find user in database
    user = User.query.filter_by(username=username).first()

    # Verify user exists and password matches the hash
    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "Login successful!", "status": "success"}), 200
    else:
        return jsonify({"error": "Invalid username or password!"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
