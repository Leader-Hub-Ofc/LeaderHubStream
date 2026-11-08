from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SecurityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    device_info = db.Column(db.String(300), nullable=False)
    access_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Verified')

# Create tables
with app.app_context():
    db.create_all()

# --- Middleware / Security Check for every request ---
@app.before_request
class SecurityVerification:
    pass

@app.route('/')
def home():
    # Capture Client Details
    client_ip = request.remote_addr
    device_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save log to database
    try:
        log = SecurityLog(ip_address=client_ip, device_info=device_info)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return jsonify({
        "message": "Welcome to LeaderHub Website",
        "security_status": "Verified (Human / Secure Connection)",
        "live_time": current_time,
        "client_ip": client_ip,
        "device_info": device_info
    })

# --- Fetch Movies Endpoint ---
@app.route('/api/movies', methods=['GET'])
def get_movies():
    query = request.args.get('query', 'avengers')
    api_key = "your_actual_api_key_here"  # Ungaloda valid API key-ai inge podunga
    url = f"https://LedaerHub/github/?s={query}&apikey={leaderhub77_api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get("Response") == "True":
            return jsonify({"status": "success", "movies": data.get("Search")})
        else:
            return jsonify({"status": "error", "message": "API Key terminated or no movies found!"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Register User ---
@app.route('/api/users', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and Email are required!"}), 400

    try:
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "User already exists or database error!"}), 400

# --- View Security Logs (Admin Route) ---
@app.route('/api/logs', methods=['GET'])
def get_security_logs():
    logs = SecurityLog.query.all()
    log_list = [{
        "id": l.id,
        "ip": l.ip_address,
        "device": l.device_info,
        "time": l.access_time
    } for l in logs]
    return jsonify(log_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
