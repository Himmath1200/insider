"""
Data Access and Exfiltration Detection Routes
Handles file access tracking, suspicious data exfiltration detection
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from database.models import db, DataAccessLog, Alert, User
from datetime import datetime, timedelta

# Create blueprint
exfiltration_bp = Blueprint('exfiltration', __name__, url_prefix='/exfiltration')


@exfiltration_bp.route('/')
def index():
    """
    Data Exfiltration Dashboard
    Shows overview of file access and suspicious activities
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    
    # Get all data access logs
    logs = DataAccessLog.query.order_by(
        DataAccessLog.timestamp.desc()
    ).paginate(page=page, per_page=20)
    
    # Statistics
    total_accesses = DataAccessLog.query.count()
    suspicious_accesses = DataAccessLog.query.filter_by(is_suspicious=True).count()
    critical_risk = DataAccessLog.query.filter_by(risk_level='critical').count()
    
    stats = {
        'total_accesses': total_accesses,
        'suspicious_accesses': suspicious_accesses,
        'critical_risk': critical_risk,
        'high_risk': DataAccessLog.query.filter_by(risk_level='high').count(),
    }
    
    return render_template('data_exfiltration.html', 
                         logs=logs,
                         stats=stats)


@exfiltration_bp.route('/simulate', methods=['GET', 'POST'])
def simulate_exfiltration():
    """
    Simulate data exfiltration attempt
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        file_name = request.form.get('file_name')
        access_type = request.form.get('access_type')
        file_size = request.form.get('file_size', type=int)
        destination = request.form.get('destination')
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Determine risk level based on criteria
        risk_level = 'low'
        is_suspicious = False
        
        if file_size > 5000:  # > 5MB
            risk_level = 'high'
            is_suspicious = True
        
        if destination and destination != 'local':
            risk_level = 'critical' if risk_level == 'high' else 'high'
            is_suspicious = True
        
        if access_type in ['download', 'transfer']:
            is_suspicious = True
            risk_level = 'high' if risk_level in ['low', 'medium'] else risk_level
        
        # Create data access log
        access_log = DataAccessLog(
            user_id=user_id,
            file_name=file_name,
            access_type=access_type,
            file_size=file_size,
            destination=destination,
            is_suspicious=is_suspicious,
            risk_level=risk_level,
            description=f'Simulated {access_type} attempt'
        )
        
        db.session.add(access_log)
        
        # Create alert if suspicious
        if is_suspicious:
            alert_title = 'Data Exfiltration Alert'
            if risk_level == 'critical':
                alert_title = f'CRITICAL: Potential Data Exfiltration - {user.username}'
                alert_severity = 'critical'
            elif risk_level == 'high':
                alert_title = f'High Risk Data Access - {user.username}'
                alert_severity = 'high'
            else:
                alert_title = f'Suspicious Data Access - {user.username}'
                alert_severity = 'medium'
            
            alert = Alert(
                alert_type='exfiltration',
                user_id=user_id,
                title=alert_title,
                description=f'File: {file_name}, Type: {access_type}, Size: {file_size}KB, Destination: {destination}',
                severity=alert_severity,
                status='open'
            )
            
            db.session.add(alert)
        
        db.session.commit()
        
        status_msg = 'blocked' if is_suspicious else 'allowed'
        flash(f'Data exfiltration attempt has been logged and {status_msg}', 'warning' if is_suspicious else 'info')
        return redirect(url_for('exfiltration.view_report'))
    
    return render_template('simulate_data_access.html')


@exfiltration_bp.route('/suspicious')
def suspicious_access():
    """
    View suspicious data access attempts
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    
    logs = DataAccessLog.query.filter_by(is_suspicious=True).order_by(
        DataAccessLog.timestamp.desc()
    ).paginate(page=page, per_page=20)
    
    return render_template('suspicious_data_access.html', logs=logs)


@exfiltration_bp.route('/report')
def view_report():
    """
    View data exfiltration report
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get all data access logs grouped by risk level
    critical = DataAccessLog.query.filter_by(risk_level='critical').order_by(
        DataAccessLog.timestamp.desc()
    ).all()
    
    high = DataAccessLog.query.filter_by(risk_level='high').order_by(
        DataAccessLog.timestamp.desc()
    ).all()
    
    medium = DataAccessLog.query.filter_by(risk_level='medium').order_by(
        DataAccessLog.timestamp.desc()
    ).all()
    
    low = DataAccessLog.query.filter_by(risk_level='low').order_by(
        DataAccessLog.timestamp.desc()
    ).all()
    
    # Access type breakdown
    type_count = {}
    all_accesses = DataAccessLog.query.all()
    for access in all_accesses:
        type_count[access.access_type] = type_count.get(access.access_type, 0) + 1
    
    stats = {
        'critical_count': len(critical),
        'high_count': len(high),
        'medium_count': len(medium),
        'low_count': len(low),
        'total_count': DataAccessLog.query.count(),
        'suspicious_count': DataAccessLog.query.filter_by(is_suspicious=True).count(),
        'type_count': type_count,
    }
    
    return render_template('exfiltration_report.html',
                         critical=critical,
                         high=high,
                         medium=medium,
                         low=low,
                         stats=stats)


@exfiltration_bp.route('/user/<int:user_id>')
def user_accesses(user_id):
    """
    View data access attempts for a specific user
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get_or_404(user_id)
    accesses = DataAccessLog.query.filter_by(user_id=user_id).order_by(
        DataAccessLog.timestamp.desc()
    ).all()
    
    return render_template('user_data_accesses.html', user=user, accesses=accesses)


@exfiltration_bp.route('/api/exfiltration-stats')
def get_exfiltration_stats():
    """
    API endpoint to get exfiltration statistics for charts
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Risk level breakdown
    risk_count = {
        'critical': DataAccessLog.query.filter_by(risk_level='critical').count(),
        'high': DataAccessLog.query.filter_by(risk_level='high').count(),
        'medium': DataAccessLog.query.filter_by(risk_level='medium').count(),
        'low': DataAccessLog.query.filter_by(risk_level='low').count(),
    }
    
    # Access type breakdown
    all_accesses = DataAccessLog.query.all()
    type_count = {}
    for access in all_accesses:
        type_count[access.access_type] = type_count.get(access.access_type, 0) + 1
    
    # Suspicious vs normal
    suspicious_count = DataAccessLog.query.filter_by(is_suspicious=True).count()
    normal_count = DataAccessLog.query.filter_by(is_suspicious=False).count()
    
    return jsonify({
        'risk_count': risk_count,
        'type_count': type_count,
        'suspicious_count': suspicious_count,
        'normal_count': normal_count,
    })


@exfiltration_bp.route('/api/top-files')
def get_top_files():
    """
    API endpoint to get most accessed files
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    all_accesses = DataAccessLog.query.all()
    file_count = {}
    
    for access in all_accesses:
        file_count[access.file_name] = file_count.get(access.file_name, 0) + 1
    
    # Sort by count and get top 10
    top_files = sorted(file_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return jsonify({
        'files': [{'name': f[0], 'count': f[1]} for f in top_files]
    })
