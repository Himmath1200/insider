"""
Mitigation and Security Policy Routes
Handles security recommendations and policy management
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database.models import db, SecurityPolicy

# Create blueprint
mitigation_bp = Blueprint('mitigation', __name__, url_prefix='/mitigation')


def require_admin(f):
    """Decorator to require admin role"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('auth.unauthorized'))
        return f(*args, **kwargs)
    
    return decorated_function


@mitigation_bp.route('/')
def index():
    """
    Security Mitigation and Policy Page
    Shows recommendations and current policies
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get all policies grouped by type
    policies = SecurityPolicy.query.all()
    
    policy_types = {}
    for policy in policies:
        if policy.policy_type not in policy_types:
            policy_types[policy.policy_type] = []
        policy_types[policy.policy_type].append(policy)
    
    # Count policies by priority
    priority_count = {
        'critical': SecurityPolicy.query.filter_by(priority='critical').count(),
        'high': SecurityPolicy.query.filter_by(priority='high').count(),
        'medium': SecurityPolicy.query.filter_by(priority='medium').count(),
        'low': SecurityPolicy.query.filter_by(priority='low').count(),
    }
    
    return render_template('mitigation.html', 
                         policies=policies,
                         policy_types=policy_types,
                         priority_count=priority_count)


@mitigation_bp.route('/password-policy')
def password_policy():
    """
    Password Policy Recommendations
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    policies = SecurityPolicy.query.filter_by(policy_type='password_policy').all()
    
    recommendations = [
        'Minimum 12 characters',
        'Mix of uppercase, lowercase, numbers, and special characters',
        'No dictionary words',
        'No personal information',
        'Change password every 90 days',
        'Remember last 5 passwords',
        'Account lockout after 5 failed attempts',
    ]
    
    return render_template('password_policy.html', 
                         policies=policies,
                         recommendations=recommendations)


@mitigation_bp.route('/access-control')
def access_control():
    """
    Access Control Policy Recommendations
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    policies = SecurityPolicy.query.filter_by(policy_type='access_control').all()
    
    recommendations = [
        'Implement Role-Based Access Control (RBAC)',
        'Apply principle of least privilege',
        'Regular access reviews (quarterly)',
        'Segregation of duties',
        'Enforce strong authentication for privileged access',
        'Monitor and audit access changes',
        'Implement Multi-Factor Authentication (MFA) for admin accounts',
    ]
    
    return render_template('access_control.html', 
                         policies=policies,
                         recommendations=recommendations)


@mitigation_bp.route('/login-restrictions')
def login_restrictions():
    """
    Login and Authentication Restrictions
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    policies = SecurityPolicy.query.filter_by(policy_type='login_restrictions').all()
    
    recommendations = [
        'Account lockout after 5 failed login attempts',
        '30-minute lockout period',
        'Log all login attempts',
        'Alert on failed login from new location',
        'Session timeout after 30 minutes of inactivity',
        'Require re-authentication for sensitive operations',
        'Implement geographic restrictions if applicable',
        'Monitor login patterns for anomalies',
    ]
    
    return render_template('login_restrictions.html', 
                         policies=policies,
                         recommendations=recommendations)


@mitigation_bp.route('/monitoring-policy')
def monitoring_policy():
    """
    Activity Monitoring and Logging Policy
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    policies = SecurityPolicy.query.filter_by(policy_type='monitoring_policy').all()
    
    recommendations = [
        'Log all user login/logout events',
        'Track all file access attempts',
        'Monitor database queries',
        'Track privilege changes and escalation attempts',
        'Alert on suspicious patterns (3+ failed logins)',
        'Alert on unusual access times',
        'Log all administrative actions',
        'Retain logs for minimum 90 days',
        'Regular log review and analysis',
    ]
    
    return render_template('monitoring_policy.html', 
                         policies=policies,
                         recommendations=recommendations)


@mitigation_bp.route('/data-protection')
def data_protection():
    """
    Data Protection and DLP Policy
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    policies = SecurityPolicy.query.filter_by(policy_type='data_protection').all()
    
    recommendations = [
        'Classify data by sensitivity level',
        'Implement Data Loss Prevention (DLP) rules',
        'Restrict large file downloads (max 100MB)',
        'Monitor external data transfers',
        'Encrypt data at rest and in transit',
        'Restrict copy/paste operations for sensitive data',
        'Track USB device usage',
        'Require approval for external transfers',
        'Monitor cloud storage access',
    ]
    
    return render_template('data_protection.html', 
                         policies=policies,
                         recommendations=recommendations)


@mitigation_bp.route('/policy/<int:policy_id>/update-notes', methods=['POST'])
@require_admin
def update_policy_notes(policy_id):
    """
    Update admin notes for a policy (Admin only)
    """
    policy = SecurityPolicy.query.get_or_404(policy_id)
    
    notes = request.form.get('admin_notes')
    
    if notes:
        policy.admin_notes = notes
        policy.updated_at = db.func.now()
        db.session.commit()
        flash('Policy notes updated successfully', 'success')
    
    return redirect(url_for('mitigation.index'))


@mitigation_bp.route('/api/policies')
def get_policies():
    """
    API endpoint to get all policies in JSON format
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    policies = SecurityPolicy.query.all()
    
    policies_data = []
    for policy in policies:
        policies_data.append({
            'id': policy.id,
            'type': policy.policy_type,
            'title': policy.title,
            'description': policy.description,
            'recommendation': policy.recommendation,
            'priority': policy.priority,
            'admin_notes': policy.admin_notes,
        })
    
    return jsonify(policies_data)


@mitigation_bp.route('/api/priority-stats')
def get_priority_stats():
    """
    API endpoint to get policy priority statistics
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    priority_count = {
        'critical': SecurityPolicy.query.filter_by(priority='critical').count(),
        'high': SecurityPolicy.query.filter_by(priority='high').count(),
        'medium': SecurityPolicy.query.filter_by(priority='medium').count(),
        'low': SecurityPolicy.query.filter_by(priority='low').count(),
    }
    
    # Type breakdown
    type_count = {}
    all_policies = SecurityPolicy.query.all()
    for policy in all_policies:
        type_count[policy.policy_type] = type_count.get(policy.policy_type, 0) + 1
    
    return jsonify({
        'priority_count': priority_count,
        'type_count': type_count,
    })
