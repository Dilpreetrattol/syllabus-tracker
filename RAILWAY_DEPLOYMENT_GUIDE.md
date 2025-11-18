# 🚂 Complete Railway Deployment Guide - Step by Step

This guide will walk you through deploying your Syllabus Tracker to Railway from scratch.

---

## 📋 Prerequisites Checklist

- [x] GitHub repository: `Dilpreetrattol/syllabus-tracker`
- [x] Code pushed to `main` branch
- [x] `requirements.txt` with all dependencies
- [x] `Procfile` configured for Gunicorn
- [x] `runtime.txt` specifying Python version
- [x] `config.py` supports `DATABASE_URL`

---

## 🚀 Step 1: Create Railway Account

### 1.1 Go to Railway
- Open your browser and navigate to: **https://railway.app**

### 1.2 Sign Up with GitHub
- Click **"Login"** or **"Start a New Project"**
- Select **"Login with GitHub"**
- Authorize Railway to access your GitHub account
- Grant permissions when prompted

✅ **Result:** You should now see the Railway dashboard

---

## 📦 Step 2: Create New Project from GitHub

### 2.1 Start New Project
- On the Railway dashboard, click **"New Project"**
- You'll see several options:
  - Deploy from GitHub repo
  - Deploy from template
  - Empty project

### 2.2 Deploy from GitHub
- Click **"Deploy from GitHub repo"**
- Railway will show a list of your repositories

### 2.3 Select Your Repository
- Find and click **`syllabus-tracker`**
- Railway will automatically:
  - Detect it's a Python project
  - Read `runtime.txt` for Python version
  - Start building immediately

### 2.4 Wait for Initial Detection
- Railway creates a **Web Service** automatically
- The service will try to build but will fail initially (missing DATABASE_URL)
- This is expected! ✅

✅ **Result:** You should see a project with one service card labeled "syllabus-tracker" or "web"

---

## 🗄️ Step 3: Add PostgreSQL Database

### 3.1 Add Database Service
- In your Railway project dashboard
- Click **"New"** button (top right)
- Select **"Database"**
- Choose **"Add PostgreSQL"**

### 3.2 Wait for Provisioning
- Railway will create a PostgreSQL instance
- This takes about 30-60 seconds
- You'll see a new card labeled **"Postgres"**

### 3.3 Verify DATABASE_URL is Set
- Click on your **Web Service** (syllabus-tracker)
- Go to **"Variables"** tab
- You should see `DATABASE_URL` already listed (automatically linked)
- Format: `postgresql://postgres:password@host:5432/railway`

✅ **Result:** PostgreSQL database is running and DATABASE_URL is available to your app

---

## ⚙️ Step 4: Configure Environment Variables

### 4.1 Generate SECRET_KEY
Open PowerShell on your local machine and run:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**Copy the output** (it will look like: `8b145bb85b71a6d67086f0c9d717cf6bc14a51a6fd75857f32e452b550081c40`)

### 4.2 Add Variables to Railway
- In your **Web Service**, click **"Variables"** tab
- Click **"New Variable"**

**Add these variables:**

| Variable Name | Value |
|--------------|-------|
| `SECRET_KEY` | (paste the generated key from step 4.1) |
| `FLASK_ENV` | `production` |

### 4.3 Verify All Variables
After adding, you should see:
- ✅ `DATABASE_URL` (automatically set by Railway)
- ✅ `SECRET_KEY` (you just added)
- ✅ `FLASK_ENV` (you just added)

✅ **Result:** All required environment variables are configured

---

## 🔨 Step 5: Deploy the Application

### 5.1 Trigger Deployment
- After adding variables, Railway **automatically redeploys**
- If not, click the **"..."** menu on the Web Service
- Select **"Redeploy"**

### 5.2 Monitor Build Logs
- Click on your **Web Service**
- Go to **"Deployments"** tab
- Click the latest deployment
- Watch the **Build Logs**

**You should see:**
```
Building with Nixpacks...
Installing dependencies from requirements.txt
Successfully installed Flask SQLAlchemy gunicorn...
Build completed successfully
```

### 5.3 Wait for Deployment
- The **Deploy Logs** will show:
```
Starting Gunicorn...
Listening on 0.0.0.0:$PORT
```

