import os
import sys
import random
from datetime import datetime, timedelta, timezone

# Ensure parent directory is in Python path for Flask app imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Complaint, Media, AIPrediction, ComplaintStatusHistory, Department, ComplaintAssignment

app = create_app()

# =====================================================================
# NASHIK LANDMARKS & GEOLOCATION COORDINATE POOL
# =====================================================================
NASHIK_LOCATIONS = [
    {"name": "Trimurti Chowk, CIDCO", "lat": 19.9723, "lng": 73.7621, "importance": "Arterial"},
    {"name": "College Road, Near RYK College", "lat": 20.0035, "lng": 73.7648, "importance": "Arterial"},
    {"name": "MG Road, Near CBS Bus Stand", "lat": 19.9975, "lng": 73.7898, "importance": "High Traffic"},
    {"name": "Gangapur Road, Near KTHM College", "lat": 20.0112, "lng": 73.7714, "importance": "School Zone"},
    {"name": "Satpur MIDC Industrial Area", "lat": 19.9884, "lng": 73.7291, "importance": "Industrial"},
    {"name": "Panchavati, Near Kalaram Temple", "lat": 20.0089, "lng": 73.7952, "importance": "Heritage Zone"},
    {"name": "Nashik Road Railway Station Area", "lat": 19.9542, "lng": 73.8311, "importance": "Transit Junction"},
    {"name": "Indira Nagar, Near Jogging Track", "lat": 19.9654, "lng": 73.7782, "importance": "Residential"},
    {"name": "Govind Nagar, Near City Center Mall", "lat": 19.9812, "lng": 73.7701, "importance": "Commercial Area"},
    {"name": "Pathardi Phata, Mumbai-Agra Highway", "lat": 19.9421, "lng": 73.7612, "importance": "Major Highway"},
    {"name": "Dwarka Circle Junction", "lat": 19.9892, "lng": 73.8011, "importance": "Major Highway"},
    {"name": "Untwadi, Near Apollo Hospital", "lat": 19.9845, "lng": 73.7689, "importance": "Hospital Junction"},
    {"name": "Ambad MIDC Industrial Zone", "lat": 19.9482, "lng": 73.7381, "importance": "Industrial Area"},
    {"name": "Mahatma Nagar Ground Area", "lat": 19.9981, "lng": 73.7542, "importance": "Residential"},
    {"name": "Adgaon Naka, Ozar Highway", "lat": 20.0312, "lng": 73.8341, "importance": "Major Highway"}
]

