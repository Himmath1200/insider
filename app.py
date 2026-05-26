"""
Insider Threat Detection System
Flask Application Entry Point
"""

from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_session import Session
from flask_cors import CORS
from database.models import db
from database.init_db import init_db
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///insider_threat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# CORS Configuration
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'localhost:3000,localhost:5000').split(',')
CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

# Initialize extensions
db.init_app(app)
Session(app)

# Import routes
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.log_routes import log_bp
from routes.escalation_routes import escalation_bp
from routes.exfiltration_routes import exfiltration_bp
from routes.mitigation_routes import mitigation_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(log_bp)
app.register_blueprint(escalation_bp)
app.register_blueprint(exfiltration_bp)
app.register_blueprint(mitigation_bp)


@app.before_request
def before_request():
    """
    Execute before each request
    - Check if database exists, if not initialize it
    - Store current user in session
    """
    # Check if user is logged in
    if 'user_id' in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)


@app.context_processor
def inject_user():
    """
    Inject current user data into all templates
    """
    if 'user_id' in session:
        from database.models import User
        user = User.query.get(session['user_id'])
        if user:
            return dict(current_user=user)
    return dict(current_user=None)


@app.route('/')
def index():
    """
    Home page / Dashboard
    Redirects to login if not authenticated
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """
    Main Dashboard Page
    Shows overview of all modules and recent alerts
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from database.models import User, Alert, ActivityLog, EscalationLog, DataAccessLog
    
    user = User.query.get(session['user_id'])
    
    # Get statistics
    total_users = User.query.count()
    total_alerts = Alert.query.filter_by(status='open').count()
    critical_alerts = Alert.query.filter_by(status='open', severity='critical').count()
    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()
    open_alerts = Alert.query.filter_by(status='open').order_by(Alert.timestamp.desc()).limit(10).all()
    
    # Get chart data
    suspicious_activities = ActivityLog.query.filter_by(status='suspicious').count()
    normal_activities = ActivityLog.query.filter_by(status='normal').count()
    
    escalations = EscalationLog.query.count()
    critical_escalations = EscalationLog.query.filter_by(severity='critical').count()
    
    data_exfiltrations = DataAccessLog.query.filter_by(is_suspicious=True).count()
    
    stats = {
        'total_users': total_users,
        'total_alerts': total_alerts,
        'critical_alerts': critical_alerts,
        'suspicious_activities': suspicious_activities,
        'normal_activities': normal_activities,
        'escalations': escalations,
        'critical_escalations': critical_escalations,
        'data_exfiltrations': data_exfiltrations,
    }
    
    return render_template('index.html', 
                         user=user,
                         stats=stats,
                         recent_activities=recent_activities,
                         open_alerts=open_alerts)


@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    """
    API endpoint to get dashboard statistics for charts
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    from database.models import ActivityLog, Alert, EscalationLog, DataAccessLog
    from datetime import datetime, timedelta
    
    # Get data from last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Activity trend
    activities = ActivityLog.query.filter(
        ActivityLog.timestamp >= seven_days_ago
    ).all()
    
    alerts = Alert.query.filter(
        Alert.timestamp >= seven_days_ago
    ).all()
    
    # Group by day
    activity_by_day = {}
    for activity in activities:
        day = activity.timestamp.strftime('%Y-%m-%d')
        activity_by_day[day] = activity_by_day.get(day, 0) + 1
    
    alert_by_day = {}
    for alert in alerts:
        day = alert.timestamp.strftime('%Y-%m-%d')
        alert_by_day[day] = alert_by_day.get(day, 0) + 1
    
    # Severity breakdown
    severity_count = {
        'critical': Alert.query.filter_by(severity='critical').count(),
        'high': Alert.query.filter_by(severity='high').count(),
        'medium': Alert.query.filter_by(severity='medium').count(),
        'low': Alert.query.filter_by(severity='low').count(),
    }
    
    return jsonify({
        'activity_trend': activity_by_day,
        'alert_trend': alert_by_day,
        'severity_breakdown': severity_count,
    })


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


def create_app():
    """
    Application factory function
    """
    # Initialize database if it doesn't exist
    if not os.path.exists('insider_threat.db'):
        with app.app_context():
            init_db(app)
    
    return app


if __name__ == '__main__':
    # Create app context and initialize database
    with app.app_context():
        if not os.path.exists('insider_threat.db'):
            print("\n" + "="*50)
            print("Initializing database for the first time...")
            print("="*50)
            init_db(app)
    
    # Run Flask application
    # Get port from environment variable (Railway, Heroku) or use default for development
    port = int(os.getenv('PORT', 5000))
    is_production = os.getenv('ENVIRONMENT') == 'production'
    
    print("\n" + "="*50)
    print("Starting Insider Threat Detection System")
    print("="*50)
    print(f"Server running on port {port}")
    print(f"Environment: {'Production' if is_production else 'Development'}")
    print("="*50 + "\n")
    
    # Production: use 0.0.0.0 for all interfaces, development: use localhost
    host = '0.0.0.0' if is_production else 'localhost'
    app.run(debug=not is_production, host=host, port=port)
