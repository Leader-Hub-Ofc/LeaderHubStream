from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import traceback
from datetime import datetime

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderhub_errors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Error Log Database Model ---
class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    error_message = db.Column(db.Text, nullable=False)
    stack_trace = db.Column(db.Text, nullable=False)
    route = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(50), nullable=False)
    client_ip = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# --- Global Automatic Error Handler ---
@app.errorhandler(Exception)
def handle_exception(e):
    # Catch error details
    error_message = str(e)
    tb_str = traceback.format_exc()
    route = request.path
    method = request.method
    client_ip = request.remote_addr

    # Save bug/error automatically to database
    try:
        new_log = ErrorLog(
            error_message=error_message,
            stack_trace=tb_str,
            route=route,
            method=method,
            client_ip=client_ip
        )
        db.session.add(new_log)
        db.session.commit()
    except Exception as db_err:
        print("Database error saving log:", db_err)

    # Return clean response to the user
    return jsonify({
        "status": "error",
        "message": "An internal server error occurred. LeaderHub Admin has been notified.",
        "details": error_message
    }), 500

# --- Admin Route to View All Bugs/Errors ---
@app.route('/api/admin/bugs', methods=['GET'])
def get_bugs():
    # Admin can view all trapped errors here
    logs = ErrorLog.query.order_by(ErrorLog.timestamp.desc()).all()
    bug_list = [{
        "id": log.id,
        "error": log.error_message,
        "route": log.route,
        "method": log.method,
        "ip": log.client_ip,
        "time": log.timestamp,
        "trace": log.stack_trace
    } for log in logs]
    
    return jsonify({"total_bugs": len(bug_list), "bugs": bug_list})

# --- Sample Route with intentional bug to test ---
@app.route('/api/test-bug')
def test_bug():
    # Intentional division by zero error to test the tracker
    result = 10 / 0
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
