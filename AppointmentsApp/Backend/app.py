import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from pyrebase import pyrebase

# Initialize Flask App
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Change this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# JWT and Limiter
jwt = JWTManager(app)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
CORS(app)

# Firebase Admin SDK Initialization
cred = credentials.Certificate("./firebase.json")  # Downloaded from Firebase Console
firebase_admin.initialize_app(cred)

# Firestore initialization
db = firestore.client()

# Pyrebase config (for Firebase Authentication)
firebase_config = {
    "apiKey": "AIzaSyBpqUri8bXF2PilpHk-Pc_I2Tht5fn4ILg",
    "authDomain": "appointmentapp-cf21e.firebaseapp.com",
    "databaseURL": "https://appointmentapp-cf21e-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "appointmentapp-cf21e",
    "storageBucket": "appointmentapp-cf21e.appspot.com",
    "messagingSenderId": "435198699958",
    "appId": "1:435198699958:web:b28a4fb48a0b88e6147917",
    "measurementId": "G-EH3PRX9381"
}
firebase = pyrebase.initialize_app(firebase_config)
auth_client = firebase.auth()

# User Registration Route
@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Firebase Authentication: Create User
        user_record = auth.create_user(
            email=data['email'],
            password=data['password']
        )
        
        # Save additional user data to Firestore
        user_data = {
            'username': data['username'],
            'is_admin': False,
            'created_at': datetime.utcnow()
        }
        db.collection('users').document(user_record.uid).set(user_data)
        
        return jsonify({"message": "User created successfully", "user_id": user_record.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User Login Route
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Authenticate with Firebase Authentication
        user = auth_client.sign_in_with_email_and_password(data['email'], data['password'])
        uid = user['localId']

        # Create JWT token
        access_token = create_access_token(identity=uid)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create Salon Route (Firestore)
@app.route('/salon', methods=['POST'])
@jwt_required()
def create_salon():
    try:
        data = request.json
        salon_data = {
            'name': data['name'],
            'address': data['address'],
            'phone': data['phone'],
            'created_at': datetime.utcnow()
        }
        db.collection('salons').add(salon_data)
        return jsonify(salon_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Salon Route
@app.route('/salon/<id>', methods=['GET'])
@jwt_required()
def get_salon(id):
    try:
        salon_ref = db.collection('salons').document(id).get()
        if not salon_ref.exists:
            return jsonify({"error": "Salon not found"}), 404
        return jsonify(salon_ref.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update Salon Route
@app.route('/salon/<id>', methods=['PUT'])
@jwt_required()
def update_salon(id):
    try:
        data = request.json
        salon_ref = db.collection('salons').document(id)
        salon_ref.update({
            'name': data['name'],
            'address': data['address'],
            'phone': data['phone'],
            'updated_at': datetime.utcnow()
        })
        return jsonify({"message": "Salon updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete Salon Route
@app.route('/salon/<id>', methods=['DELETE'])
@jwt_required()
def delete_salon(id):
    try:
        salon_ref = db.collection('salons').document(id)
        salon_ref.delete()
        return jsonify({"message": "Salon deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get All Salons (Paginated) Route
@app.route('/salons', methods=['GET'])
@jwt_required()
def get_all_salons():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        salons_ref = db.collection('salons').limit(per_page).offset((page - 1) * per_page).stream()
        salons = [salon.to_dict() for salon in salons_ref]

        return jsonify(salons), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create Service Route
@app.route('/service', methods=['POST'])
@jwt_required()
def create_service():
    try:
        data = request.json
        service_data = {
            'name': data['name'],
            'duration': data['duration'],
            'price': data['price'],
            'salon_id': data['salon_id'],
            'created_at': datetime.utcnow()
        }
        db.collection('services').add(service_data)
        return jsonify(service_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create Appointment Route
@app.route('/appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    try:
        data = request.json
        appointment_data = {
            'date_time': data['date_time'],
            'service_id': data['service_id'],
            'client_name': data['client_name'],
            'client_phone': data['client_phone'],
            'created_at': datetime.utcnow()
        }
        db.collection('appointments').add(appointment_data)
        return jsonify(appointment_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Available Slots Route
@app.route('/available_slots', methods=['GET'])
@jwt_required()
def get_available_slots():
    try:
        salon_id = request.args.get('salon_id', type=str)
        service_id = request.args.get('service_id', type=str)
        date = request.args.get('date', type=str)

        if not all([salon_id, service_id, date]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Parse date
        date = datetime.strptime(date, '%Y-%m-%d').date()

        # Get the service document from Firestore
        service_ref = db.collection('services').document(service_id).get()
        if not service_ref.exists:
            return jsonify({"error": "Service not found"}), 404
        service = service_ref.to_dict()

        # Fetch appointments for the given day
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        
        appointments_ref = db.collection('appointments').where('service_id', '==', service_id).where(
            'date_time', '>=', start_of_day).where('date_time', '<=', end_of_day).stream()
        
        appointments = [appointment.to_dict() for appointment in appointments_ref]

        # Define working hours
        working_start = datetime.combine(date, datetime.strptime("09:00", "%H:%M").time())
        working_end = datetime.combine(date, datetime.strptime("17:00", "%H:%M").time())

        # Calculate available slots
        all_slots = []
        current_slot = working_start
        while current_slot + timedelta(minutes=service['duration']) <= working_end:
            all_slots.append(current_slot)
            current_slot += timedelta(minutes=30)

        # Filter out occupied slots
        available_slots = [slot for slot in all_slots if not any(
            datetime.strptime(app['date_time'], "%Y-%m-%dT%H:%M:%S") <= slot <
            datetime.strptime(app['date_time'], "%Y-%m-%dT%H:%M:%S") + timedelta(minutes=service['duration'])
            for app in appointments
        )]

        return jsonify([slot.isoformat() for slot in available_slots])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
