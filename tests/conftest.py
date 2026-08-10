import pytest
from app import create_app, db
from app.models import User, Department

@pytest.fixture
def app():
    """Creates a fresh Flask app with an in-memory SQLite database for testing."""
    # We create a specific testing configuration dictionary dynamically
    app = create_app('development')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False, # Disable CSRF for testing forms
    })

    # Push an application context to bind the SQLAlchemy db object
    with app.app_context():
        db.create_all()
        
        # Seed basic required data
        dept = Department(name="Test Dept", contact_email="test@dept.com", contact_phone="123")
        db.session.add(dept)
        db.session.commit()
        
        yield app
        
        # Clean up after the test is done
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app to simulate web requests."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()