# Cloud Database Deployment Guide

Your Syllabus Tracker is now configured for cloud database deployment! 🚀

## Supported Cloud Platforms

### Option 1: Heroku (PostgreSQL) - Easiest
### Option 2: Railway (PostgreSQL/MySQL)
### Option 3: Render (PostgreSQL)
### Option 4: PlanetScale (MySQL)
### Option 5: AWS RDS / Azure / GCP

---

## 🚀 Quick Deploy to Heroku

### Prerequisites
- Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- Git repository initialized

### Steps

1. **Login to Heroku**
```powershell
heroku login
```

2. **Create Heroku App**
```powershell
heroku create syllabus-tracker-app
```

3. **Add PostgreSQL Database**
```powershell
heroku addons:create heroku-postgresql:mini
```

4. **Set Environment Variables**
```powershell
heroku config:set SECRET_KEY="your-production-secret-key-here"
heroku config:set FLASK_ENV=production
```

5. **Deploy**
```powershell
git add .
git commit -m "Configure for cloud deployment"
git push heroku main
```

6. **Initialize Database**
```powershell
heroku run flask db upgrade
heroku run python scripts/create_db.py
```

7. **Open Your App**
```powershell
heroku open
```

---

## 🚂 Deploy to Railway

### Steps

1. **Go to Railway.app and create account**
2. **Click "New Project" → "Deploy from GitHub"**
3. **Select your repository**
4. **Add PostgreSQL database**:
   - Click "New" → "Database" → "PostgreSQL"
5. **Add environment variables in Settings**:
   - `SECRET_KEY`: your-secret-key
   - `FLASK_ENV`: production
6. **Railway auto-deploys on git push**

**Note**: Railway automatically sets `DATABASE_URL` environment variable.

---

## 🎨 Deploy to Render

### Steps

1. **Go to Render.com and create account**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure:**
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn "app:create_app()"`
5. **Add PostgreSQL database**:
   - Dashboard → "New +" → "PostgreSQL"
   - Copy the Internal Database URL
6. **Add environment variables**:
   - `DATABASE_URL`: (paste database URL)
   - `SECRET_KEY`: your-secret-key
   - `FLASK_ENV`: production
7. **Deploy**

---

## 🌐 Deploy to PlanetScale (MySQL Cloud)

### Steps

1. **Create PlanetScale account** at planetscale.com
2. **Create database**:
```powershell
pscale database create syllabus-tracker
```

3. **Get connection string**:
```powershell
pscale connect syllabus-tracker main --port 3309
```

4. **Copy connection URL and set in .env**:
```
DATABASE_URL=mysql+mysqlconnector://user:pass@host:port/dbname?ssl_ca=/path/to/cert
```

5. **For production, create password**:
```powershell
pscale password create syllabus-tracker main password-name
```

---

## 🔧 Configuration Details

### Environment Variables Required

**For all platforms:**
- `DATABASE_URL` - Automatically set by most platforms
- `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `FLASK_ENV` - Set to `production`

**Optional:**
- `FLASK_APP` - Default: `app`

### Database URL Format

**PostgreSQL:**
```
postgresql://user:password@host:port/database
```

**MySQL:**
```
mysql+mysqlconnector://user:password@host:port/database
```

---

## 📊 Database Migration

### Initialize database on cloud:

```powershell
# If using Heroku
heroku run flask db upgrade
heroku run python scripts/create_db.py

# If using Railway (via Railway CLI)
railway run flask db upgrade
railway run python scripts/create_db.py

# If using Render (via SSH)
# Access Shell from Render dashboard, then:
flask db upgrade
python scripts/create_db.py
```

---

## 🔒 Security Best Practices

1. **Generate strong SECRET_KEY**:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Never commit .env file** - Already in .gitignore

3. **Use environment variables** for all sensitive data

4. **Enable SSL** - Most cloud platforms auto-enable

5. **Set FLASK_ENV=production** to disable debug mode

---

## 🧪 Testing Cloud Database Locally

1. **Get cloud database URL** from your platform
2. **Set in .env**:
```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

3. **Run locally**:
```powershell
flask run
```

Your app will now connect to the cloud database!

---

## 📝 Environment Variables Template

Create `.env.production` for cloud deployment:

```env
# Production Environment Variables
DATABASE_URL=your-cloud-database-url-here
SECRET_KEY=your-generated-secret-key-here
FLASK_ENV=production
FLASK_APP=app

# Optional
ENABLE_CLAUDE_HAIKU_45=false
```

---

## ⚡ Performance Tips

1. **Connection Pooling** - Already configured in config.py
2. **Use CDN** for static files in production
3. **Enable caching** for frequently accessed data
4. **Database indexes** - Already set on foreign keys
5. **Monitor query performance** with platform tools

---

## 🐛 Troubleshooting

### "No module named psycopg2"
```powershell
pip install -r requirements.txt
```

### "Connection refused"
- Check DATABASE_URL is set correctly
- Verify database is running on cloud platform
- Check firewall rules allow connections

### "Application error"
- Check logs: `heroku logs --tail` (Heroku)
- Verify all environment variables are set
- Ensure database is migrated: `flask db upgrade`

### "500 Internal Server Error"
- Set `FLASK_ENV=production` to see proper error pages
- Check application logs on your platform
- Verify database schema is up to date

---

## 📦 What's Included

Your project now has:
- ✅ `config.py` - Cloud database support with automatic detection
- ✅ `requirements.txt` - Added psycopg2-binary (PostgreSQL) and gunicorn
- ✅ `Procfile` - For Heroku/Railway deployment
- ✅ `runtime.txt` - Specifies Python version
- ✅ Connection pooling and SSL support
- ✅ Automatic postgres:// → postgresql:// conversion (Heroku fix)

---

## 🎯 Next Steps

1. Choose your cloud platform
2. Follow the specific deployment guide above
3. Set environment variables
4. Deploy and migrate database
5. Test your live application!

**Your app is cloud-ready! 🌟**