# =====================================================================
# REALISTIC COMPLAINT TEMPLATES WITH VARYING SEVERITY
# =====================================================================
COMPLAINT_TEMPLATES = [
    # CRITICAL SEVERITY (Scores: 85 - 98)
    {
        "category": "Pothole",
        "desc": "Massive 2-foot deep crater on the main arterial road right near the hospital entrance. Causing major traffic jams and severe risk of two-wheeler accidents during peak hours.",
        "severity": "Critical",
        "score_range": (85, 98),
        "cv_class": "pothole",
        "action": "Deploy emergency road repair crew within 12 hours. Issue traffic diversion advisory."
    },
    {
        "category": "Water Leakage",
        "desc": "Main underground supply pipeline burst near the main chowk. High-pressure clean drinking water flooding the road for 5 hours, causing severe asphalt erosion.",
        "severity": "Critical",
        "score_range": (85, 96),
        "cv_class": "water_leakage",
        "action": "Shut off local main valve immediately. Send emergency hydraulic repair team."
    },
    {
        "category": "Fallen Tree",
        "desc": "Large banyan tree collapsed across both lanes following monsoon storm winds. Entire transit road blocked, trapping vehicles and damaging overhead electrical wires.",
        "severity": "Critical",
        "score_range": (88, 97),
        "cv_class": "fallen_tree",
        "action": "Dispatch forestry chainsaw unit and power grid maintenance crew immediately."
    },

    # HIGH SEVERITY (Scores: 65 - 84)
    {
        "category": "Garbage",
        "desc": "Uncontrolled overflow from public garbage dump near local vegetable market. Blocking pedestrian pathway and emitting toxic odor for over 3 days.",
        "severity": "High",
        "score_range": (68, 84),
        "cv_class": "garbage_heap",
        "action": "Send heavy sanitation dumper truck and sanitize the surrounding market area."
    },
    {
        "category": "Streetlight",
        "desc": "Complete dark corridor along 500 meters of the highway junction due to damaged transformer box. Poses severe safety risk to commuters at night.",
        "severity": "High",
        "score_range": (65, 82),
        "cv_class": "broken_streetlight",
        "action": "Schedule electrical team inspection and replace damaged transformer fuse box."
    },
    {
        "category": "Pothole",
        "desc": "Cluster of multiple deep potholes causing vehicle slowdowns near school bus drop zone.",
        "severity": "High",
        "score_range": (66, 80),
        "cv_class": "pothole",
        "action": "Queue hot-mix asphalt patching team for priority repair within 24-48 hours."
    },

    # MEDIUM SEVERITY (Scores: 40 - 64)
    {
        "category": "Streetlight",
        "desc": "Single streetlight pole flickering continuously near residential lane entrance.",
        "severity": "Medium",
        "score_range": (42, 60),
        "cv_class": "broken_streetlight",
        "action": "Routine inspection scheduled. Replace LED bulb fixture within 3-5 days."
    },
    {
        "category": "Garbage",
        "desc": "Plastic litter and uncollected dry waste accumulated along park sidewalk.",
        "severity": "Medium",
        "score_range": (40, 58),
        "cv_class": "garbage_heap",
        "action": "Notify ward sanitation worker for routine morning sweep and clearance."
    },
    {
        "category": "Water Leakage",
        "desc": "Minor slow leak from commercial meter line creating small puddle on side lane.",
        "severity": "Medium",
        "score_range": (45, 62),
        "cv_class": "water_leakage",
        "action": "Issue work order to municipal plumbing unit for routine pipeline sealing."
    },

    # LOW SEVERITY (Scores: 15 - 39)
    {
        "category": "Fallen Tree",
        "desc": "Overhanging dry tree branch blocking visibility of local street signpost.",
        "severity": "Low",
        "score_range": (18, 38),
        "cv_class": "fallen_tree",
        "action": "Add to weekly tree trimming schedule for neighborhood parks department."
    },
    {
        "category": "Garbage",
        "desc": "Small pile of garden trimmings and leaf litter left on residential curb.",
        "severity": "Low",
        "score_range": (15, 35),
        "cv_class": "garbage_heap",
        "action": "Clear during standard weekly organic waste collection route."
    }
]

STATUS_CHOICES = ["Pending Dispatch", "Assigned", "Under Investigation", "Work Started", "Resolved"]

