# Insider Threat Detection System - Deployment Guide

This guide shows you how to deploy your Insider Threat Detection System with:
- **Backend API**: Railway (Flask + SQLite)
- **Frontend**: Netlify (Static assets)

## Prerequisites

Before deploying, ensure you have:
- GitHub account (for version control)
- Railway account (free at railway.app)
- Netlify account (free at netlify.com)
- Git installed locally

## Architecture

```
┌─────────────────────────┐
│  Netlify (Frontend)     │
│  - HTML, CSS, JS        │
│  - React/Vue (optional) │
└────────┬────────────────┘
         │ API Calls
         ↓
┌─────────────────────────┐
│  Railway (Backend)      │
│  - Flask API            │
│  - SQLite Database      │
│  - Business Logic       │
└─────────────────────────┘
```

## Part 1: Prepare for Git & GitHub

### Step 1: Initialize Git Repository

```bash
cd "C:\Users\[YourUsername]\OneDrive\Desktop\VS Code Files and webs\Insider Threat"
git init
git add .
git commit -m "Initial commit: Insider Threat Detection System"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Name it: `insider-threat-detection`
4. Click "Create Repository"
5. Follow the commands shown on GitHub to push your code

```bash
git remote add origin https://github.com/YOUR_USERNAME/insider-threat-detection.git
git branch -M main
git push -u origin main
```

## Part 2: Deploy Backend to Railway

### Step 1: Connect Railway to GitHub

1. Go to [Railway.app](https://railway.app)
2. Sign up or login (use GitHub for easier signup)
3. Click "Create New Project"
4. Select "Deploy from GitHub repo"
5. Authorize Railway to access your GitHub
6. Select your `insider-threat-detection` repository

### Step 2: Configure Environment Variables on Railway

1. In Railway project dashboard, click "Variables"
2. Add these environment variables:

```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=[Generate a random string: python -c "import secrets; print(secrets.token_hex(32))"]
ALLOWED_ORIGINS=localhost:3000,your-netlify-domain.netlify.app
```

### Step 3: Monitor Deployment

1. Click "Deployments" tab
2. Watch as Railway automatically builds and deploys your app
3. Once complete, you'll get a URL like: `https://insider-threat-xxxxx.railway.app`

**Save this URL** - you'll need it for the frontend!

### Step 4: Test Backend API

```bash
# Get the Railway URL
https://insider-threat-xxxxx.railway.app

# Test it's working
curl https://insider-threat-xxxxx.railway.app/
# Should redirect to login
```

## Part 3: Create Frontend for Netlify

### Step 1: Create Frontend Distribution

The frontend files need to be in a `dist` folder. Create a simple index.html that will be deployed to Netlify:

```bash
# Create dist folder
mkdir dist
```

### Step 2: Copy Frontend Files

Your HTML templates will be served as static files. Update the frontend to make API calls to your Railway backend.

### Step 3: Create Environment File for Frontend

Create `.env.production` for the production frontend URL:

```
VITE_API_URL=https://your-railway-backend.railway.app
REACT_APP_API_URL=https://your-railway-backend.railway.app
```

## Part 4: Deploy Frontend to Netlify

### Step 1: Connect Netlify to GitHub

