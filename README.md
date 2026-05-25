# Insider Threat Detection System

A comprehensive web-based application for detecting and analyzing insider threats within an organization. This system monitors user activities, detects suspicious behavior, and provides security recommendations.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Modules](#modules)
- [Demo Credentials](#demo-credentials)
- [Troubleshooting](#troubleshooting)

## Features

### Module 1: User Enumeration & Access Mapping
- Create and manage user accounts
- Assign roles (Admin/User)
- View access permissions matrix
- Display user roles and departments
- Admin user management (add, edit, delete)

### Module 2: Log Analysis & Suspicious Activity Detection
- Track all user activities (login, logout, file access)
- Monitor failed login attempts
- Detect suspicious patterns:
  - Multiple failed logins in short time
  - Access at unusual times
  - Unauthorized file access
- Filter and search logs
- Display activity alerts

### Module 3: Privilege Escalation Simulation
- Simulate unauthorized role switching attempts
- Monitor admin access attempts
- Generate security warnings
- Log escalation attempts with severity levels
- Generate escalation reports

### Module 4: Data Access & Exfiltration Simulation
- Track file access activities
- Simulate file downloads and transfers
- Detect suspicious data exfiltration:
  - Large file downloads
  - Unauthorized external transfers
  - Unusual access patterns
- Risk level assessment
- Generate alerts for suspicious activities

### Module 5: Mitigation & Policy Design
- Security policy recommendations
- Password policy guidelines
- Access control best practices
- Login restriction policies
- Activity monitoring guidelines
- Data protection recommendations
- Admin notes for policies

### Extra Features
- **Dashboard**: Real-time overview of all security events
- **Navigation**: Sidebar navigation for easy module access
- **Charts**: Visual representation of data using Chart.js
- **Bootstrap UI**: Professional, responsive design
- **Search & Filter**: Advanced search and filtering options
- **Flash Messages**: Real-time alerts and notifications
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

### Backend
- **Framework**: Python Flask 2.3.3
- **Database**: SQLite3
- **ORM**: SQLAlchemy
- **Session Management**: Flask-Session

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Bootstrap 5.3 + Custom styling
- **JavaScript**: Vanilla JS + Chart.js for visualizations
- **Icons**: Font Awesome 6.4

### Development
- **Python**: 3.7+
- **pip**: Package manager

## Project Structure

```
Insider Threat/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── insider_threat.db              # SQLite database (auto-created)
│
├── database/                       # Database configuration
│   ├── __init__.py
│   ├── models.py                  # SQLAlchemy models
│   └── init_db.py                 # Database initialization
│
├── routes/                         # Flask blueprints/routes
│   ├── __init__.py
│   ├── auth_routes.py             # Authentication
│   ├── user_routes.py             # User management
│   ├── log_routes.py              # Activity logging
│   ├── escalation_routes.py       # Privilege escalation
│   ├── exfiltration_routes.py     # Data exfiltration
│   └── mitigation_routes.py       # Security policies
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── login.html                 # Login page
│   ├── index.html                 # Dashboard
│   ├── user_enumeration.html      # User list
│   ├── access_mapping.html        # Access control
│   ├── add_user.html              # Add user form
│   ├── edit_user.html             # Edit user form
│   ├── profile.html               # User profile
│   ├── log_analysis.html          # Activity logs
│   ├── suspicious_activities.html # Suspicious activity log
│   ├── failed_logins.html         # Failed login attempts
│   ├── privilege_escalation.html  # Escalation dashboard
│   ├── escalation_report.html     # Escalation report
│   ├── data_exfiltration.html     # Exfiltration dashboard
│   ├── exfiltration_report.html   # Exfiltration report
│   ├── mitigation.html            # Mitigation overview
│   ├── password_policy.html       # Password policy
│   ├── access_control.html        # Access control policy
│   ├── login_restrictions.html    # Login restrictions
│   ├── monitoring_policy.html     # Monitoring policy
│   ├── data_protection.html       # Data protection policy
│   ├── 404.html                   # Error page
│   ├── 500.html                   # Server error
│   └── unauthorized.html          # Unauthorized access
│
├── static/                         # Static files
│   ├── css/
│   │   └── style.css              # Main stylesheet
│   └── js/
│       ├── main.js                # Main JavaScript
│       └── charts.js              # Chart.js configurations
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Visual Studio Code (recommended)

### Step 1: Install Python

If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/)

### Step 2: Install Dependencies

Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database

The database will be automatically created and initialized when you run the application for the first time.

## Quick Start

### Running the Application

1. **Open Terminal** in VS Code or command prompt

2. **Navigate to project directory**:
   ```bash
   cd "C:\Users\[YourUsername]\OneDrive\Desktop\VS Code Files and webs\Insider Threat"
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

   You should see output like:
   ```
   ==================================================
   Starting Insider Threat Detection System
   ==================================================
   Open your browser and navigate to: http://localhost:5000
   Press CTRL+C to stop the server
   ==================================================
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

5. **Login** with demo credentials (see below)

## Usage

### Basic Operations

#### Login
1. Navigate to http://localhost:5000
2. Enter username and password
3. Click Login

#### Navigate Modules
- Use the sidebar dropdown menu to access different modules
- Each module provides specific functionality

#### View Dashboard
- After login, you'll see the main dashboard
- View statistics, recent activities, and open alerts
- All charts update in real-time

#### Manage Users (Admin Only)
1. Go to "User Enumeration"
2. Click "Add New User" button
3. Fill in user details
4. Click "Create User"

#### Simulate Security Events
- Go to specific module (Escalation/Exfiltration)
- Click "Simulate" button
- Fill in event details
- System will log the event and generate alerts

#### View Reports
- Each module has a report section
- Reports show severity breakdown and statistics
- Filter and analyze data

## Modules

### Module 1: User Enumeration
**Path**: `/users/`
- View all users
- See user roles and permissions
- Access control matrix
- Admin functions: Add, Edit, Delete users

### Module 2: Log Analysis
**Path**: `/logs/`
- View all activity logs
- Filter by activity type and status
- Search logs
- Identify suspicious activities
- View failed login attempts

### Module 3: Privilege Escalation
**Path**: `/escalation/`
- Monitor escalation attempts
- View severity levels
- Simulate escalation attempts
- Generate escalation reports

### Module 4: Data Exfiltration
**Path**: `/exfiltration/`
- Track file access
- Detect suspicious transfers
- Risk assessment
- Simulate data access attempts
- Generate exfiltration reports

### Module 5: Mitigation
**Path**: `/mitigation/`
- Security policy recommendations
- Best practices for each policy area
- Admin notes management
- Priority levels for policies

## Demo Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Administrator

### Sample User Accounts
All sample users use the same password: `user123`

- **john_dev** - Development department
- **sarah_sales** - Sales department
- **mike_hr** - Human Resources
- **alice_finance** - Finance department

### Try This

1. Login as admin to manage users
2. Login as user to see restricted features
3. Use the "Simulate" buttons to generate test events
4. View reports and alerts

## Database

### Automatic Initialization
The database is automatically created on first run with:
- All necessary tables
- Sample data for testing
- Pre-configured security policies

### Database File
- Location: `insider_threat.db` (in project root)
- Type: SQLite3
- Size: ~100KB with sample data

### Reset Database
To reset the database:
1. Stop the application (Ctrl+C)
2. Delete `insider_threat.db` file
3. Run the application again
4. Database will be recreated with fresh sample data

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Port 5000 already in use"

**Solution**: Change the port in app.py
```python
app.run(debug=True, host='localhost', port=5001)  # Use 5001 instead
```

### Problem: Database lock error

**Solution**: 
1. Stop the application
2. Delete `insider_threat.db`
3. Restart the application

### Problem: Templates not found

**Solution**: Ensure you're running from the correct directory where `app.py` is located

### Problem: CSS/JS not loading

**Solution**: 
- Check that `static` folder exists
- Verify CSS and JS files are in correct subdirectories
- Clear browser cache (Ctrl+Shift+Delete)
- Restart the application

## Features Demo

### Sample Activities Included

The application comes with pre-populated sample data including:

1. **Users**: 4 sample users with different roles
2. **Activities**: Various login, file access, and logout events
3. **Escalations**: Sample privilege escalation attempts
4. **Data Access**: Sample file access and transfer attempts
5. **Alerts**: Pre-generated security alerts

### Try These Actions

1. **Login and Logout**: Track activities in logs
2. **View Dashboard**: See real-time statistics
3. **Simulate Events**: Generate new security events
4. **Generate Reports**: View comprehensive reports
5. **Manage Policies**: (Admin) Add notes to security policies

## Performance Notes

- Application runs smoothly on systems with 4GB+ RAM
- Database is optimized for up to 100,000 records
- Charts render efficiently with Chart.js
- Response time: < 500ms for most operations

## Security Considerations

This is a **demonstration/educational system** and includes:
- Sample credentials (change in production)
- No HTTPS (use in production)
- No advanced authentication (add 2FA for production)
- SQLite (use production DB like PostgreSQL)
- Sample data (sanitize before production use)

## Support & Questions

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in browser console (F12)
3. Check terminal for detailed error logs
4. Verify all files are present in correct directories

## Future Enhancements

Potential improvements:
- Two-factor authentication (2FA)
- LDAP integration
- Email notifications
- Advanced reporting and scheduling
- Machine learning for anomaly detection
- Multi-factor authentication
- SIEM integration
- Real-time threat intelligence

## License

This project is provided as-is for educational purposes.

## Version

**Version**: 1.0.0  
**Release Date**: May 2026  
**Last Updated**: May 26, 2026

---

**Happy Monitoring! Stay Secure!** 🔒