def seed_nashik_complaints():
    """Generates 75+ complaints randomly distributed across Nashik using injected citizen accounts."""
    print("\n" + "="*70)
    print("🏙️ CITYPULSE AI - NASHIK COMPLAINT INJECTION ENGINE")
    print("="*70)

    with app.app_context():
        # Retrieve all available citizen users
        citizens = User.query.filter_by(role='citizen').all()
        if not citizens:
            print("❌ No citizen users found! Please run 'python scripts/seed_users.py' first.")
            return

        admin_user = User.query.filter_by(role='admin').first()
        admin_id = admin_user.id if admin_user else 1

        departments = Department.query.all()
        dept_map = {d.name: d.id for d in departments}

        print(f"👥 Found {len(citizens)} active citizens in database. Generating 75 Nashik complaints...")

        complaints_created = 0
        now = datetime.now(timezone.utc)

        for i in range(75):
            citizen = random.choice(citizens)
            loc = random.choice(NASHIK_LOCATIONS)
            template = random.choice(COMPLAINT_TEMPLATES)

            lat_jitter = random.uniform(-0.003, 0.003)
            lng_jitter = random.uniform(-0.003, 0.003)
            final_lat = round(loc["lat"] + lat_jitter, 6)
            final_lng = round(loc["lng"] + lng_jitter, 6)

            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            reported_time = now - timedelta(days=days_ago, hours=hours_ago)

            status = random.choice(STATUS_CHOICES)

            # Create Base Complaint (removed unmapped rating / feedback_text arguments)
            new_complaint = Complaint(
                user_id=citizen.id,
                category=template["category"],
                description=f"{template['desc']} (Location: {loc['name']})",
                latitude=final_lat,
                longitude=final_lng,
                status=status,
                reported_at=reported_time
            )
            db.session.add(new_complaint)
            db.session.flush()

            cv_conf = round(random.uniform(0.72, 0.98), 3)
            dummy_filename = f"sample_{template['cv_class']}_{random.randint(100, 999)}.jpg"
            
            media_rec = Media(
                complaint_id=new_complaint.id,
                file_path=dummy_filename,
                cv_detected_class=template["cv_class"],
                cv_confidence=cv_conf,
                cv_bounding_box="[45, 120, 310, 280]"
            )
            db.session.add(media_rec)

            priority_score = random.randint(template["score_range"][0], template["score_range"][1])
            ai_pred = AIPrediction(
                complaint_id=new_complaint.id,
                severity_level=template["severity"],
                priority_score=float(priority_score),
                recommended_action=template["action"],
                human_verified=True,
                is_correct=True
            )
            db.session.add(ai_pred)

            history_log = ComplaintStatusHistory(
                complaint_id=new_complaint.id,
                status="Pending Dispatch",
                notes=f"Report logged by citizen {citizen.name}. AI Priority: {priority_score}/100.",
                changed_by_id=citizen.id,
                changed_at=reported_time
            )
            db.session.add(history_log)

            if status in ['Assigned', 'Under Investigation', 'Work Started', 'Resolved'] and departments:
                target_dept_id = departments[0].id
                if "Road" in template["category"] or "Pothole" in template["category"]:
                    target_dept_id = dept_map.get("Roads & Infrastructure", target_dept_id)
                elif "Garbage" in template["category"]:
                    target_dept_id = dept_map.get("Sanitation & Waste Management", target_dept_id)
                elif "Water" in template["category"]:
                    target_dept_id = dept_map.get("Water Supply & Sewerage", target_dept_id)
                elif "Tree" in template["category"]:
                    target_dept_id = dept_map.get("Parks & Forestry", target_dept_id)
                elif "Streetlight" in template["category"]:
                    target_dept_id = dept_map.get("Electrical & Public Lighting", target_dept_id)

                assignment = ComplaintAssignment(
                    complaint_id=new_complaint.id,
                    department_id=target_dept_id,
                    assigned_by_id=admin_id,
                    assigned_at=reported_time + timedelta(hours=1)
                )
                db.session.add(assignment)

                status_history_log = ComplaintStatusHistory(
                    complaint_id=new_complaint.id,
                    status=status,
                    notes=f"Advanced to '{status}' state by Command Center Operator.",
                    changed_by_id=admin_id,
                    changed_at=reported_time + timedelta(hours=random.randint(2, 12))
                )
                db.session.add(status_history_log)

            complaints_created += 1

        db.session.commit()

        print("="*70)
        print(f"✅ SUCCESSFULLY INJECTED {complaints_created} COMPLAINTS ACROSS NASHIK!")
        print("="*70)
        print("📊 SUMMARY OF NASHIK SEEDED DATA:")
        print(f"   • Total Active Complaints Generated : {complaints_created}")
        print(f"   • Geographic Distribution Scope      : Nashik Wards, MIDC, Highways & Chowks")
        print(f"   • Severity Range Distribution        : Low (15 pts) to Critical (98 pts)")
        print("="*70 + "\n")

if __name__ == '__main__':
    seed_nashik_complaints()