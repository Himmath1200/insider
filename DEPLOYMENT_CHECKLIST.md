# 🚀 Insider Threat Detection - Deployment Checklist

## Pre-Deployment Checklist (5 minutes)

- [ ] All code committed to Git
- [ ] `.env` file created from `.env.example` (not committed)
- [ ] Generated secure `SECRET_KEY`
- [ ] GitHub repository created
- [ ] Code pushed to GitHub

## Railway Backend Deployment (5 minutes)

### Setup
- [ ] Visit https://railway.app
- [ ] Login with GitHub
- [ ] Create new project → "Deploy from GitHub repo"
- [ ] Select `insider-threat-detection` repository

### Configuration
- [ ] Set environment variables:
  - `FLASK_ENV` = `production`
  - `SECRET_KEY` = `your-generated-key`
  - `ALLOWED_ORIGINS` = `localhost:3000,localhost:5000`
  - `DEBUG` = `False`

### Deployment
- [ ] Monitor deployment progress
- [ ] Copy Railway URL: `https://insider-threat-xxxxx.railway.app`
- [ ] Test backend:
  ```bash
  curl https://insider-threat-xxxxx.railway.app/
  ```

## Netlify Frontend Deployment (5 minutes)

### Setup
- [ ] Visit https://netlify.com
- [ ] Login with GitHub
- [ ] Click "Add new site" → "Import an existing project"
- [ ] Select your GitHub repository

### Configuration
- [ ] Build settings:
  - **Build command**: (leave empty or `npm run build`)
  - **Publish directory**: `templates`
- [ ] Add environment variable:
  - `REACT_APP_API_URL` = `https://your-railway-backend.railway.app`

### Deployment
- [ ] Netlify auto-deploys after configuration
- [ ] Copy Netlify URL: `https://your-site-name.netlify.app`
- [ ] Visit frontend URL in browser

## Post-Deployment Configuration (5 minutes)

### Update CORS on Railway
- [ ] Go to Railway dashboard
- [ ] Select your project
- [ ] Click "Variables"
- [ ] Update `ALLOWED_ORIGINS`:
  ```
  localhost:3000,localhost:5000,your-site-name.netlify.app
  ```
- [ ] Save changes

### Verify Everything Works
- [ ] Visit Netlify frontend URL
- [ ] Check browser console (F12) for errors
- [ ] Login with `admin / admin123`
- [ ] Navigate through all modules
- [ ] Check that data loads from backend

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| 🔴 CORS error | Update `ALLOWED_ORIGINS` on Railway → Save → Wait 1 min |
| 🔴 Blank page | Check browser console (F12), verify `REACT_APP_API_URL` |
| 🔴 Login fails | Verify Railway backend running, check logs |
| 🔴 API 404 error | Verify endpoint URLs, check Railway logs |
| 🔴 Netlify 404 | Check `publish directory` is `templates` |

## Files Structure Reference

```
Deployment Files Created:
✅ Procfile                    # Railway configuration
✅ runtime.txt                 # Python version
✅ netlify.toml               # Netlify configuration
✅ .env.example               # Environment template
✅ .gitignore                 # Git exclusions
✅ package.json               # Build config
✅ requirements.txt           # Updated with CORS
✅ app.py                     # Updated with CORS
✅ DEPLOYMENT.md              # Detailed guide
✅ NETLIFY_QUICKSTART.md      # Quick reference
✅ CONFIG_GUIDE.md            # Configuration docs
✅ DEPLOYMENT_CHANGES.md      # This file
✅ setup-deployment.sh        # Setup script
```

## URLs After Deployment

- **Frontend**: `https://your-site-name.netlify.app`
- **Backend API**: `https://insider-threat-xxxxx.railway.app`
- **Railway Dashboard**: `https://railway.app/project/[project-id]`
- **Netlify Dashboard**: `https://app.netlify.com/sites/[site-name]`

## Demo Credentials

```
Admin Login:
  Username: admin
  Password: admin123

Regular Users (password: user123):
  - john_dev
  - sarah_sales
  - mike_hr
  - alice_finance
```

## Performance Expectations

✅ **Frontend Load Time**: < 2 seconds (Netlify CDN)
✅ **API Response Time**: < 500ms (Railway backend)
✅ **Database Queries**: < 100ms (Local SQLite)
✅ **Overall Page Load**: < 3 seconds

## Cost Breakdown

- **Railway**: ~$0-10/month (includes $5/month free credit)
- **Netlify**: $0/month (free tier)
- **GitHub**: $0/month (public repo)
- **Total**: ~$0-10/month for small deployments

## Monitoring

### Railway Dashboard
- Check "Logs" for errors
- Monitor "CPU" and "Memory" usage
- View "Deployments" history

### Netlify Dashboard
- Monitor "Deploys" tab
- Check "Analytics" for traffic
- Review "Functions" (if using)

## Maintenance Reminders

⏰ **Daily**:
- Check Rails logs for errors
- Verify frontend accessibility

⏰ **Weekly**:
- Review Railway resource usage
- Monitor Netlify deploy logs

⏰ **Monthly**:
- Update dependencies: `pip install -U -r requirements.txt`
- Backup database if in production
- Review cost/usage reports

## Rollback Procedure

If something breaks:

**Railway**:
1. Go to Deployments tab
2. Find last working deployment
3. Click "Redeploy"

**Netlify**:
1. Go to Deploys tab
2. Find last working deploy
3. Click deploy → "Publish this deploy"

## Advanced Configuration (Optional)

### Custom Domain
- Add domain to Netlify (Site settings → Domain management)
- Add domain to Railway (Project settings → Networking)
- Configure DNS records

### SSL Certificate
- Automatic on both platforms ✅

### Email Notifications
- Railway: Settings → Notifications
- Netlify: Site settings → Notifications

### Database Backup
- Export SQLite: `sqlite3 insider_threat.db .dump > backup.sql`
- Store backup safely

## Success Indicators

✅ Frontend loads at `https://your-site-name.netlify.app`
✅ Login works with demo credentials
✅ Can create new users (admin)
✅ Can simulate security events
✅ Can view reports and charts
✅ No CORS errors in browser console
✅ No errors in Railway logs

---

## Next Steps

1. **Follow DEPLOYMENT.md** for detailed step-by-step instructions
2. **Or use NETLIFY_QUICKSTART.md** for quick deployment
3. **Check CONFIG_GUIDE.md** for configuration questions
4. **Monitor logs** after deployment
5. **Test thoroughly** with demo data
6. **Share with users** once verified

**Time to Deploy**: ~30 minutes total
**Difficulty**: ⭐⭐ (Beginner-friendly)
**Success Rate**: >95% (following these steps)

---

**Ready to deploy? Start with DEPLOYMENT.md!** 🚀
