import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///salon.db')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Change this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
migrate = Migrate(app, db)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    price = db.Column(db.Float, nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)

# Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)

class SalonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Salon
        load_instance = True

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = True

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True

user_schema = UserSchema()
salon_schema = SalonSchema()
service_schema = ServiceSchema()
appointment_schema = AppointmentSchema()

# Routes
@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400   
        user = User(username=data['username'], password=generate_password_hash(data['password']))
        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/salon', methods=['POST'])
@jwt_required()
def create_salon():
    try:
        data = request.json
        salon = Salon(name=data['name'], address=data['address'], phone=data['phone'])
        db.session.add(salon)
        db.session.commit()
        return jsonify(salon_schema.dump(salon)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/salon/<int:id>', methods=['GET'])
@jwt_required()
def get_salon(id):
    try:
        salon = Salon.query.get_or_404(id)
        return jsonify(salon_schema.dump(salon))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/salon/<int:id>', methods=['PUT'])
@jwt_required()
def update_salon(id):
    try:
        salon = Salon.query.get_or_404(id)
        data = request.json
        salon.name = data.get('name', salon.name)
        salon.address = data.get('address', salon.address)
        salon.phone = data.get('phone', salon.phone)
        db.session.commit()
        return jsonify(salon_schema.dump(salon))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/salon/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_salon(id):
    try:
        salon = Salon.query.get_or_404(id)
        db.session.delete(salon)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/salons', methods=['GET'])
@jwt_required()
def get_salons():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        salons = Salon.query.paginate(page=page, per_page=per_page)
        return jsonify({
            'items': salon_schema.dump(salons.items, many=True),
            'total': salons.total,
            'pages': salons.pages,
            'page': page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/service', methods=['POST'])
@jwt_required()
def create_service():
    try:
        data = request.json
        service = Service(name=data['name'], duration=data['duration'], price=data['price'], salon_id=data['salon_id'])
        db.session.add(service)
        db.session.commit()
        return jsonify(service_schema.dump(service)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    try:
        data = request.json
        appointment = Appointment(
            date_time=datetime.fromisoformat(data['date_time']),
            service_id=data['service_id'],
            client_name=data['client_name'],
            client_phone=data['client_phone']
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify(appointment_schema.dump(appointment)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/available_slots', methods=['GET'])
@jwt_required()
def get_available_slots():
    try:
        salon_id = request.args.get('salon_id', type=int)
        service_id = request.args.get('service_id', type=int)
        date = request.args.get('date', type=str)

        if not all([salon_id, service_id, date]):
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        service = Service.query.get_or_404(service_id)
        
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        appointments = Appointment.query.filter(
            Appointment.service_id == service_id,
            Appointment.date_time.between(start_of_day, end_of_day)
        ).all()

        working_start = datetime.combine(date, datetime.strptime("09:00", "%H:%M").time())
        working_end = datetime.combine(date, datetime.strptime("17:00", "%H:%M").time())

        all_slots = []
        current_slot = working_start
        while current_slot + timedelta(minutes=service.duration) <= working_end:
            all_slots.append(current_slot)
            current_slot += timedelta(minutes=30)

        available_slots = [slot for slot in all_slots if not any(
            appointment.date_time <= slot < appointment.date_time + timedelta(minutes=service.duration)
            for appointment in appointments
        )]

        return jsonify([slot.isoformat() for slot in available_slots])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # HTTP is the default; no need to specify anything for HTTP.
