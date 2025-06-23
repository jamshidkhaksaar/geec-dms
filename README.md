# GEEC Online Document Management System (DMS)

A secure, web-based document management system designed for organizations to upload, verify, and track official letters. The system provides role-based access control, CEO verification workflows, and public verification capabilities through QR codes.

## 🚀 Features

### Core Functionality
- **Document Upload**: Secure PDF letter uploads with drag-and-drop interface
- **CEO Verification**: Email-based verification workflow with direct approval/rejection links
- **QR Code Generation**: Unique QR codes for each letter for public verification
- **Status Tracking**: Real-time status updates (Pending, Verified, Rejected)
- **Public Verification**: Third-party verification without accessing document content

### User Management
- **Role-Based Access**: Admin, CEO, and User roles with different permissions
- **User Management**: Admin can create, edit, and manage user accounts
- **Secure Authentication**: Password-hashed login system

### Dashboard & Analytics
- **Interactive Dashboard**: Statistics cards with visual charts
- **Letter Overview**: Comprehensive listing with search and filtering
- **Mobile Responsive**: Fully optimized for mobile devices
- **Real-time Updates**: Automatic status updates and notifications

### System Features
- **Email Notifications**: SendGrid integration for automated emails
- **Customizable Branding**: Company logo and name customization
- **Audit Logging**: Complete activity tracking for compliance
- **Shared Hosting Ready**: Designed for easy deployment on shared hosting

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MySQL
- **Email Service**: SendGrid API
- **QR Codes**: Python QRCode library
- **PDF Processing**: Secure file handling
- **Charts**: Chart.js for dashboard visualizations

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL 5.7 or higher
- SendGrid account (for email notifications)
- Web server (Apache/Nginx for production)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd geec-online-dms
```

### 2. Run Setup Script
```bash
python setup_dms.py
```

### 3. Configure Database
```bash
# Login to MySQL
mysql -u root -p

# Import the database schema
mysql -u root -p < database_schema.sql
```

### 4. Update Configuration
Edit the `.env` file with your settings:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=geec_dms
SECRET_KEY=your-secret-key-here
SENDGRID_API_KEY=your-sendgrid-api-key
```

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 👤 Default Login Credentials

After running the database schema:
- **Admin**: `admin` / `admin123`
- **CEO**: `ceo` / `ceo123`
- **User**: `user` / `user123`

⚠️ **Change these passwords immediately in production!**

## 📖 User Guide

### For Administrators

#### User Management
1. Navigate to **User Management** in the sidebar
2. Click **Add User** to create new accounts
3. Assign appropriate roles (Admin, CEO, User)
4. Edit or deactivate users as needed

#### System Settings
1. Go to **Settings** to configure:
   - Company name and branding
   - Email server settings
   - System preferences

#### Dashboard Overview
- Monitor letter statistics
- View system activity
- Access quick actions

### For Users

#### Uploading Letters
1. Click **Create New Letter**
2. Drag and drop your PDF file or click to browse
3. Enter an optional title
4. Check "Require CEO Verification" if needed
5. Add any additional notes
6. Click **Upload Letter**

#### Tracking Letters
1. Go to **Letter Status** to view all your letters
2. Use filters to find specific letters
3. Click the QR code icon to view/download QR codes
4. Use the eye icon to see public verification page

### For CEOs

#### Verifying Letters
1. Check your email for verification requests
2. Click the verification link in the email
3. Review the letter details and document
4. Choose **Approve** or **Reject** with comments
5. The status updates automatically

#### Dashboard Access
- View pending verifications
- Monitor approval statistics
- Quick access to verification queue

### Public Verification

#### Via QR Code
1. Scan the QR code with any QR reader
2. View verification status and letter details
3. No access to actual document content

#### Manual Verification
1. Visit the verification page
2. Enter the letter number manually
3. View verification status and metadata

## 🔧 Configuration

### Email Settings (SendGrid)
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.sendgrid.net',
    'smtp_port': 587,
    'sender_email': 'your-email@company.com',
    'api_key': 'your-sendgrid-api-key'
}
```

### Database Configuration
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'geec_dms',
    'user': 'root',
    'password': 'your_password'
}
```

### File Upload Settings
- Maximum file size: 16MB
- Allowed formats: PDF only
- Upload directory: `uploads/`

## 🚀 Production Deployment

### Shared Hosting Deployment

1. **Upload Files**: Transfer all files to your hosting directory
2. **Database Setup**: Import `database_schema.sql` via cPanel/phpMyAdmin
3. **Configuration**: Update database credentials in `app.py`
4. **Dependencies**: Install requirements (contact host if needed)
5. **Permissions**: Set appropriate file permissions (755/644)

### Dedicated Server Deployment

1. **Web Server Configuration** (Nginx + Gunicorn):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/app/static;
    }
}
```

2. **Run with Gunicorn**:
```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

3. **SSL Certificate**: Use Let's Encrypt or commercial SSL
4. **Environment Variables**: Set production environment variables
5. **Database**: Use production MySQL server

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Update default user passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up regular database backups
- [ ] Enable audit logging
- [ ] Restrict file upload types
- [ ] Configure proper file permissions

## 🗂️ File Structure

```
geec-online-dms/
├── app.py                    # Main Flask application
├── database_schema.sql       # Database schema and initial data
├── requirements.txt          # Python dependencies
├── setup_dms.py             # Setup script
├── README.md                # This file
├── PRD.md                   # Product Requirements Document
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── dashboard.html      # Dashboard
│   ├── create_letter.html  # Letter upload
│   ├── letter_status.html  # Letter listing
│   ├── verify_letter.html  # Public verification
│   └── ceo_verify.html     # CEO verification
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Custom styles
│   ├── js/
│   │   └── main.js         # JavaScript functionality
│   └── images/             # Image assets
└── uploads/                 # File uploads directory
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Check MySQL service is running
- Verify database credentials
- Ensure database exists

**File Upload Issues**
- Check file size (max 16MB)
- Verify uploads directory permissions
- Ensure PDF format only

**Email Not Sending**
- Verify SendGrid API key
- Check email configuration
- Test SMTP connectivity

**Permission Errors**
- Set correct file permissions (755/644)
- Check upload directory ownership
- Verify Python module access

### Debug Mode
Enable debug mode for development:
```python
app.run(debug=True)
```

### Logs
Check application logs in:
- Console output (development)
- Web server logs (production)
- Application log files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

## 🔄 Version History

- **v1.0.0** - Initial release
  - Core document management functionality
  - User authentication and role management
  - CEO verification workflow
  - QR code generation and public verification
  - Responsive web interface
  - Email notifications

---

**GEEC Online DMS** - Secure • Reliable • Professional Document Management 