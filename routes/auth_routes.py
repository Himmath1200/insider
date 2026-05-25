"""
Authentication Routes
Handles user login and logout
"""

from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database.models import db, User

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Page and Handler
    Authenticates user credentials against database
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('auth.login'))
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('This account is inactive', 'danger')
                return redirect(url_for('auth.login'))
            
            # Set session variables
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session.permanent = True
            
            # Log the login activity
            from database.models import ActivityLog
            from datetime import datetime
            
            activity = ActivityLog(
                user_id=user.id,
                activity_type='login',
                description=f'User {username} logged in',
                status='normal',
                ip_address=request.remote_addr
            )
            db.session.add(activity)
            db.session.commit()
            
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        
        else:
            # Log failed login attempt
            from database.models import ActivityLog
            
            activity = ActivityLog(
                user_id=user.id if user else None,
                activity_type='failed_login',
                description=f'Failed login attempt for {username}',
                status='suspicious',
                ip_address=request.remote_addr
            )
            db.session.add(activity)
            db.session.commit()
            
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    User Logout Handler
    Clears session and logs the logout activity
    """
    if 'user_id' in session:
        user_id = session['user_id']
        username = session.get('username', 'Unknown')
        
        # Log the logout activity
        from database.models import ActivityLog
        
        activity = ActivityLog(
            user_id=user_id,
            activity_type='logout',
            description=f'User {username} logged out',
            status='normal'
        )
        db.session.add(activity)
        db.session.commit()
    
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/unauthorized')
def unauthorized():
    """
    Unauthorized Access Page
    """
    return render_template('unauthorized.html'), 403
