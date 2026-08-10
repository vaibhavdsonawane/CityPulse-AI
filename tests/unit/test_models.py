from app.models import User
from app import db

def test_new_user(app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, role, and password hashing fields are defined correctly
    """
    with app.app_context():
        user = User(full_name="Unit Test User", email="unit@test.com", phone_number="1112223333")
        user.set_password("SecurePass123")
        
        # Save to the in-memory test database to trigger SQLAlchemy defaults
        db.session.add(user)
        db.session.flush() 
        
        assert user.email == "unit@test.com"
        assert user.role == "citizen" # This will now successfully equal 'citizen'
        assert user.password_hash != "SecurePass123"
        assert user.check_password("SecurePass123") is True
        assert user.check_password("WrongPassword") is False