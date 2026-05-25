"""
Database Models for Insider Threat Detection System
This module contains all SQLAlchemy models for the application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for login and access control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    department = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    activity_logs = db.relationship('ActivityLog', back_populates='user')
    escalation_logs = db.relationship('EscalationLog', back_populates='user')
    data_access_logs = db.relationship('DataAccessLog', back_populates='user')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class ActivityLog(db.Model):
    """Activity Log model to track user activities"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # login, logout, file_access, failed_login
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    status = db.Column(db.String(20), default='normal')  # normal, suspicious, critical
    
    # Relationships
    user = db.relationship('User', back_populates='activity_logs')
    
    def __repr__(self):
        return f'<ActivityLog {self.user_id} - {self.activity_type}>'


class EscalationLog(db.Model):
    """Privilege Escalation Log model"""
    __tablename__ = 'escalation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    escalation_type = db.Column(db.String(100), nullable=False)  # unauthorized_role_switch, admin_access_attempt
    attempted_role = db.Column(db.String(20))
    current_role = db.Column(db.String(20))
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='blocked')  # blocked, allowed, pending
    
    # Relationships
    user = db.relationship('User', back_populates='escalation_logs')
    
    def __repr__(self):
        return f'<EscalationLog {self.user_id} - {self.escalation_type}>'


class DataAccessLog(db.Model):
    """Data Access and Exfiltration Log model"""
    __tablename__ = 'data_access_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    access_type = db.Column(db.String(50), nullable=False)  # read, download, copy, transfer
    file_size = db.Column(db.Integer)  # in KB
    destination = db.Column(db.String(255))  # external transfer destination
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_suspicious = db.Column(db.Boolean, default=False)
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high, critical
    
    # Relationships
    user = db.relationship('User', back_populates='data_access_logs')
    
    def __repr__(self):
        return f'<DataAccessLog {self.user_id} - {self.file_name}>'


class SecurityPolicy(db.Model):
    """Security Policy and Mitigation Recommendations"""
    __tablename__ = 'security_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    policy_type = db.Column(db.String(100), nullable=False)  # password_policy, access_control, etc
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SecurityPolicy {self.policy_type}>'


class Alert(db.Model):
    """Security Alerts for suspicious activities"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)  # suspicious_activity, escalation, exfiltration
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='open')  # open, acknowledged, resolved
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Alert {self.alert_type} - {self.severity}>'
