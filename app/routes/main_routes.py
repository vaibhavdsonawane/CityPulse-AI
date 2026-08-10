from flask import Blueprint, render_template
from sqlalchemy import func
from app.models import Complaint, User, AIPrediction
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # 📊 Live City Statistics Database Query
    total_reported = Complaint.query.filter(Complaint.parent_id == None).count()
    total_resolved = Complaint.query.filter(Complaint.parent_id == None, Complaint.status == 'Resolved').count()
    total_pending = Complaint.query.filter(
        Complaint.parent_id == None, 
        Complaint.status.in_(['Pending Dispatch', 'Needs Manual Review', 'Assigned', 'Under Investigation', 'Work Started'])
    ).count()
    
    high_priority = db.session.query(Complaint).join(AIPrediction).filter(
        Complaint.parent_id == None,
        (AIPrediction.priority_score >= 85) | (AIPrediction.severity_level == 'Critical')
    ).count()

    active_citizens = User.query.filter_by(role='citizen').count()

    # Dynamic Metric Payload
    stats = {
        'total_reported': total_reported,
        'total_resolved': total_resolved,
        'total_pending': total_pending,
        'high_priority': high_priority,
        'active_citizens': active_citizens,
        'avg_response_time': '4.8 hrs'
    }

    return render_template('index.html', stats=stats)