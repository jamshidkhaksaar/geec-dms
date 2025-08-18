# GEEC DMS - Namecheap Shared Hosting Guide

## 🚀 Quick Start Deployment Guide

Your Flask Document Management System is now ready for production deployment on Namecheap shared hosting. Follow these steps:

## ✅ What You Have Now

Your application includes:
- **Main Application**: `app.py` - Production-ready Flask app
- **WSGI Entry Point**: `passenger_wsgi.py` - Required for shared hosting
- **Database Schema**: `database_schema.sql` - Complete database structure
- **Security Configuration**: `.htaccess` - Apache security settings
- **Environment Template**: `env_template.txt` - Configuration template
- **Production Tools**: Password generator and setup verification scripts

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Namecheap Account
1. **Login to cPanel** on your Namecheap hosting account
2. **Verify Python Support**: Go to "Software" → "Setup Python App"
3. **Create MySQL Database**: Go to "Databases" → "MySQL Databases"
   - Database name: `yourusername_geec_dms`
   - Create user with full privileges
   - Note the credentials

### Step 2: Upload Your Files
Upload these files to your hosting directory (e.g., `/public_html/geec-dms/`):

**Required Files:**
- `app.py`
- `passenger_wsgi.py`
- `production_requirements.txt` (rename to `requirements.txt`)
- `database_schema.sql`
- `.htaccess`
- `static/` folder (with all CSS, JS, images)
- `templates/` folder (with all HTML files)
- Create an empty `uploads/` folder

### Step 3: Setup Python Environment
1. In cPanel → "Setup Python App"
2. Create new application:
   - **Python Version**: 3.8 or higher
   - **Application Root**: `/public_html/geec-dms`
   - **Application URL**: `yourdomain.com/geec-dms`
   - **Startup File**: `passenger_wsgi.py`
3. Install dependencies from requirements.txt

### Step 4: Configure Database
1. Access **phpMyAdmin** from cPanel
2. Select your database
3. Import `database_schema.sql`
4. Verify all tables are created (users, letters, settings, etc.)

### Step 5: Setup Environment Variables
1. Create `.env` file in your app root directory
2. Copy content from `env_template.txt`
3. Update with your actual values:
```bash
SECRET_KEY=your-strong-secret-key-here
DB_HOST=localhost
DB_NAME=yourusername_geec_dms
DB_USER=yourusername_dbuser
DB_PASSWORD=your_database_password
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
FLASK_ENV=production
FLASK_DEBUG=False
```

### Step 6: Update Default Passwords
**Important Security Step!**

1. Run `python3 generate_password.py` locally to generate secure password hashes
2. In phpMySQL, update default user passwords:
```sql
UPDATE users SET password = 'your_generated_hash' WHERE username = 'admin';
UPDATE users SET password = 'your_generated_hash' WHERE username = 'ceo';
UPDATE users SET password = 'your_generated_hash' WHERE username = 'user';
```

### Step 7: Set File Permissions
- `passenger_wsgi.py`: 755
- `uploads/` directory: 755
- `.env` file: 644
- Other files: 644

### Step 8: Test Your Application
1. Visit your application URL
2. Test login with updated credentials
3. Upload a test PDF file
4. Verify all functions work

## 🔧 Additional Setup (Optional)

### Email Configuration (Recommended)
1. Create **SendGrid account** (free tier available)
2. Generate API key
3. Update `.env` with SendGrid credentials
4. Test email functionality in app settings

### SSL Certificate (Recommended)
1. Enable SSL in Namecheap cPanel
2. Force HTTPS redirects
3. Update `.htaccess` if needed

## 🆘 Troubleshooting

### Common Issues:

**500 Internal Server Error:**
- Check cPanel Error Logs
- Verify `passenger_wsgi.py` syntax
- Check database connection in `.env`

**File Upload Not Working:**
- Check `uploads/` directory permissions (755)
- Verify disk space availability

**Database Connection Failed:**
- Double-check database credentials in `.env`
- Ensure database user has proper privileges

**Email Not Sending:**
- Verify SendGrid API key
- Check SendGrid account status

## 📞 Support
- **Application Issues**: Check the deployment checklist
- **Hosting Issues**: Contact Namecheap support
- **Email Issues**: Check SendGrid documentation

## 🎉 You're Ready!

Once deployed, your GEEC Document Management System will have:
- ✅ Secure user authentication (Admin, CEO, User roles)
- ✅ PDF document upload and management
- ✅ CEO verification workflow with email notifications
- ✅ Public letter verification via QR codes
- ✅ Admin panel for user and system management
- ✅ Mobile-responsive design
- ✅ Production-grade security

**Default Login Credentials (Change immediately!):**
- Admin: `admin` / (your new password)
- CEO: `ceo` / (your new password)
- User: `user` / (your new password)

---

**Need Help?** Refer to `DEPLOYMENT_CHECKLIST.md` for detailed troubleshooting and `production_setup.py` for setup verification. 