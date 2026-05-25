"""
Privilege Escalation Detection Routes
Handles privilege escalation attempts, logging, and reporting
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from database.models import db, EscalationLog, Alert, User
from datetime import datetime, timedelta

# Create blueprint
escalation_bp = Blueprint('escalation', __name__, url_prefix='/escalation')


@escalation_bp.route('/')
def index():
    """
    Privilege Escalation Dashboard
    Shows overview of escalation attempts
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    
    # Get all escalation attempts
    escalations = EscalationLog.query.order_by(
        EscalationLog.timestamp.desc()
    ).paginate(page=page, per_page=20)
    
    # Statistics
    total_escalations = EscalationLog.query.count()
    blocked_escalations = EscalationLog.query.filter_by(status='blocked').count()
    critical_escalations = EscalationLog.query.filter_by(severity='critical').count()
    
    stats = {
        'total': total_escalations,
        'blocked': blocked_escalations,
        'critical': critical_escalations,
        'allowed': EscalationLog.query.filter_by(status='allowed').count(),
    }
    
    return render_template('privilege_escalation.html', 
                         escalations=escalations,
                         stats=stats)


@escalation_bp.route('/simulate', methods=['GET', 'POST'])
def simulate_escalation():
    """
    Simulate privilege escalation attempt
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        escalation_type = request.form.get('escalation_type')
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Create escalation attempt log
        escalation = EscalationLog(
            user_id=user_id,
            escalation_type=escalation_type,
            attempted_role='admin',
            current_role=user.role,
            description=f'User attempted {escalation_type}',
            severity='high',
            status='blocked'
        )
        
        db.session.add(escalation)
        
        # Create alert
        alert = Alert(
            alert_type='escalation',
            user_id=user_id,
            title=f'Privilege Escalation Attempt - {user.username}',
            description=f'Attempt type: {escalation_type}',
            severity='high',
            status='open'
        )
        
        db.session.add(alert)
        db.session.commit()
        
        flash('Escalation attempt has been logged and blocked', 'warning')
        return redirect(url_for('escalation.view_report'))
    
    return render_template('simulate_escalation.html')


@escalation_bp.route('/report')
def view_report():
    """
    View escalation report
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get all escalations grouped by severity
    critical = EscalationLog.query.filter_by(severity='critical').order_by(
        EscalationLog.timestamp.desc()
    ).all()
    
    high = EscalationLog.query.filter_by(severity='high').order_by(
        EscalationLog.timestamp.desc()
    ).all()
    
    medium = EscalationLog.query.filter_by(severity='medium').order_by(
        EscalationLog.timestamp.desc()
    ).all()
    
    low = EscalationLog.query.filter_by(severity='low').order_by(
        EscalationLog.timestamp.desc()
    ).all()
    
    # Count by type
    type_count = {}
    all_escalations = EscalationLog.query.all()
    for escalation in all_escalations:
        type_count[escalation.escalation_type] = type_count.get(escalation.escalation_type, 0) + 1
    
    stats = {
        'critical_count': len(critical),
        'high_count': len(high),
        'medium_count': len(medium),
        'low_count': len(low),
        'total_count': EscalationLog.query.count(),
        'blocked_count': EscalationLog.query.filter_by(status='blocked').count(),
        'type_count': type_count,
    }
    
    return render_template('escalation_report.html',
                         critical=critical,
                         high=high,
                         medium=medium,
                         low=low,
                         stats=stats)


@escalation_bp.route('/user/<int:user_id>')
def user_escalations(user_id):
    """
    View escalation attempts for a specific user
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get_or_404(user_id)
    escalations = EscalationLog.query.filter_by(user_id=user_id).order_by(
        EscalationLog.timestamp.desc()
    ).all()
    
    return render_template('user_escalations.html', user=user, escalations=escalations)


@escalation_bp.route('/api/escalation-stats')
def get_escalation_stats():
    """
    API endpoint to get escalation statistics for charts
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Severity breakdown
    severity_count = {
        'critical': EscalationLog.query.filter_by(severity='critical').count(),
        'high': EscalationLog.query.filter_by(severity='high').count(),
        'medium': EscalationLog.query.filter_by(severity='medium').count(),
        'low': EscalationLog.query.filter_by(severity='low').count(),
    }
    
    # Status breakdown
    status_count = {
        'blocked': EscalationLog.query.filter_by(status='blocked').count(),
        'allowed': EscalationLog.query.filter_by(status='allowed').count(),
        'pending': EscalationLog.query.filter_by(status='pending').count(),
    }
    
    # Type breakdown
    all_escalations = EscalationLog.query.all()
    type_count = {}
    for escalation in all_escalations:
        type_count[escalation.escalation_type] = type_count.get(escalation.escalation_type, 0) + 1
    
    return jsonify({
        'severity_count': severity_count,
        'status_count': status_count,
        'type_count': type_count,
    })


@escalation_bp.route('/api/timeline')
def get_timeline():
    """
    API endpoint to get escalation timeline
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get data from last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    escalations = EscalationLog.query.filter(
        EscalationLog.timestamp >= seven_days_ago
    ).order_by(EscalationLog.timestamp.asc()).all()
    
    timeline = []
    for escalation in escalations:
        timeline.append({
            'timestamp': escalation.timestamp.isoformat(),
            'user': escalation.user.username if escalation.user else 'Unknown',
            'type': escalation.escalation_type,
            'severity': escalation.severity,
            'status': escalation.status,
        })
    
    return jsonify(timeline)
