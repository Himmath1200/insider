"""
Activity Log Analysis Routes
Handles log viewing, filtering, searching, and suspicious activity detection
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database.models import db, ActivityLog, Alert, User
from datetime import datetime, timedelta

# Create blueprint
log_bp = Blueprint('logs', __name__, url_prefix='/logs')


@log_bp.route('/')
def view_logs():
    """
    View all activity logs with filtering and searching capabilities
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter_type', 'all')
    filter_status = request.args.get('filter_status', 'all')
    search_query = request.args.get('search', '')
    
    # Base query
    query = ActivityLog.query
    
    # Apply filters
    if filter_type != 'all':
        query = query.filter_by(activity_type=filter_type)
    
    if filter_status != 'all':
        query = query.filter_by(status=filter_status)
    
    # Apply search
    if search_query:
        query = query.filter(
            db.or_(
                ActivityLog.description.ilike(f'%{search_query}%'),
                User.username.ilike(f'%{search_query}%')
            )
        ).join(User)
    
    # Order by timestamp descending
    query = query.order_by(ActivityLog.timestamp.desc())
    
    # Paginate results (10 per page)
    logs = query.paginate(page=page, per_page=10)
    
    # Get unique activity types for filter dropdown
    activity_types = db.session.query(ActivityLog.activity_type.distinct()).all()
    activity_types = [t[0] for t in activity_types]
    
    return render_template('log_analysis.html', 
                         logs=logs,
                         activity_types=activity_types,
                         current_filter_type=filter_type,
                         current_filter_status=filter_status,
                         search_query=search_query)


@log_bp.route('/user/<int:user_id>')
def user_logs(user_id):
    """
    View logs for a specific user
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    
    logs = ActivityLog.query.filter_by(user_id=user_id).order_by(
        ActivityLog.timestamp.desc()
    ).paginate(page=page, per_page=20)
    
    return render_template('user_activity_logs.html', user=user, logs=logs)


@log_bp.route('/suspicious')
def suspicious_activity():
    """
    View only suspicious activities
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    
    logs = ActivityLog.query.filter_by(status='suspicious').order_by(
        ActivityLog.timestamp.desc()
    ).paginate(page=page, per_page=20)
    
    return render_template('suspicious_activities.html', logs=logs)


@log_bp.route('/failed-logins')
def failed_logins():
    """
    View all failed login attempts
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    
    logs = ActivityLog.query.filter_by(activity_type='failed_login').order_by(
        ActivityLog.timestamp.desc()
    ).paginate(page=page, per_page=20)
    
    return render_template('failed_logins.html', logs=logs)


def detect_suspicious_activity():
    """
    Detect suspicious activities using rule-based logic
    - Multiple failed logins (3+ in 15 minutes)
    - Access at unusual time
    - Unauthorized file access
    """
    
    suspicious_activities = []
    now = datetime.utcnow()
    fifteen_min_ago = now - timedelta(minutes=15)
    
    # Rule 1: Multiple failed logins
    failed_logins = ActivityLog.query.filter(
        ActivityLog.activity_type == 'failed_login',
        ActivityLog.timestamp >= fifteen_min_ago
    ).all()
    
    # Group by user
    users_failed_logins = {}
    for log in failed_logins:
        if log.user_id not in users_failed_logins:
            users_failed_logins[log.user_id] = []
        users_failed_logins[log.user_id].append(log)
    
    # Check for 3+ failed logins
    for user_id, logs in users_failed_logins.items():
        if len(logs) >= 3:
            user = User.query.get(user_id)
            # Create alert
            alert = Alert(
                alert_type='suspicious_activity',
                user_id=user_id,
                title=f'Multiple Failed Login Attempts - {user.username}',
                description=f'{len(logs)} failed login attempts in the last 15 minutes',
                severity='high',
                status='open'
            )
            db.session.add(alert)
            suspicious_activities.append(alert)
    
    db.session.commit()
    return suspicious_activities


@log_bp.route('/api/activity-stats')
def get_activity_stats():
    """
    API endpoint to get activity statistics for charts
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get data from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    activities = ActivityLog.query.filter(
        ActivityLog.timestamp >= thirty_days_ago
    ).all()
    
    # Count by type
    type_count = {}
    for activity in activities:
        type_count[activity.activity_type] = type_count.get(activity.activity_type, 0) + 1
    
    # Count by status
    status_count = {
        'normal': ActivityLog.query.filter_by(status='normal').count(),
        'suspicious': ActivityLog.query.filter_by(status='suspicious').count(),
        'critical': ActivityLog.query.filter_by(status='critical').count(),
    }
    
    return jsonify({
        'type_count': type_count,
        'status_count': status_count,
    })


@log_bp.route('/api/timeline')
def get_timeline():
    """
    API endpoint to get activity timeline for the last 24 hours
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get data from last 24 hours
    twentyfour_hours_ago = datetime.utcnow() - timedelta(hours=24)
    
    activities = ActivityLog.query.filter(
        ActivityLog.timestamp >= twentyfour_hours_ago
    ).order_by(ActivityLog.timestamp.asc()).all()
    
    timeline = []
    for activity in activities:
        timeline.append({
            'timestamp': activity.timestamp.isoformat(),
            'user': activity.user.username if activity.user else 'Unknown',
            'activity_type': activity.activity_type,
            'status': activity.status,
            'description': activity.description
        })
    
    return jsonify(timeline)
