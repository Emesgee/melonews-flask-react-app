import pytest
from backend.models import db, User  # Absolute import
from backend.app import app  # Absolute import

@pytest.fixture
def client():
    """Sets up a test client for Flask application with a clean database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables before each test
        yield client
        # Drop all tables after each test to ensure a clean state
        #with app.app_context():
        #    db.drop_all()

# Test Registration
def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/register', json={
        'name': 'TestUser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully!'


# Test Login
def test_login_user(client):
    """Test user login"""
    client.post('/api/register', json={
        'name': 'TestUser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()


# Test Profile Access
def test_get_profile(client):
    """Test accessing user profile"""
    client.post('/api/register', json={
        'name': 'TestUser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    login_response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']

    response = client.get('/api/profile', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    assert response.get_json()['name'] == 'TestUser'
