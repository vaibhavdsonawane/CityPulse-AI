from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='citizen') # 'citizen' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaints = db.relationship('Complaint', backref='author', lazy=True)

class Department(db.Model):
    __tablename__ = 'department'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)

    assignments = db.relationship('ComplaintAssignment', backref='department', lazy=True)

class Complaint(db.Model):
    __tablename__ = 'complaint'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='Pending Dispatch')
    parent_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=True)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    media = db.relationship('Media', backref='complaint', uselist=False, lazy=True)
    ai_prediction = db.relationship('AIPrediction', backref='complaint', uselist=False, lazy=True)
    assignment = db.relationship('ComplaintAssignment', backref='complaint', uselist=False, lazy=True)
    status_history = db.relationship('ComplaintStatusHistory', backref='complaint', lazy=True)

class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    cv_detected_class = db.Column(db.String(50), nullable=True)
    cv_confidence = db.Column(db.Float, nullable=True)
    cv_bounding_box = db.Column(db.String(100), nullable=True)

class AIPrediction(db.Model):
    __tablename__ = 'ai_prediction'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    severity_level = db.Column(db.String(20), nullable=False)
    priority_score = db.Column(db.Float, nullable=False)
    recommended_action = db.Column(db.Text, nullable=True)
    human_verified = db.Column(db.Boolean, default=False)
    is_correct = db.Column(db.Boolean, default=True)
    corrected_class = db.Column(db.String(50), nullable=True)

class ComplaintAssignment(db.Model):
    __tablename__ = 'complaint_assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

class ComplaintStatusHistory(db.Model):
    __tablename__ = 'complaint_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    changed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)