1. Go to [Netlify.com](https://netlify.com)
2. Sign up or login (use GitHub for easier signup)
3. Click "Add new site" → "Import an existing project"
4. Select "GitHub"
5. Authorize Netlify to access your GitHub
6. Select `insider-threat-detection` repository

### Step 2: Configure Build Settings

When prompted for build settings:

**Build Command**: `npm run build` (or leave blank if no build needed)
**Publish Directory**: `dist` (or `public` depending on setup)

**Or manually configure:**

1. Click "Site settings"
2. Go to "Build & Deploy" → "Continuous Deployment"
3. Set:
   - **Build command**: (leave empty for static files)
   - **Publish directory**: `dist`

### Step 3: Add Environment Variables

1. In Netlify dashboard, click "Site settings"
2. Go to "Build & Deploy" → "Environment"
3. Add environment variables:

```
REACT_APP_API_URL=https://your-railway-backend.railway.app
```

### Step 4: Deploy

1. Commit and push any changes to GitHub:

```bash
git add .
git commit -m "Prepare for Netlify deployment"
git push
```

2. Netlify will automatically deploy when you push to GitHub
3. Your site will be available at: `https://your-site-name.netlify.app`

## Part 5: Update CORS Settings

### On Railway Backend

Update the `ALLOWED_ORIGINS` environment variable to include your Netlify domain:

```
ALLOWED_ORIGINS=localhost:3000,localhost:5000,your-site-name.netlify.app
```

## Part 6: Connect Frontend to Backend

### Update API Base URL

In your frontend JavaScript, update the API base URL:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Make API calls
fetch(`${API_BASE_URL}/api/dashboard-stats`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## Part 7: Testing Deployment

### Test Backend

```bash
# Get your Railway URL from the dashboard
curl https://insider-threat-xxxxx.railway.app/auth/login
# Should show login page or redirect
```

### Test Frontend

1. Visit your Netlify domain: `https://your-site-name.netlify.app`
2. Check browser console (F12) for any API errors
3. Login with demo credentials:
   - **Admin**: admin / admin123
   - **User**: john_dev / user123

### Troubleshoot

**CORS Errors**: 
- Check `ALLOWED_ORIGINS` on Railway includes your Netlify domain
- Verify API URL in frontend matches Railway backend

**API Calls Failing**:
- Verify Railway backend is running (check deployments)
- Check API_URL environment variable in frontend
- Check browser console (F12) for actual error messages

## Part 8: Custom Domain (Optional)

### Add Custom Domain to Netlify

1. Go to Netlify Site settings
2. Click "Domain management"
3. Click "Add custom domain"
4. Follow the DNS setup instructions

### Add Custom Domain to Railway

1. Go to Railway project settings
2. Click "Networking"
3. Add your custom domain
4. Configure DNS

## Monitoring & Maintenance

### Railway Dashboard
- **Logs**: View real-time logs of your backend
- **Metrics**: Monitor CPU, memory, requests
- **Deployments**: See deployment history

### Netlify Dashboard
- **Deploys**: View deployment history
- **Analytics**: Monitor site traffic
- **Functions**: View serverless function logs

## Environment Variables Quick Reference

### Railway (Backend)
```
FLASK_ENV=production
SECRET_KEY=your-random-secret
ALLOWED_ORIGINS=your-netlify-domain.netlify.app
DEBUG=False
```

### Netlify (Frontend)
```
REACT_APP_API_URL=https://your-railway-backend.railway.app
```

## Costs

### Railway
- **Free Tier**: $5/month credit (usually sufficient for demo/small projects)
- **Pay-as-you-go**: After free tier expires (~$0.50 per active hour)

### Netlify
- **Free Tier**: Unlimited sites, 300 build minutes/month
- **Pro**: $19/month for higher limits

## Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] Railway project created and connected
- [ ] Environment variables set on Railway
- [ ] Backend API tested and working
- [ ] Railway URL obtained
- [ ] Netlify project created and connected
- [ ] Frontend CORS origin updated
- [ ] Frontend API URL updated
- [ ] Netlify domain configured
- [ ] End-to-end testing completed
- [ ] Demo credentials working
- [ ] All modules accessible from frontend

## Rollback Instructions

### If Deployment Breaks

**Railway Backend:**
1. Go to Railway dashboard
2. Click "Deployments"
3. Select previous successful deployment
4. Click "Revert"

**Netlify Frontend:**
1. Go to Netlify dashboard
2. Click "Deploys"
3. Click on previous successful deploy
4. Click "Publish deploy"

## Performance Tips

- **Railway**: Monitor resource usage in dashboard
- **Netlify**: Enable caching for assets (already in netlify.toml)
- **Database**: Regular backups recommended
- **Logs**: Clean up old logs regularly

## Security Reminders

⚠️ **Before Production:**
1. Change `SECRET_KEY` to a secure random value
2. Set `DEBUG=False` (already done in production config)
3. Configure HTTPS (automatic on both platforms)
4. Use strong passwords for test accounts
5. Enable 2FA on Railway and Netlify accounts
6. Keep dependencies updated
7. Review CORS origins list

## Support & Troubleshooting

### Railway Support
- Docs: https://docs.railway.app
- Status: https://railway.app/status
- Discord: Railway community Discord

### Netlify Support
- Docs: https://docs.netlify.com
- Community: Netlify forums and Discord

## Next Steps

1. **Monitor Performance**: Watch backend logs and frontend analytics
2. **User Feedback**: Gather feedback from testers
3. **Improvements**: Fix bugs and add features
4. **Scale**: If traffic increases, upgrade plans

---

**Deployment Complete!** Your Insider Threat Detection System is now live on the internet. 🚀
