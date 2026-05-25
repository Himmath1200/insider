"""
User Enumeration and Access Mapping Routes
Handles user management and access control
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.models import db, User
from datetime import datetime

# Create blueprint
user_bp = Blueprint('users', __name__, url_prefix='/users')


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


@user_bp.route('/')
def list_users():
    """
    List all users with their roles and permissions
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get all users
    users = User.query.all()
    
    # Define role permissions mapping
    role_permissions = {
        'admin': ['User Management', 'Log Analysis', 'System Settings', 'Report Generation'],
        'user': ['View Profile', 'View Own Activity Logs', 'Request Access']
    }
    
    user_data = []
    for user in users:
        user_data.append({
            'user': user,
            'permissions': role_permissions.get(user.role, [])
        })
    
    return render_template('user_enumeration.html', users=user_data, role_permissions=role_permissions)


@user_bp.route('/access-mapping')
def access_mapping():
    """
    Display access mapping page showing user roles and permissions
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    users = User.query.all()
    
    # Define access matrix
    access_matrix = {
        'admin': {
            'user_management': True,
            'log_analysis': True,
            'system_settings': True,
            'report_generation': True,
            'data_access': True,
            'privilege_escalation': True
        },
        'user': {
            'user_management': False,
            'log_analysis': True,
            'system_settings': False,
            'report_generation': False,
            'data_access': True,
            'privilege_escalation': False
        }
    }
    
    return render_template('access_mapping.html', users=users, access_matrix=access_matrix)


@user_bp.route('/add', methods=['GET', 'POST'])
@require_admin
def add_user():
    """
    Add new user (Admin only)
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        department = request.form.get('department')
        
        # Validate inputs
        if not all([username, email, password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('users.add_user'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('users.add_user'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('users.add_user'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            role=role,
            department=department
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {username} created successfully', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('add_user.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@require_admin
def edit_user(user_id):
    """
    Edit user details (Admin only)
    """
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.role = request.form.get('role', 'user')
        user.department = request.form.get('department')
        user.is_active = request.form.get('is_active') == 'on'
        
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        db.session.commit()
        flash(f'User {user.username} updated successfully', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('edit_user.html', user=user)


@user_bp.route('/delete/<int:user_id>', methods=['POST'])
@require_admin
def delete_user(user_id):
    """
    Delete user (Admin only)
    """
    # Prevent deleting current admin
    if user_id == session.get('user_id'):
        flash('You cannot delete your own account', 'danger')
        return redirect(url_for('users.list_users'))
    
    user = User.query.get_or_404(user_id)
    username = user.username
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} deleted successfully', 'success')
    return redirect(url_for('users.list_users'))


@user_bp.route('/api/user-roles')
def get_user_roles():
    """
    API endpoint to get user role distribution for charts
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    users = User.query.all()
    role_count = {}
    
    for user in users:
        role = user.role
        role_count[role] = role_count.get(role, 0) + 1
    
    return jsonify(role_count)


@user_bp.route('/profile')
def profile():
    """
    View current user's profile
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    # Get user's recent activities
    from database.models import ActivityLog
    recent_activities = ActivityLog.query.filter_by(user_id=user.id).order_by(
        ActivityLog.timestamp.desc()
    ).limit(10).all()
    
    return render_template('profile.html', user=user, recent_activities=recent_activities)
