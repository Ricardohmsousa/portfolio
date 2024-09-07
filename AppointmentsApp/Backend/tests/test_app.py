import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from flask_jwt_extended import create_access_token
from app import app

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def valid_token(test_client):
    # Mock a valid user ID
    user_id = 'test-user-id'
    token = create_access_token(identity=user_id)
    return token

# Mock Firebase Auth
@pytest.fixture(autouse=True)
def mock_firebase():
    with patch('app.auth') as mock_auth:
        mock_auth.create_user = MagicMock(return_value=MagicMock(uid='test-user-id'))
        mock_auth.sign_in_with_email_and_password = MagicMock(return_value={'localId': 'test-user-id'})
        yield mock_auth


# Mock Firestore
@pytest.fixture(autouse=True)
def mock_firestore():
    with patch('app.db') as mock_db:
        mock_db.collection = MagicMock()
        mock_db.collection.return_value.document.return_value.get.return_value.exists = True
        mock_db.collection.return_value.document.return_value.get.return_value.to_dict.return_value = {
            'name': 'My Salon',
            'address': '123 Salon St',
            'phone': '123-456-7890',
            'created_at': datetime.utcnow()
        }
        yield mock_db

def test_register(test_client):
    response = test_client.post('/register', json={
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'username': 'newuser'
    })
    assert response.status_code == 201
    assert 'user_id' in response.json

def test_login(test_client):
    response = test_client.post('/login', json={
        'email': 'newuser@example.com',
        'password': 'newpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_create_salon(test_client, valid_token):
    with patch('app.db.collection.return_value.add') as mock_add:
        response = test_client.post('/salon', json={
            'name': 'My Salon',
            'address': '123 Salon St',
            'phone': '123-456-7890'
        }, headers={'Authorization': f'Bearer {valid_token}'})
        assert response.status_code == 201
        assert response.json['name'] == 'My Salon'
        args, _ = mock_add.call_args
        assert 'created_at' in args[0]
        assert isinstance(args[0]['created_at'], datetime)


def test_get_salon(test_client, valid_token):
    response = test_client.get('/salon/test-salon-id', headers={'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'My Salon'

def test_update_salon(test_client, valid_token):
    with patch('app.db.collection.return_value.document.return_value.update') as mock_update:
        response = test_client.put('/salon/test-salon-id', json={
            'name': 'Updated Salon',
            'address': '456 New St',
            'phone': '987-654-3210'
        }, headers={'Authorization': f'Bearer {valid_token}'})
        assert response.status_code == 200
        assert response.json['message'] == 'Salon updated successfully'
        args, _ = mock_update.call_args
        assert 'updated_at' in args[0]
        assert isinstance(args[0]['updated_at'], datetime)


def test_delete_salon(test_client, valid_token):
    with patch('app.db.collection.return_value.document.return_value.delete') as mock_delete:
        response = test_client.delete('/salon/test-salon-id', headers={'Authorization': f'Bearer {valid_token}'})
        assert response.status_code == 200
        assert response.json['message'] == 'Salon deleted successfully'
        mock_delete.assert_called_once()

def test_get_all_salons(test_client, valid_token):
    with patch('app.db.collection.return_value.stream') as mock_stream:
        mock_stream.return_value = [MagicMock(to_dict=MagicMock(return_value={
            'name': 'My Salon',
            'address': '123 Salon St',
            'phone': '123-456-7890'
        }))]
        response = test_client.get('/salons', headers={'Authorization': f'Bearer {valid_token}'})
        assert response.status_code == 200
        assert isinstance(response.json, list)
def test_create_service(test_client, valid_token):
    with patch('app.db.collection.return_value.add') as mock_add:
        response = test_client.post('/service', json={
            'name': 'Haircut',
            'duration': 30,
            'price': 20,
            'salon_id': 'test-salon-id'
        }, headers={'Authorization': f'Bearer {valid_token}'})
        assert response.status_code == 201
        assert response.json['name'] == 'Haircut'
        args, _ = mock_add.call_args
        assert 'created_at' in args[0]
        assert isinstance(args[0]['created_at'], datetime)
def test_create_appointment(test_client, valid_token):



    with patch('app.db.collection.return_value.add') as mock_add:
        response = test_client.post('/appointment', json={
            'date_time': datetime.utcnow().isoformat(),
            'service_id': 'test-service-id',
            'client_name': 'John Doe',
            'client_phone': '123-456-7890'
        }, headers={'Authorization': f'Bearer {valid_token}'})
        assert response.status_code == 201
        assert response.json['client_name'] == 'John Doe'
        args, _ = mock_add.call_args
        assert 'created_at' in args[0]
        assert isinstance(args[0]['created_at'], datetime)


from unittest.mock import patch
from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pytest

def test_get_available_slots(test_client, valid_token):
    # Mock Firestore collection access
    with patch('app.db.collection') as mock_collection:
        # Mock the service document
        mock_service_ref = MagicMock()
        mock_service_ref.exists = True
        mock_service_ref.to_dict.return_value = {'duration': 30}  # Example duration
        mock_collection.return_value.document.return_value.get.return_value = mock_service_ref

        # Mock appointments query
        mock_appointments_ref = MagicMock()
        mock_appointments_ref.stream.return_value = []  # Empty list of appointments
        mock_collection.return_value.where.return_value.where.return_value.where.return_value = mock_appointments_ref

        response = test_client.get('/available_slots', query_string={
            'salon_id': 'test-salon-id',
            'service_id': 'test-service-id',
            'date': datetime.utcnow().date().isoformat()
        }, headers={'Authorization': f'Bearer {valid_token}'})

        assert response.status_code == 200
        assert isinstance(response.json, list)
        # Optional: Check response content based on the mock data
        assert response.json  # Assuming it should return a list of available slots

if __name__ == '__main__':
    pytest.main()
