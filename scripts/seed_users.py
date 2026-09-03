import os
import sys
import random
import string
from datetime import datetime, timedelta

# Ensure parent directory is in Python path for Flask app imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

# =====================================================================
# EXTENSIVE DATA POOLS (INDIAN NAMES, SURNAMES, TOWNS & PASSWORDS)
# =====================================================================

INDIAN_FIRST_NAMES = [
    "Aarav", "Ananya", "Rohan", "Priya", "Aditya", "Sneha", "Vikram", "Neha", "Rahul", "Pooja",
    "Siddharth", "Kavya", "Arjun", "Riya", "Karan", "Ishita", "Dev", "Anushka", "Yash", "Tanvi",
    "Akash", "Meera", "Varun", "Shruti", "Manish", "Divya", "Gaurav", "Sanya", "Rajesh", "Prerna",
    "Alok", "Simran", "Deepak", "Aishwarya", "Kunal", "Rachna", "Pranav", "Nisha", "Sameer", "Swati",
    "Nikhil", "Shreya", "Abhishek", "Sonam", "Vivek", "Payal", "Tushar", "Preeti", "Saurabh", "Monika",
    "Amit", "Ritu", "Sanjay", "Anjali", "Vijay", "Aarti", "Pankaj", "Komal", "Suresh", "Bhavna",
    "Ramesh", "Deepika", "Dinesh", "Kavita", "Nitin", "Sunita", "Manoj", "Anita", "Ashok", "Geeta",
    "Vikas", "Seema", "Rakesh", "Rekha", "Sunil", "Poonam", "Anil", "Sangeeta", "MOHAN", "Sudha",
    "Harish", "Usha", "Vinod", "Asha", "Satish", "Lata", "Naresh", "Manju", "Ganesh", "Pushpa",
    "Kishore", "Saroj", "Jitendra", "Sharda", "Dharmendra", "Kiran", "Lalit", "Maya", "Mukesh", "Renu",
    "Pawan", "Vimla", "Subhash", "Sushma", "Tarun", "Mamta", "Bhagwan", "Kusum", "Chander", "Kamlesh",
    "Gopal", "Shakuntala", "Hemant", "Santosh", "Mahendra", "Bimla", "Kailash", "Sheela", "Rajendra", "Vidya",
    "Narendra", "Rami", "Surendra", "Savitri", "Joginder", "Parvati", "Omprakash", "Lalita", "Purushottam", "Basanti",
    "Brijesh", "Tara", "Girraj", "Nirmala", "Ramkant", "Devki", "Shivkumar", "Munni", "Radheshyam", "Shanti",
    "Ghanshyam", "Ganga", "Shri", "Jamuna", "Kishan", "Kaushalya", "Balkishan", "Saraswati", "Bhairav", "Durga",
    "Kalyan", "Gauri", "Shankar", "Lakshmi", "Bholanath", "Saraswati", "Bhudev", "Champa", "Charandas", "Champa",
    "Chintamani", "Chameli", "Dayaram", "Daya", "Deenabandhu", "Draupadi", "Dwarika", "Gayatri", "Gopiram", "Gopika",
    "Govardhan", "Indira", "Hariom", "Indumati", "Harkishan", "Janki", "Ishwar", "Kalavati", "Jagdish", "Kanti",
    "Jaswant", "Kastoori", "Kanhaiya", "Kausalya", "Kedarnath", "Kiranbala", "Kripashankar", "Kusumkani", "Laxman", "Leelavati",
    "Madanmohan", "Madhuri", "Mahadev", "Maina", "Mahavir", "Malti", "Manmohan", "Manorama", "Mathuradas", "Mohini"
]

INDIAN_LAST_NAMES = [
    "Sharma", "Verma", "Patil", "Deshmukh", "Kulkarni", "Gupta", "Singh", "Joshi", "Mehta", "Rao",
    "Nair", "Iyer", "Reddy", "Chowdhury", "Banerjee", "Chatterjee", "Mishra", "Pandey", "Pawar", "Shinde",
    "Gaikwad", "Bhosale", "Kadam", "Jadhav", "More", "Agarwal", "Bhatia", "Kapoor", "Malhotra", "Saxena",
    "Tiwari", "Dubey", "Tripathi", "Shukla", "Awasthi", "Dwivedi", "Chaubey", "Pathak", "Pandya", "Vyas",
    "Bhatt", "Dave", "Jani", "Thakar", "Trivedi", "Yagnik", "Shastri", "Vora", "Parikh", "Shah", "Patel",
    "Desai", "Amin", "Chaudhari", "Prajapati", "Solanki", "Chavda", "Rathod", "Parmar", "Makwana", "Vaghela",
    "Jha", "Thakur", "Sinha", "Srivastava", "Prasad", "Verma", "Yadav", "Mandal", "Paswan", "Mahto",
    "Das", "Dutta", "Sarkar", "Roy", "Ghosh", "Bhowmick", "Mitra", "Bose", "Pal", "Guha",
    "Sen", "Chakraborty", "Nandi", "Mukherjee", "Ray", "Majumdar", "Adhikari", "Biswas", "Saha", "Barman",
    "Kaur", "Grewal", "Dhillon", "Sidhu", "Gill", "Sandhu", "Brar", "Aulakh", "Bains", "Chahal",
    "Deol", "Ghosal", "Johal", "Kahlon", "Khaira", "Lalli", "Mann", "Nijjar", "Pannu", "Randhawa",
    "Saini", "Shergill", "Sohi", "Toor", "Uppal", "Virk", "Warraich", "Bhat", "Dhar", "Raina",
    "Kaul", "Kak", "Mattoo", "Ganjoo", "Pandita", "Razdan", "Kilam", "Tiku", "Zutshi", "Thussu",
    "Bhan", "Kachroo", "Trisal", "Fotedar", "Langoo", "Suchu", "Khosa", "Waza", "Saraf", "Karu"
]

