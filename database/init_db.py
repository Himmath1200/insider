"""
Database Initialization with Sample Data
This script creates all database tables and populates them with sample data
"""

from datetime import datetime, timedelta
from database.models import db, User, ActivityLog, EscalationLog, DataAccessLog, SecurityPolicy, Alert


def init_db(app):
    """
    Initialize the database and create all tables
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        # Drop all tables (for fresh initialization)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✓ Database tables created successfully!")
        
        # Add sample data
        add_sample_data()
        
        print("✓ Sample data added successfully!")


def add_sample_data():
    """Add sample data for testing and demonstration"""
    
    # Create sample users
    print("\n--- Adding Sample Users ---")
    
    # Admin user
    admin = User(
        username='admin',
        email='admin@insider-threat.local',
        role='admin',
        department='IT Security'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Regular users
    user1 = User(
        username='john_dev',
        email='john@company.local',
        role='user',
        department='Development'
    )
    user1.set_password('user123')
    db.session.add(user1)
    
    user2 = User(
        username='sarah_sales',
        email='sarah@company.local',
        role='user',
        department='Sales'
    )
    user2.set_password('user123')
    db.session.add(user2)
    
    user3 = User(
        username='mike_hr',
        email='mike@company.local',
        role='user',
        department='Human Resources'
    )
    user3.set_password('user123')
    db.session.add(user3)
    
    user4 = User(
        username='alice_finance',
        email='alice@company.local',
        role='user',
        department='Finance'
    )
    user4.set_password('user123')
    db.session.add(user4)
    
    db.session.commit()
    print(f"✓ Created 5 sample users")
    
    # Create sample activity logs
    print("--- Adding Sample Activity Logs ---")
    
    base_time = datetime.utcnow()
    
    activities = [
        ActivityLog(user_id=2, activity_type='login', timestamp=base_time - timedelta(hours=2), 
                   ip_address='192.168.1.100', status='normal', description='Normal login'),
        ActivityLog(user_id=2, activity_type='file_access', timestamp=base_time - timedelta(hours=1.5),
                   description='Accessed: project_files.zip', status='normal'),
        ActivityLog(user_id=3, activity_type='failed_login', timestamp=base_time - timedelta(minutes=45),
                   ip_address='192.168.1.101', status='suspicious', description='3 failed login attempts'),
        ActivityLog(user_id=3, activity_type='failed_login', timestamp=base_time - timedelta(minutes=40),
                   ip_address='192.168.1.101', status='suspicious'),
        ActivityLog(user_id=3, activity_type='failed_login', timestamp=base_time - timedelta(minutes=35),
                   ip_address='192.168.1.101', status='suspicious'),
        ActivityLog(user_id=3, activity_type='login', timestamp=base_time - timedelta(minutes=30),
                   ip_address='192.168.1.101', status='normal', description='Login after failed attempts'),
        ActivityLog(user_id=4, activity_type='login', timestamp=base_time - timedelta(hours=3),
                   ip_address='192.168.1.102', status='normal'),
        ActivityLog(user_id=4, activity_type='file_access', timestamp=base_time - timedelta(hours=2.5),
                   description='Accessed: salary_report.xlsx', status='suspicious'),
        ActivityLog(user_id=5, activity_type='login', timestamp=base_time - timedelta(hours=4),
                   ip_address='192.168.1.103', status='normal'),
        ActivityLog(user_id=5, activity_type='logout', timestamp=base_time - timedelta(hours=3),
                   description='Normal logout'),
    ]
    
    for activity in activities:
        db.session.add(activity)
    
    db.session.commit()
    print(f"✓ Created {len(activities)} sample activity logs")
    
    # Create sample escalation logs
    print("--- Adding Sample Escalation Logs ---")
    
    escalations = [
        EscalationLog(user_id=2, escalation_type='unauthorized_role_switch', 
                     attempted_role='admin', current_role='user',
                     timestamp=base_time - timedelta(days=1),
                     description='User attempted to switch to admin role',
                     severity='high', status='blocked'),
        EscalationLog(user_id=3, escalation_type='admin_access_attempt',
                     attempted_role='admin', current_role='user',
                     timestamp=base_time - timedelta(hours=5),
                     description='Unauthorized admin panel access attempt',
                     severity='critical', status='blocked'),
    ]
    
    for escalation in escalations:
        db.session.add(escalation)
    
    db.session.commit()
    print(f"✓ Created {len(escalations)} sample escalation logs")
    
    # Create sample data access logs
    print("--- Adding Sample Data Access Logs ---")
    
    data_accesses = [
        DataAccessLog(user_id=2, file_name='project_code.zip', access_type='download',
                     file_size=5120, timestamp=base_time - timedelta(hours=2),
                     is_suspicious=False, risk_level='low', destination='local'),
        DataAccessLog(user_id=4, file_name='employee_list.xlsx', access_type='download',
                     file_size=1024, timestamp=base_time - timedelta(hours=2.5),
                     is_suspicious=True, risk_level='medium', destination='local'),
        DataAccessLog(user_id=4, file_name='salary_report.xlsx', access_type='copy',
                     file_size=2048, timestamp=base_time - timedelta(hours=2),
                     is_suspicious=True, risk_level='high',
                     destination='external_email'),
        DataAccessLog(user_id=5, file_name='database_backup.sql', access_type='download',
                     file_size=10240, timestamp=base_time - timedelta(hours=3),
                     is_suspicious=True, risk_level='critical',
                     destination='usb_device'),
        DataAccessLog(user_id=2, file_name='config.json', access_type='read',
                     file_size=50, timestamp=base_time - timedelta(hours=1.5),
                     is_suspicious=False, risk_level='low', destination='local'),
    ]
    
    for access in data_accesses:
        db.session.add(access)
    
    db.session.commit()
    print(f"✓ Created {len(data_accesses)} sample data access logs")
    
    # Create sample security policies
    print("--- Adding Sample Security Policies ---")
    
    policies = [
        SecurityPolicy(policy_type='password_policy', title='Strong Password Requirements',
                      description='All users must use passwords with at least 12 characters',
                      recommendation='Enforce strong password policy - minimum 12 characters, mix of uppercase, lowercase, numbers, and special characters',
                      priority='high'),
        SecurityPolicy(policy_type='access_control', title='Role-Based Access Control (RBAC)',
                      description='Implement strict role-based access control',
                      recommendation='Ensure principle of least privilege - users should only have access to data needed for their role',
                      priority='critical'),
        SecurityPolicy(policy_type='login_restrictions', title='Login Restrictions',
                      description='Restrict login attempts and monitor for suspicious patterns',
                      recommendation='Implement account lockout after 5 failed login attempts, enable 2FA for admin accounts',
                      priority='high'),
        SecurityPolicy(policy_type='monitoring_policy', title='Activity Monitoring',
                      description='Monitor and log all user activities',
                      recommendation='Enable comprehensive logging of all file accesses, failed login attempts, and privilege escalation attempts',
                      priority='critical'),
        SecurityPolicy(policy_type='data_protection', title='Data Protection Policy',
                      description='Protect sensitive data from unauthorized access and exfiltration',
                      recommendation='Implement DLP (Data Loss Prevention), restrict large file downloads, monitor external transfers',
                      priority='critical'),
    ]
    
    for policy in policies:
        db.session.add(policy)
    
    db.session.commit()
    print(f"✓ Created {len(policies)} sample security policies")
    
    # Create sample alerts
    print("--- Adding Sample Alerts ---")
    
    alerts = [
        Alert(alert_type='suspicious_activity', user_id=3, 
             title='Multiple Failed Login Attempts', 
             description='User sarah_sales had 3 failed login attempts in 10 minutes',
             severity='high', status='open', timestamp=base_time - timedelta(minutes=35)),
        Alert(alert_type='exfiltration', user_id=4,
             title='Suspicious Data Download',
             description='User mike_hr downloaded salary_report.xlsx and attempted transfer to external email',
             severity='critical', status='open', timestamp=base_time - timedelta(hours=2)),
        Alert(alert_type='escalation', user_id=2,
             title='Unauthorized Role Switch Attempt',
             description='User john_dev attempted to switch to admin role',
             severity='high', status='acknowledged', timestamp=base_time - timedelta(days=1)),
        Alert(alert_type='exfiltration', user_id=5,
             title='Critical: Large Database File Transfer',
             description='User alice_finance transferred 10MB database backup to USB device',
             severity='critical', status='open', timestamp=base_time - timedelta(hours=3)),
    ]
    
    for alert in alerts:
        db.session.add(alert)
    
    db.session.commit()
    print(f"✓ Created {len(alerts)} sample alerts")
    
    print("\n✓ All sample data added successfully!")
    print("\n--- Test Account Credentials ---")
    print("Admin Account:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nRegular Users (same password for all):")
    print("  Usernames: john_dev, sarah_sales, mike_hr, alice_finance")
    print("  Password: user123")
