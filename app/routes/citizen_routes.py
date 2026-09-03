import os
import random
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.models import Complaint, Media, AIPrediction, ComplaintStatusHistory, ComplaintAssignment, Department
from app import db
from app.utils import calculate_distance

# AI Controllers
from app.controllers.cv_service import vision_ai
from app.controllers.ml_service import severity_ai
from app.controllers.nlp_service import nlp_ai

citizen_bp = Blueprint('citizen', __name__, url_prefix='/citizen')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_lifecycle_steps(complaint):
    status = complaint.status
    has_ai = complaint.ai_prediction is not None
    is_assigned = status in ['Assigned', 'Under Investigation', 'Work Started', 'Resolved']
    is_investigating = status in ['Under Investigation', 'Work Started', 'Resolved']
    is_work_started = status in ['Work Started', 'Resolved']
    is_resolved = status == 'Resolved'

    steps = [
        {'title': 'Submitted', 'desc': f'Reported on {complaint.reported_at.strftime("%b %d, %H:%M")}', 'state': 'completed'},
        {'title': 'AI Analyzed', 'desc': f'CV Conf: {int(complaint.media.cv_confidence * 100)}%' if complaint.media else 'Automated Scoring', 'state': 'completed' if has_ai else 'active'},
        {'title': 'Assigned to Department', 'desc': complaint.assignment.department.name if (complaint.assignment and complaint.assignment.department) else 'Queued for Dispatch', 'state': 'completed' if is_assigned else ('active' if status == 'Pending Dispatch' else 'pending')},
        {'title': 'Under Investigation', 'desc': 'Field Inspection Team', 'state': 'completed' if is_investigating else ('active' if status == 'Assigned' else 'pending')},
        {'title': 'Work Started', 'desc': 'On-Site Maintenance', 'state': 'completed' if is_work_started else ('active' if status == 'Under Investigation' else 'pending')},
        {'title': 'Resolved', 'desc': 'Issue Fully Fixed', 'state': 'completed' if is_resolved else ('active' if status == 'Work Started' else 'pending')}
    ]
    return steps

@citizen_bp.route('/dashboard')
@login_required
def dashboard():
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.reported_at.desc()).all()
    
    total_submitted = len(complaints)
    total_resolved = sum(1 for c in complaints if c.status == 'Resolved')
    
    total_verified = sum(
        1 for c in complaints 
        if (c.media and c.media.cv_confidence >= 0.60) or (c.ai_prediction and c.ai_prediction.human_verified)
    )

    civic_points = (total_submitted * 20) + (total_verified * 50) + (total_resolved * 100)

    badges = [
        {'name': 'First Reporter', 'icon': '🥉', 'tier': 'Bronze', 'unlocked': total_submitted >= 1, 'desc': 'Submitted 1+ verified municipal report'},
        {'name': 'Active Citizen', 'icon': '🥈', 'tier': 'Silver', 'unlocked': total_verified >= 3, 'desc': 'Achieved 3+ AI-verified infrastructure reports'},
        {'name': 'Civic Champion', 'icon': '🥇', 'tier': 'Gold', 'unlocked': total_resolved >= 5 or civic_points >= 500, 'desc': 'Directly contributed to 5+ resolved city issues'},
        {'name': 'Community Hero', 'icon': '🏆', 'tier': 'Platinum', 'unlocked': civic_points >= 1000 or total_submitted >= 15, 'desc': 'Earned 1,000+ civic points through exemplary reporting'}
    ]

    unlocked_badges = [b for b in badges if b['unlocked']]
    current_title = unlocked_badges[-1]['name'] if unlocked_badges else 'Civic Contributor'
    current_badge_icon = unlocked_badges[-1]['icon'] if unlocked_badges else '👤'

    if civic_points >= 800:
        impact_rating, impact_color = 'VERY HIGH', 'text-success'
    elif civic_points >= 300:
        impact_rating, impact_color = 'HIGH', 'text-primary'
    elif civic_points >= 100:
        impact_rating, impact_color = 'MEDIUM', 'text-warning'
    else:
        impact_rating, impact_color = 'EMERGING', 'text-secondary'

    impact_stats = {
        'points': civic_points,
        'title': current_title,
        'badge_icon': current_badge_icon,
        'submitted': total_submitted,
        'verified': total_verified,
        'resolved': total_resolved,
        'rating': impact_rating,
        'rating_color': impact_color,
        'badges': badges
    }

    notifications = []
    user_complaint_ids = [c.id for c in complaints]
    
    if user_complaint_ids:
        history_logs = db.session.query(ComplaintStatusHistory, Complaint)\
            .join(Complaint, ComplaintStatusHistory.complaint_id == Complaint.id)\
            .filter(ComplaintStatusHistory.complaint_id.in_(user_complaint_ids))\
            .order_by(ComplaintStatusHistory.changed_at.desc()).limit(15).all()

        for log, comp in history_logs:
            if log.status == 'Assigned':
                icon = '🏢'
                message = f"Your complaint #CP{comp.id} ({comp.category}) has been assigned to field crew."
            elif log.status == 'Under Investigation':
                icon = '🔍'
                message = f"Inspection team is currently investigating complaint #CP{comp.id}."
            elif log.status == 'Work Started':
                icon = '🛠️'
                message = f"On-site repair work started for complaint #CP{comp.id}."
            elif log.status == 'Resolved':
                icon = '✅'
                message = f"Great news! Your complaint #CP{comp.id} has been resolved."
            else:
                icon = '🔔'
                message = f"Complaint #CP{comp.id} status updated to '{log.status}'."

            notifications.append({
                'id': log.id,
                'complaint_id': comp.id,
                'category': comp.category,
                'status': log.status,
                'icon': icon,
                'message': message,
                'notes': log.notes,
                'time': log.changed_at.strftime('%b %d, %H:%M')
            })

    for c in complaints:
        c.lifecycle_steps = calculate_lifecycle_steps(c)

    return render_template('citizen/dashboard.html', complaints=complaints, impact=impact_stats, notifications=notifications)

