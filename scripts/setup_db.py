import os
import sys

# Ensure parent directory is in Python path for Flask app imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Department, Complaint, Media, AIPrediction, ComplaintAssignment, ComplaintStatusHistory
from werkzeug.security import generate_password_hash

app = create_app()

def initialize_database():
    print("\n" + "=" * 70)
    print("🛠️  CITYPULSE AI - DATABASE INITIALIZATION & SCHEMA SETUP")
    print("=" * 70)
    
    with app.app_context():
        # Create all database tables matching app/models.py
        db.create_all()
        print("✨ Database tables created/verified successfully!")

        # Seed Default Admin Account if missing
        admin_email = "admin@citypulse.gov"
        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            admin_pwd = generate_password_hash("Admin@123!", method='scrypt')
            admin_user = User(
                name="System Administrator",
                email=admin_email,
                password_hash=admin_pwd,
                role="admin"
            )
            db.session.add(admin_user)
            print("👤 Seeded default Admin user: admin@citypulse.gov")

        # Seed Default Citizen Account if missing
        citizen_email = "aarav.patil@example.com"
        existing_citizen = User.query.filter_by(email=citizen_email).first()

        if not existing_citizen:
            citizen_pwd = generate_password_hash("Citizen@123", method='scrypt')
            citizen_user = User(
                name="Aarav Patil",
                email=citizen_email,
                password_hash=citizen_pwd,
                role="citizen"
            )
            db.session.add(citizen_user)
            print("👤 Seeded default Citizen user: aarav.patil@example.com")

        # Seed Municipal Departments if missing
        departments = [
            {"name": "Roads & Infrastructure", "email": "roads@nashik.gov.in", "phone": "0253-2222221"},
            {"name": "Sanitation & Waste Management", "email": "sanitation@nashik.gov.in", "phone": "0253-2222222"},
            {"name": "Water Supply & Sewerage", "email": "water@nashik.gov.in", "phone": "0253-2222223"},
            {"name": "Parks & Forestry", "email": "parks@nashik.gov.in", "phone": "0253-2222224"},
            {"name": "Electrical & Public Lighting", "email": "electrical@nashik.gov.in", "phone": "0253-2222225"}
        ]

        for dept_info in departments:
            dept_exists = Department.query.filter_by(name=dept_info["name"]).first()
            if not dept_exists:
                dept = Department(
                    name=dept_info["name"],
                    contact_email=dept_info["email"],
                    contact_phone=dept_info["phone"]
                )
                db.session.add(dept)

        db.session.commit()
        print("🏢 Municipal departments verified/seeded successfully!")

        print("\n" + "=" * 70)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 70)
        print("🔑 Admin Credentials:   admin@citypulse.gov     | Password: Admin@123!")
        print("🔑 Citizen Credentials: aarav.patil@example.com | Password: Citizen@123")
        print("=" * 70 + "\n")

if __name__ == '__main__':
    initialize_database()