EMAIL_DOMAINS = [
    "example.com", "citypulse.in", "nashik.gov.in", "citizen.org.in", 
    "urban.co.in", "civicmail.in", "smartcity.in", "indiamail.com"
]

# Prefixes and suffixes for randomized password building
PWD_PREFIXES = ["City", "Pulse", "Citizen", "Nashik", "Smart", "Civic", "Urban", "Safe", "Metro", "Clean"]
PWD_MID = ["#", "@", "$", "!", "%", "&", "*"]
PWD_SUFFIXES = ["2026", "123", "999", "777", "888", "2025", "4321", "101", "365", "007"]

def generate_random_password():
    """Generates a unique, realistic password for each injected user."""
    prefix = random.choice(PWD_PREFIXES)
    symbol = random.choice(PWD_MID)
    suffix = random.choice(PWD_SUFFIXES)
    rand_char = random.choice(string.ascii_uppercase)
    return f"{prefix}{symbol}{rand_char}{suffix}"

# =====================================================================
# SEEDING EXECUTION ENGINE
# =====================================================================

def inject_150_users():
    """
    Creates and inserts 150 unique citizen profiles into the SQLite database.
    Prints the complete credentials log (email & password) at the end.
    """
    print("\n" + "="*70)
    print("🚀 CITYPULSE AI - DATABASE USER SEEDING ENGINE")
    print("="*70)
    print("📌 Task: Injecting 150 unique Indian Citizen accounts into database...")

    credentials_log = []

    with app.app_context():
        # Ensure database tables exist
        db.create_all()

        existing_emails = set(row[0] for row in db.session.query(User.email).all())
        users_to_commit = []

        generated_count = 0
        used_combinations = set()

        while generated_count < 150:
            first = random.choice(INDIAN_FIRST_NAMES)
            last = random.choice(INDIAN_LAST_NAMES)
            
            full_name = f"{first} {last}"
            combination_key = f"{first}_{last}_{generated_count}"

            if combination_key in used_combinations:
                continue
            used_combinations.add(combination_key)

            # Generate unique clean email
            clean_first = first.lower().replace(" ", "")
            clean_last = last.lower().replace(" ", "")
            domain = random.choice(EMAIL_DOMAINS)
            
            email = f"{clean_first}.{clean_last}{generated_count + 1}@{domain}"

            if email in existing_emails:
                continue
            existing_emails.add(email)

            # Generate random password
            plain_password = generate_random_password()
            password_hash = generate_password_hash(plain_password, method='scrypt')

            # Random creation timestamp within last 120 days
            random_days_ago = random.randint(1, 120)
            created_at = datetime.utcnow() - timedelta(days=random_days_ago)

            new_user = User(
                name=full_name,
                email=email,
                password_hash=password_hash,
                role='citizen',
                created_at=created_at
            )

            users_to_commit.append(new_user)
            credentials_log.append({
                'id': generated_count + 1,
                'name': full_name,
                'email': email,
                'password': plain_password
            })

            generated_count += 1

        # Bulk save users to database
        db.session.bulk_save_objects(users_to_commit)
        db.session.commit()

        print("\n" + "✅"*35)
        print(f" SUCCESS: Injected {len(users_to_commit)} Citizen Accounts into Database!")
        print("✅"*35 + "\n")

        # =====================================================================
        # PRINT COMPLETE INJECTED CREDENTIALS LOG (EMAIL & PASSWORDS)
        # =====================================================================
        print("="*80)
        print("📋 COMPLETE LOG OF INJECTED USER CREDENTIALS (150 ACCOUNTS)")
        print("="*80)
        print(f"{'NO.':<5} | {'FULL NAME':<24} | {'EMAIL ADDRESS':<36} | {'PASSWORD'}")
        print("-" * 80)

        for cred in credentials_log:
            print(f"{cred['id']:<5} | {cred['name']:<24} | {cred['email']:<36} | {cred['password']}")

        print("-" * 80)
        print("✨ Database injection complete! You can now log in with any of these credentials.")
        print("="*80 + "\n")

if __name__ == '__main__':
    inject_150_users()