@citizen_bp.route('/api/analyze-text', methods=['POST'])
@login_required
def analyze_text_api():
    data = request.get_json() or {}
    description = data.get('description', '')
    
    category_guess = nlp_ai.predict_from_text(description)['predicted_category']
    existing_count = Complaint.query.filter_by(category=category_guess).count() + 1
    
    analysis = nlp_ai.predict_from_text(description, complaint_frequency=existing_count)
    return jsonify(analysis)

@citizen_bp.route('/feedback/<int:complaint_id>', methods=['POST'])
@login_required
def submit_feedback(complaint_id):
    complaint = Complaint.query.filter_by(id=complaint_id, user_id=current_user.id).first_or_404()
    
    if complaint.status != 'Resolved':
        flash('Feedback can only be submitted after an issue is officially marked as Resolved.', 'warning')
        return redirect(url_for('citizen.dashboard'))

    rating = request.form.get('rating', type=int)
    feedback_text = request.form.get('feedback_text', '').strip()

    if rating and 1 <= rating <= 5:
        complaint.rating = rating
        complaint.feedback_text = feedback_text
        db.session.commit()
        flash('Thank you for rating your issue resolution! Your feedback helps improve city services.', 'success')
    else:
        flash('Please select a star rating between 1 and 5.', 'danger')

    return redirect(url_for('citizen.dashboard'))

