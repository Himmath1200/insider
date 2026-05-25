# Deployment Configuration Guide

This document explains all configuration files and environment variables needed for deployment.

## Configuration Files

### 1. `.env` (Main Configuration File)

**Location**: Project root
**Created from**: `.env.example`
**Purpose**: Stores sensitive configuration values

**Example content**:
```
FLASK_ENV=production
FLASK_APP=app.py
DEBUG=False
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=sqlite:///insider_threat.db
SESSION_TYPE=filesystem
PERMANENT_SESSION_LIFETIME=1800
FRONTEND_URL=https://your-domain.netlify.app
ALLOWED_ORIGINS=your-domain.netlify.app,localhost:3000
API_PORT=5000
API_HOST=0.0.0.0
```

### 2. `Procfile` (Railway/Heroku Deployment)

**Location**: Project root
**Purpose**: Tells Railway how to run your app
**Content**:
```
web: gunicorn app:app
```

### 3. `runtime.txt` (Python Version)

**Location**: Project root
**Purpose**: Specifies Python version for Railway
**Content**:
```
python-3.11.0
```

### 4. `netlify.toml` (Netlify Configuration)

**Location**: Project root
**Purpose**: Configures Netlify build and deployment
**Key sections**:
- `[build]`: Build command and output directory
- `[build.environment]`: Environment variables for frontend
- `[[redirects]]`: URL routing for single-page apps
- `[[headers]]`: HTTP headers for security and caching

### 5. `package.json` (Node.js/Build Configuration)

**Location**: Project root
**Purpose**: (Optional) For npm-based frontend builds
**Scripts**:
```json
{
  "scripts": {
    "build": "prepare frontend files",
    "dev": "development command",
    "start": "production command"
  }
}
```

### 6. `.gitignore` (Git Exclusions)

**Location**: Project root
**Purpose**: Tells Git which files to ignore
**Ignores**:
- `__pycache__/` - Python cache
- `.env` - Sensitive environment variables
- `*.db` - SQLite databases
- `node_modules/` - npm packages
- `.vscode/` - IDE settings

## Environment Variables

### Backend Variables (Railway)

| Variable | Value | Example |
|----------|-------|---------|
| `FLASK_ENV` | `production` or `development` | `production` |
| `DEBUG` | `False` (production) or `True` (dev) | `False` |
| `SECRET_KEY` | Random secret string (32+ chars) | `a3f8k9x2m5n1p7q4r9s2t3u4v5w6x7y8` |
| `ALLOWED_ORIGINS` | Comma-separated domains | `mydomain.netlify.app,localhost:3000` |
| `DATABASE_URL` | Database connection string | `sqlite:///insider_threat.db` |
| `API_PORT` | Port for Flask server | `5000` |
| `API_HOST` | Host address | `0.0.0.0` |

### Frontend Variables (Netlify)

| Variable | Value | Example |
|----------|-------|---------|
| `REACT_APP_API_URL` | Backend API URL | `https://your-backend.railway.app` |
| `NODE_VERSION` | Node version for build | `18.0.0` |

## Generating a Secure SECRET_KEY

### Option 1: Python

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Option 2: OpenSSL

```bash
openssl rand -hex 32
```

### Option 3: Online Generator

Use an online tool (make sure to keep it secret!)

**NEVER** share your SECRET_KEY!

## Setting Up Environment Variables

### Local Development

1. Create `.env` file in project root
2. Add your variables
3. Install python-dotenv: `pip install python-dotenv`
4. Variables auto-load when app starts

### Railway

1. Go to Railway dashboard
2. Select your project
3. Click "Variables"
4. Add each variable
5. Click "Save"

### Netlify

1. Go to Netlify dashboard
2. Select your site
3. Site settings → Build & deploy → Environment
4. Add variables
5. New deployments use updated variables

## Deployment Configuration Checklist

- [ ] Created `.env` file from `.env.example`
- [ ] Generated a secure `SECRET_KEY`
- [ ] Set `ALLOWED_ORIGINS` to your Netlify domain
- [ ] Updated `REACT_APP_API_URL` to Railway backend
- [ ] `Procfile` present with `gunicorn app:app`
- [ ] `runtime.txt` specifies Python 3.11
- [ ] `netlify.toml` configured with correct publish directory
- [ ] `.gitignore` excludes `.env` and `.db` files
- [ ] `requirements.txt` includes Flask-CORS and gunicorn
- [ ] GitHub repository created and pushed
- [ ] Environment variables set on Railway
- [ ] Environment variables set on Netlify

## Important Security Notes

⚠️ **NEVER**:
- Commit `.env` file to Git
- Share your `SECRET_KEY`
- Use test credentials in production
- Leave `DEBUG=True` in production
- Forget to update `ALLOWED_ORIGINS`

✅ **ALWAYS**:
- Use environment variables for sensitive data
- Generate a new `SECRET_KEY` for production
- Enable HTTPS (automatic on both platforms)
- Keep dependencies updated
- Monitor deployment logs

## Testing Configuration

Before production deployment, test with:

```bash
# Local testing
FLASK_ENV=development python app.py

# Check environment variables loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.environ.get('SECRET_KEY'))"
```

## Troubleshooting Configuration

| Problem | Solution |
|---------|----------|
| `.env` not loaded | Check file location (project root) and `python-dotenv` installed |
| CORS errors | Verify `ALLOWED_ORIGINS` includes your domain exactly |
| Database not found | Check `DATABASE_URL` is correct and database exists |
| Frontend blank | Check `REACT_APP_API_URL` points to correct backend |
| Build fails on Netlify | Check `package.json` build script is correct |

## Production Checklist

Before going live:

- [ ] `DEBUG=False`
- [ ] `FLASK_ENV=production`
- [ ] Secure `SECRET_KEY` generated
- [ ] HTTPS enabled (automatic)
- [ ] Database backed up
- [ ] Error logging configured
- [ ] Monitoring set up (Railway/Netlify dashboards)
- [ ] Backup deployment plan ready
- [ ] Domain configured (optional)
- [ ] Tests passed

## Configuration Documentation

For platform-specific configuration:
- **Railway**: https://docs.railway.app/guides/environment-variables
- **Netlify**: https://docs.netlify.com/configure-builds/environment-variables

---

**All configuration files are prepared and ready for deployment!**
