# GEEC DMS - Deployment Checklist for Namecheap Shared Hosting

## Pre-Deployment Checklist

### 1. Account Setup
- [ ] Namecheap shared hosting account with Python support
- [ ] Domain or subdomain configured
- [ ] cPanel access credentials
- [ ] SendGrid account created
- [ ] SendGrid API key generated

### 2. Local Preparation
- [ ] All files tested locally
- [ ] Database schema verified
- [ ] Environment variables configured
- [ ] Production requirements.txt verified
- [ ] Password hashes generated

### 3. Files to Upload
- [*] `app.py` - Main Flask application
- [*] `passenger_wsgi.py` - WSGI entry point
- [*] `requirements.txt` or `production_requirements.txt`
- [*] `database_schema.sql` - Database structure
- [*] `.env` - Environment variables (create from .env.production)
- [*] `.htaccess` - Apache configuration
- [*] `static/` - CSS, JS, images
- [*] `templates/` - HTML templates
- [*] `uploads/` - File upload directory (create empty)

## Deployment Steps

### Step 1: Setup Python Environment
1. Login to cPanel
2. Go to "Software" → "Setup Python App"
3. Create new Python app:
   - **Python Version**: 3.8+
   - **Application Root**: `/public_html/geec-dms`
   - **Application URL**: `yourdomain.com/geec-dms`
   - **Startup File**: `passenger_wsgi.py`
4. Note the virtual environment path

### Step 2: Upload Files
1. Use File Manager or FTP/SFTP
2. Upload all files to application root
3. Set permissions:
   - `passenger_wsgi.py`: 755
   - `uploads/`: 755
   - `.env`: 644
   - Other files: 644

### Step 3: Install Dependencies
1. In Python App interface, click "Install packages"
2. Either:
   - Upload requirements.txt and install from file
   - Or manually install: `pip install flask werkzeug mysql-connector-python qrcode pillow sendgrid python-dotenv`

### Step 4: Database Setup
1. Go to "Databases" → "MySQL Databases"
2. Create database: `yourusername_geec_dms`
3. Create user with full privileges
4. Access phpMyAdmin
5. Import `database_schema.sql`
6. Verify tables created successfully

### Step 5: Configure Environment
1. Copy `.env.production` to `.env`
2. Update with your actual values:
   ```
   SECRET_KEY=your-generated-secret-key
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
1. Run `python3 generate_password.py` locally
2. Generate hashes for admin, ceo, user accounts
3. Update database with new hashes:
   ```sql
   UPDATE users SET password = 'generated_hash_here' WHERE username = 'admin';
   UPDATE users SET password = 'generated_hash_here' WHERE username = 'ceo';
   UPDATE users SET password = 'generated_hash_here' WHERE username = 'user';
   ```

### Step 7: Test Application
1. Visit your application URL
2. Check for any errors in cPanel Error Logs
3. Test login functionality
4. Test file upload
5. Test email notifications (if configured)

## Post-Deployment Checklist

### Security
- [ ] Changed all default passwords
- [ ] SSL certificate installed and configured
- [ ] HTTPS redirect enabled
- [ ] Sensitive files protected (.env, .py, .sql)
- [ ] File upload directory secured

### Functionality Testing
- [ ] User login/logout works
- [ ] File upload functionality works
- [ ] CEO verification workflow works
- [ ] Email notifications work
- [ ] Public verification page works
- [ ] Admin panel accessible
- [ ] User management works

### Performance & Monitoring
- [ ] Application loads quickly
- [ ] Database queries performing well
- [ ] File uploads working within size limits
- [ ] Error logging configured
- [ ] Backup strategy implemented

## Troubleshooting Common Issues

### 500 Internal Server Error
1. Check cPanel Error Logs
2. Verify passenger_wsgi.py syntax
3. Check file permissions
4. Verify Python dependencies installed
5. Check database connection

### Database Connection Issues
1. Verify database credentials in .env
2. Check if database exists
3. Verify user has proper privileges
4. Test connection from phpMyAdmin

### File Upload Issues
1. Check uploads/ directory permissions
2. Verify MAX_CONTENT_LENGTH setting
3. Check disk space availability
4. Verify upload path configuration

### Email Not Working
1. Verify SendGrid API key
2. Check SendGrid account status
3. Test email configuration in app settings
4. Check spam folders for test emails

## Maintenance Tasks

### Regular Tasks
- [ ] Monitor disk usage
- [ ] Review application logs
- [ ] Clean up old uploaded files
- [ ] Update user passwords periodically
- [ ] Backup database regularly

### Updates
- [ ] Keep Python dependencies updated
- [ ] Monitor security updates
- [ ] Update application code as needed
- [ ] Review and update email templates

## Support Contacts

- **Namecheap Support**: For hosting-related issues
- **SendGrid Support**: For email delivery issues
- **Application Support**: For custom development needs

---

**Deployment Date**: ___________  
**Deployed By**: ___________  
**Verified By**: ___________  
**Go-Live Date**: ___________ 