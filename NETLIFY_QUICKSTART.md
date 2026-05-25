# Netlify Deployment Quick Start

This document provides step-by-step instructions specifically for deploying to Netlify.

## Quick Summary

Your app uses a **split architecture**:
- **Backend** (Flask API) → Deploy to **Railway** or **Render**
- **Frontend** (HTML/CSS/JS) → Deploy to **Netlify**

## Why Split Architecture?

Netlify is designed for static sites and serverless functions. Flask is a server-side framework that requires:
- Persistent runtime (your Flask app running continuously)
- Database connection
- Background tasks

**Solution**: Run Flask on Railway (which supports full Python server runtime), and serve frontend from Netlify.

## Deployment Steps

### 1. Set Up Git & GitHub

```bash
cd "your-project-directory"
git init
git add .
git commit -m "Initial commit"

# Push to GitHub (create repo first at github.com)
git remote add origin https://github.com/YOUR_USERNAME/insider-threat-detection.git
git push -u origin main
```

### 2. Deploy Backend to Railway (5 minutes)

1. Visit https://railway.app
2. Login with GitHub
3. Create New Project → Deploy from GitHub
4. Select your `insider-threat-detection` repo
5. Set environment variables:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (generate random value)
   - `ALLOWED_ORIGINS` = `your-netlify-domain.netlify.app`
6. Copy your Railway URL (example: `https://insider-threat-xxxxx.railway.app`)

### 3. Deploy Frontend to Netlify (5 minutes)

1. Visit https://netlify.com
2. Login with GitHub
3. "Add new site" → "Import an existing project"
4. Select your GitHub repo
5. Build settings:
   - **Build command**: (leave empty)
   - **Publish directory**: `templates`
6. Set environment variable:
   - `REACT_APP_API_URL` = `https://your-railway-backend.railway.app`
7. Deploy!

### 4. Update CORS on Railway

After getting your Netlify domain:
1. Go to Railway dashboard
2. Project settings → Variables
3. Update `ALLOWED_ORIGINS` to include your Netlify domain

### 5. Test

1. Visit your Netlify URL
2. Login with: admin / admin123
3. Check browser console (F12) for any errors

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "CORS error" | Update `ALLOWED_ORIGINS` on Railway to include Netlify domain |
| "Cannot reach API" | Verify Railway is running, check API URL in frontend |
| "Blank page" | Check browser console (F12), look for errors |
| "Login not working" | Verify backend database initialized correctly |

## Files for Netlify Deployment

✅ `netlify.toml` - Netlify configuration (already created)
✅ `Procfile` - Railway configuration (already created)
✅ `.env.example` - Environment template (already created)
✅ `requirements.txt` - Python dependencies updated with CORS support

## What Gets Deployed Where

**Railway Backend**:
- `app.py`
- `database/` folder
- `routes/` folder
- `requirements.txt`

**Netlify Frontend**:
- `templates/` folder (HTML files)
- `static/css/` (stylesheets)
- `static/js/` (JavaScript)

## After Deployment

- ✅ Backend runs 24/7 on Railway
- ✅ Frontend served from Netlify CDN (fast everywhere)
- ✅ API calls go from frontend → backend
- ✅ Database lives on Railway backend

## Cost Breakdown

- **Railway**: ~$5/month (free tier) or pay-as-you-go
- **Netlify**: Free tier includes 300 build minutes/month
- **Total**: Extremely affordable for small projects

## Maintenance

- Monitor Railway logs for errors
- Check Netlify deploy logs if frontend has issues
- Keep GitHub repo updated with changes
- Both platforms auto-deploy on git push

## Need Help?

See `DEPLOYMENT.md` for detailed step-by-step instructions with troubleshooting.
