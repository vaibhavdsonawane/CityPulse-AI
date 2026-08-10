from app.models import User
from app import db

def test_homepage_redirects_to_login(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that it redirects to the login page
    """
    response = client.get('/')
    assert response.status_code == 302 # 302 is the HTTP code for a redirect
    assert b'/auth/login' in response.data

def test_valid_user_registration(client, app):
    """
    GIVEN a Flask application
    WHEN a new user posts valid data to '/auth/register'
    THEN check that the user is saved in the database
    """
    response = client.post('/auth/register', data={
        'full_name': 'Integration Test',
        'email': 'integration@test.com',
        'phone': '9998887777',
        'password': 'TestPassword!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    # Verify the user actually made it into the test database
    with app.app_context():
        user = User.query.filter_by(email='integration@test.com').first()
        assert user is not None
        assert user.full_name == 'Integration Test'