### 5.4 Check Service Status
- Go back to project dashboard
- Your Web Service should show **"Active"** with a green indicator

✅ **Result:** Application is deployed and running

---

## 🌐 Step 6: Get Your Public URL

### 6.1 Generate Public Domain
- Click on your **Web Service**
- Go to **"Settings"** tab
- Scroll to **"Networking"** section
- Click **"Generate Domain"**

### 6.2 Copy Your URL
- Railway generates a URL like: `https://syllabus-tracker-production.up.railway.app`
- **Copy this URL** - you'll need it!

✅ **Result:** Your app has a public URL

---

## 🗃️ Step 7: Initialize the Database

Your app is running but the database is empty. Let's set it up.

### 7.1 Open Railway Shell
- In your **Web Service**, click the **"..."** menu
- Select **"Run a command"** or **"Shell"**
- A terminal window opens inside your Railway container

### 7.2 Run Database Migrations
In the Railway shell, type:

```bash
FLASK_APP=app flask db upgrade
```

**Press Enter**

**Expected output:**
- If you have migrations: `Running upgrade -> head`
- If no migrations folder: `Error: Can't locate revision...` (this is OK, proceed)

### 7.3 Create Database Schema
In the Railway shell, type:

```bash
python scripts/create_db.py
```

**Press Enter**

**Expected output:**
```
Database tables created successfully!
Sample data inserted.
Test users created:
- coordinator (username: ug.coordinator, password: password123)
- teacher (username: john.doe, password: password123)
- student (username: alice.smith, password: password123)
```

### 7.4 Exit the Shell
Type `exit` or close the terminal window

✅ **Result:** Database is initialized with schema and test data

---

## ✅ Step 8: Test Your Deployed Application

### 8.1 Open Your App
- Click the **Settings** tab of your Web Service
- Under **Networking**, click your generated domain URL
- **OR** simply visit: `https://your-app.up.railway.app`

### 8.2 Test Login Page
- You should see the login page with the gradient background
- If you see errors, check the Deploy Logs

### 8.3 Login as Coordinator
Use the test credentials created by `create_db.py`:

| Role | Username | Password |
|------|----------|----------|
| UG Coordinator | `ug.coordinator` | `password123` |
| Teacher | `john.doe` | `password123` |
| Student | `alice.smith` | `password123` |

### 8.4 Test Key Features
After logging in as coordinator:

**Dashboard:**
- ✅ Shows total users, subjects, enrollments
- ✅ Recent activity feed

**Users Page:**
- ✅ List of all users
- ✅ Search functionality
- ✅ Create new user button

**Subjects Page:**
- ✅ List of subjects with departments
- ✅ Add/Edit/Delete subjects
- ✅ Manage topics with dates

**Enrollments Page:**
- ✅ Filter by course/semester
- ✅ Upload CSV
- ✅ Download enrollment data

✅ **Result:** Application is fully functional in production!

---

## 🔍 Step 9: Troubleshooting Common Issues

### Issue 1: "Application Error" or 500 Error

**Check Deploy Logs:**
- Web Service → Deployments → Latest → Deploy Logs
- Look for Python errors

**Common causes:**
- Missing `SECRET_KEY` - Add it in Variables
- Database connection failed - Verify `DATABASE_URL` is set
- Import errors - Check requirements.txt has all dependencies

### Issue 2: Database Connection Error

**Verify DATABASE_URL:**
- Web Service → Variables → DATABASE_URL should exist
- Format: `postgresql://postgres:password@host:5432/railway`

**Re-link database:**
- Delete DATABASE_URL variable
- In Postgres service → Settings → Connect → Copy connection string
- Add to Web Service Variables manually

### Issue 3: Build Failed

**Check Build Logs:**
- Look for dependency installation errors
- Ensure `requirements.txt` is in the root directory
- Verify Python version in `runtime.txt` (should be `python-3.11.5`)

