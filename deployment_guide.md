# GEEC DMS - Namecheap Shared Hosting Deployment Guide

## Prerequisites
- Namecheap shared hosting account with Python support
- MySQL database access
- SendGrid account for email notifications
- FTP/SFTP access to your hosting account

## Step-by-Step Deployment Instructions

### 1. Prepare Your Hosting Environment

#### 1.1 Verify Python Support
- Log into your Namecheap cPanel
- Go to "Software" → "Setup Python App"
- Create a new Python application:
  - Python version: 3.8 or higher
  - Application root: `/public_html/geec-dms` (or your preferred directory)
  - Application URL: your domain or subdomain
  - Application startup file: `passenger_wsgi.py`

#### 1.2 Create MySQL Database
- In cPanel, go to "Databases" → "MySQL Databases"
- Create a new database: `yourusername_geec_dms`
- Create a database user with full privileges
- Note down the database name, username, and password

### 2. Upload Application Files

#### 2.1 Upload via File Manager or FTP
Upload all files to your application root directory:
```
/public_html/geec-dms/
├── app.py
├── passenger_wsgi.py
├── requirements.txt
├── database_schema.sql
├── .env
├── static/
├── templates/
├── uploads/
└── other files...
```

#### 2.2 Set Permissions
- Set executable permissions on `passenger_wsgi.py`: 755
- Set write permissions on `uploads/` directory: 755
- Ensure `.env` file has restricted permissions: 644

### 3. Configure Environment Variables

#### 3.1 Create .env File
Copy `.env.production` to `.env` and update with your actual values:
```bash
SECRET_KEY=your-very-secure-secret-key-here
DB_HOST=localhost
DB_NAME=yourusername_geec_dms
DB_USER=yourusername_dbuser
DB_PASSWORD=your_db_password
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
FLASK_ENV=production
FLASK_DEBUG=False
```

### 4. Install Dependencies

#### 4.1 Via cPanel Python App
- Go to "Setup Python App" in cPanel
- Select your application
- In the "Packages" section, install packages from requirements.txt
- Or use the terminal if available:
```bash
pip install -r requirements.txt
```

### 5. Setup Database

#### 5.1 Import Database Schema
- Access phpMyAdmin from cPanel
- Select your database
- Import the `database_schema.sql` file
- Verify all tables are created successfully

#### 5.2 Update Default Credentials
Run these SQL commands to update default user passwords:
```sql
-- Update admin password (change 'newpassword123' to your desired password)
UPDATE users SET password = 'pbkdf2:sha256:260000$salt$hash' WHERE username = 'admin';

-- Update CEO password
UPDATE users SET password = 'pbkdf2:sha256:260000$salt$hash' WHERE username = 'ceo';

-- Update user password
UPDATE users SET password = 'pbkdf2:sha256:260000$salt$hash' WHERE username = 'user';
```

Note: You'll need to generate proper password hashes. Use the password generation script provided.

### 6. Configure Email (SendGrid)

#### 6.1 Setup SendGrid Account
1. Create account at https://sendgrid.com/
2. Generate API key
3. Add your domain for email authentication
4. Update `.env` file with your SendGrid API key

### 7. Test Your Application

#### 7.1 Access Your Application
- Visit your domain/subdomain
- Test login with default credentials
- Upload a test PDF file
- Verify email notifications work

#### 7.2 Common Issues and Solutions

**Issue: 500 Internal Server Error**
- Check error logs in cPanel
- Verify all file paths in code
- Ensure database connection works

**Issue: File Upload Not Working**
- Check `uploads/` directory permissions
- Verify upload path in application

**Issue: Email Not Sending**
- Verify SendGrid API key
- Check SendGrid account status
- Test email configuration in settings

### 8. Security Considerations

#### 8.1 Production Hardening
- Change all default passwords
- Use strong SECRET_KEY
- Regularly update dependencies
- Monitor application logs
- Backup database regularly

#### 8.2 SSL Certificate
- Enable SSL/TLS in Namecheap cPanel
- Force HTTPS redirects
- Update absolute URLs to use HTTPS

### 9. Maintenance

#### 9.1 Regular Tasks
- Monitor disk usage for uploads
- Clean up old files periodically
- Update application dependencies
- Review user access regularly

#### 9.2 Backup Strategy
- Schedule regular database backups
- Backup uploaded files
- Keep configuration files backed up

## Support

For technical issues:
1. Check application logs in cPanel
2. Verify database connectivity
3. Test email configuration
4. Review file permissions

Contact your hosting provider for server-related issues. 