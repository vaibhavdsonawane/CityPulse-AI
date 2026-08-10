import os
import sys

# Ensure parent directory is in Python path for Flask app imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Department
from werkzeug.security import generate_password_hash

app = create_app()

def reset_and_setup_database():
    print("Resetting database to sync with latest app/models.py schema...")
    
    with app.app_context():
        db.drop_all()
        print("Dropped stale database tables.")
        
        db.create_all()
        print("Created fresh database schema matching app/models.py!")
        
        admin_pwd = generate_password_hash("Admin@123!", method='scrypt')
        admin_user = User(
            name="System Administrator",
            email="admin@citypulse.gov",
            password_hash=admin_pwd,
            role="admin"
        )
        db.session.add(admin_user)
        
        citizen_pwd = generate_password_hash("Citizen@123", method='scrypt')
        citizen_user = User(
            name="Aarav Patil",
            email="aarav.patil@example.com",
            password_hash=citizen_pwd,
            role="citizen"
        )
        db.session.add(citizen_user)

        departments = [
            {"name": "Roads & Infrastructure", "email": "roads@nashik.gov.in", "phone": "0253-2222221"},
            {"name": "Sanitation & Waste Management", "email": "sanitation@nashik.gov.in", "phone": "0253-2222222"},
            {"name": "Water Supply & Sewerage", "email": "water@nashik.gov.in", "phone": "0253-2222223"},
            {"name": "Parks & Forestry", "email": "parks@nashik.gov.in", "phone": "0253-2222224"},
            {"name": "Electrical & Public Lighting", "email": "electrical@nashik.gov.in", "phone": "0253-2222225"}
        ]

        for dept_info in departments:
            dept = Department(
                name=dept_info["name"],
                contact_email=dept_info["email"],
                contact_phone=dept_info["phone"]
            )
            db.session.add(dept)

        db.session.commit()
        print("Database successfully initialized with fresh accounts & departments!")

if __name__ == '__main__':
    reset_and_setup_database()