**Fix:**
```bash
# Locally, update requirements
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Issue 4: Login Not Working

**Check if database was initialized:**
- Run `python scripts/create_db.py` again in Railway shell

**Verify test users exist:**
```bash
# In Railway shell
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); print([u.username for u in User.query.all()])"
```

### Issue 5: Static Files Not Loading

**Check Deploy Logs:**
- CSS/JS should be served by Flask in production
- Verify paths in base templates: `/static/css/...`

**If issues persist:**
- Check browser console for 404 errors
- Verify file paths are correct in templates

---

## 📊 Step 10: Monitoring and Logs

### 10.1 View Application Logs
- Web Service → **"Logs"** tab
- Shows real-time application output
- Look for:
  - HTTP requests: `GET /login 200`
  - Errors: `500 Internal Server Error`
  - Database queries

### 10.2 View Metrics
- Web Service → **"Metrics"** tab
- Shows:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

### 10.3 Database Metrics
- Postgres service → **"Metrics"** tab
- Shows:
  - Connection count
  - Query performance
  - Storage usage

---

## 🔄 Step 11: Continuous Deployment

### 11.1 Automatic Deploys
Railway is now watching your GitHub repository!

**Any time you push to `main` branch:**
```bash
git add .
git commit -m "Add new feature"
git push
```

**Railway will automatically:**
1. Detect the push
2. Start a new build
3. Deploy the new version
4. Zero-downtime switch

### 11.2 Monitor Deployments
- Web Service → **"Deployments"** tab
- See history of all deployments
- Click any deployment to see its logs

### 11.3 Rollback if Needed
- In Deployments tab
- Click a previous successful deployment
- Click **"Redeploy"**

---

## 🎯 Step 12: Production Best Practices

### 12.1 Custom Domain (Optional)
- Buy a domain (e.g., GoDaddy, Namecheap)
- In Railway: Settings → Networking → Custom Domain
- Add your domain and configure DNS

### 12.2 Environment-Specific Settings
Create different Railway projects for staging/production:
- `syllabus-tracker-staging`
- `syllabus-tracker-production`

### 12.3 Database Backups
- Postgres service → Settings → Enable automated backups
- Or use Railway CLI to export:
```bash
railway pg dump > backup.sql
```

### 12.4 Monitoring and Alerts
- Railway → Project Settings → Notifications
- Get alerts for:
  - Deployment failures
  - High resource usage
  - Crashes

---

## 📝 Quick Reference Commands

### Railway CLI (Optional)
Install Railway CLI for advanced operations:

```powershell
# Install
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run commands
railway run python scripts/add_user.py

# Open shell
railway shell
```

### Common Database Commands (Railway Shell)

```bash
# Create new admin user
python scripts/add_user.py

# Check all users
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); users = User.query.all(); [print(f'{u.username} - {u.role}') for u in users]"

# Reset database (WARNING: deletes all data)
python scripts/reset_db.py
```

---

## 🎉 Success Checklist

After completing this guide, you should have:

- ✅ Railway account connected to GitHub
- ✅ Syllabus Tracker deployed and running
- ✅ PostgreSQL database provisioned and initialized
- ✅ Public URL accessible from anywhere
- ✅ Test users working (coordinator, teacher, student)
- ✅ All features functional (dashboard, CRUD operations)
- ✅ Automatic deployments on git push
- ✅ Access to logs and metrics

---

## 🆘 Getting Help

### Railway Support
- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

### Project-Specific Issues
- Check `PRESENTATION_CHECKLIST.md` for known issues
- Review Deploy Logs in Railway
- Test locally first with `run.ps1 -Debug`

---

## 💰 Railway Pricing

**Free Tier:**
- $5 free credit per month
- Enough for hobby projects and testing
- No credit card required initially

**When you need more:**
- Pay-as-you-go after free credits
- ~$5-10/month for small apps
- Add credit card in Railway settings

---

## 🎓 What You've Learned

- ✅ Deploying Flask apps to cloud platforms
- ✅ Managing PostgreSQL databases in production
- ✅ Environment variable configuration
- ✅ Continuous deployment from GitHub
- ✅ Production debugging and monitoring
- ✅ Database migrations and seeding

---

**🎉 Congratulations! Your Syllabus Tracker is now live on Railway! 🎉**

**Your deployment URL:** `https://[your-service].up.railway.app`

---

## 📱 Share Your Project

- Add the URL to your GitHub README
- Share with your team for testing
- Use for your presentation
- Include in your portfolio

**Next Steps:**
- Customize the application
- Add more features
- Monitor usage and performance
- Scale as needed

Good luck with your presentation! 🚀