@citizen_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report_issue():
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description', '').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        # 🛑 BACKEND DEBOUNCE / DUPLICATE SUBMISSION GUARD
        # Prevents race conditions if a user rapid-clicks or submits duplicate requests within 10 seconds
        ten_seconds_ago = datetime.utcnow() - timedelta(seconds=10)
        recent_duplicate = Complaint.query.filter(
            Complaint.user_id == current_user.id,
            Complaint.description == description,
            Complaint.reported_at >= ten_seconds_ago
        ).first()

        if recent_duplicate:
            flash(f'Report #CP{recent_duplicate.id} is already being processed! Duplicate submission prevented.', 'info')
            return redirect(url_for('citizen.dashboard'))

        freq_count = Complaint.query.filter_by(category=category).count() + 1 if category and category != 'Auto' else 1
        text_analysis = nlp_ai.predict_from_text(description, complaint_frequency=freq_count)
        
        if not category or category == 'Auto':
            category = text_analysis['predicted_category']

        if 'issue_image' not in request.files:
            flash('No image provided. Evidence photo is required.', 'danger')
            return redirect(request.url)
            
        file = request.files['issue_image']
        if file.filename == '' or not allowed_file(file.filename):
            flash('Invalid image format. Please upload JPG or PNG.', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        unique_filename = f"user_{current_user.id}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        cv_class, cv_conf, cv_bbox, annotated_filename = vision_ai.analyze_image(file_path)

        CONFIDENCE_THRESHOLD = 0.60
        
        if cv_conf < CONFIDENCE_THRESHOLD:
            complaint_status = "Needs Manual Review"
            flash_msg = f'Report submitted! Vision confidence low ({int(cv_conf*100)}%). Flagged for manual review.'
            flash_category = 'warning'
        else:
            complaint_status = "Pending Dispatch"
            flash_msg = f'Report verified by AI ({int(cv_conf*100)}% Vision Conf). Priority: {text_analysis["priority_badge"]}'
            flash_category = 'success'

        now = datetime.now()
        ml_input = {
            'category': category,
            'latitude': float(latitude) if latitude else 19.9975,
            'longitude': float(longitude) if longitude else 73.7898,
            'hour_of_day': now.hour,
            'month': now.month,
            'weather': 'Clear', 
            'traffic_density': 'High' if text_analysis['location_risk'] == 'High' else 'Medium',
            'road_importance': 'Arterial' if text_analysis['location_risk'] == 'High' else 'Local',
            'distance_to_hospital_km': 1.2 if text_analysis['location_risk'] == 'High' else 4.5,
            'distance_to_school_km': 0.8 if text_analysis['location_risk'] == 'High' else 2.5,
            'historical_incidents_30d': random.randint(3, 12)
        }
        severity = severity_ai.predict(ml_input)
        final_priority_score = text_analysis['priority_score']

        existing_complaints = Complaint.query.filter_by(category=category, status="Pending Dispatch").all()
        parent_complaint_id = None
        DUPLICATE_RADIUS_METERS = 50.0

        for existing in existing_complaints:
            if existing.parent_id is None and latitude and longitude:
                dist = calculate_distance(float(latitude), float(longitude), existing.latitude, existing.longitude)
                if dist <= DUPLICATE_RADIUS_METERS:
                    parent_complaint_id = existing.id
                    break 

        new_complaint = Complaint(
            user_id=current_user.id,
            category=category,
            description=description,
            latitude=float(latitude) if latitude else 19.9975,
            longitude=float(longitude) if longitude else 73.7898,
            status=complaint_status if not parent_complaint_id else "Merged Duplicate",
            parent_id=parent_complaint_id
        )
        db.session.add(new_complaint)
        db.session.flush()

        audit_note = f"Report submitted by citizen. Initial AI Priority Score: {final_priority_score}/100."
        history_log = ComplaintStatusHistory(
            complaint_id=new_complaint.id,
            status=new_complaint.status,
            notes=audit_note,
            changed_by_id=current_user.id
        )
        db.session.add(history_log)

        media = Media(
            complaint_id=new_complaint.id,
            file_path=annotated_filename,
            cv_detected_class=cv_class,
            cv_confidence=cv_conf,
            cv_bounding_box=cv_bbox
        )
        db.session.add(media)
        
        prediction = AIPrediction(
            complaint_id=new_complaint.id,
            severity_level=severity,
            priority_score=final_priority_score,
            recommended_action=text_analysis['recommendation']
        )
        db.session.add(prediction)
        db.session.commit()
        
        if parent_complaint_id:
            flash(f'Report received! Grouped with existing {category} issue nearby to prioritize field dispatch.', 'info')
        else:
            flash(flash_msg, flash_category)
            
        return redirect(url_for('citizen.dashboard'))

    return render_template('citizen/report.html')