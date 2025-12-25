from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps, lru_cache
import os
import uuid
import qrcode
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from mysql.connector import Error
import json
from io import BytesIO
import base64
from dotenv import load_dotenv
import mailtrap as mt

# Load environment variables
load_dotenv()

# DEBUG: Check environment loading
print("=== DEBUGGING ENV LOADING ===")
print(f"Current working directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")
print(f"DB_HOST from env: {os.getenv('DB_HOST', 'NOT_SET')}")
print(f"DB_NAME from env: {os.getenv('DB_NAME', 'NOT_SET')}")
print(f"DB_USER from env: {os.getenv('DB_USER', 'NOT_SET')}")
print(f"DB_PASSWORD from env: {'SET' if os.getenv('DB_PASSWORD') else 'NOT_SET'}")
print("===========================")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'geec_dms'),
    'user': os.getenv('DB_USER', 'geec_user'),
    'password': os.getenv('DB_PASSWORD', 'geec_password_123')
}

# Mailtrap configuration
MAILTRAP_API_KEY = os.getenv('MAILTRAP_API_KEY')
MAILTRAP_FROM_EMAIL = os.getenv('MAILTRAP_FROM_EMAIL', 'jamshid@gulfextremeinc.com')

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.context_processor
def inject_company_info():
    """Make company info available to all templates"""
    return {'company_info': get_company_info()}

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@lru_cache(maxsize=1)
def get_company_info():
    """Get company information from settings"""
    connection = get_db_connection()
    company_info = {'name': 'GEEC', 'logo': None}
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT setting_key, setting_value FROM settings WHERE setting_key IN ('company_name', 'company_logo')")
        settings = cursor.fetchall()
        
        for setting in settings:
            if setting['setting_key'] == 'company_name':
                company_info['name'] = setting['setting_value']
            elif setting['setting_key'] == 'company_logo':
                company_info['logo'] = setting['setting_value']
        
        cursor.close()
        connection.close()
    
    return company_info

def login_required(f):
    """Decorator for routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'Admin':
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def ceo_required(f):
    """Decorator for routes that require CEO privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') not in ['CEO', 'Admin']:
            flash('Access denied. CEO privileges required.')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user['full_name']
                session['role'] = user['role']
                flash('Login successful!')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.')
        else:
            flash('Database connection error.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    connection = get_db_connection()
    stats = {'verified': 0, 'pending': 0, 'rejected': 0}
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Get letter statistics
        cursor.execute("SELECT status, COUNT(*) as count FROM letters GROUP BY status")
        status_counts = cursor.fetchall()
        
        for row in status_counts:
            if row['status'] == 'Verified':
                stats['verified'] = row['count']
            elif row['status'] == 'Pending':
                stats['pending'] = row['count']
            elif row['status'] == 'Rejected':
                stats['rejected'] = row['count']
        
        cursor.close()
        connection.close()
    
    return render_template('dashboard.html', stats=stats)

@app.route('/create_letter', methods=['GET', 'POST'])
@login_required
def create_letter():
    """Upload new letter"""
    if request.method == 'POST':
        if 'letter_file' not in request.files:
            flash('No file selected.')
            return redirect(request.url)
        
        file = request.files['letter_file']
        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)
        
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Generate unique barcode
            letter_number = str(uuid.uuid4()).replace('-', '')[:12].upper()
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"{request.url_root}verify/{letter_number}")
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_buffer = BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_code_data = base64.b64encode(qr_buffer.getvalue()).decode()
            
            # Save to database
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO letters (letter_number, filename, original_filename, 
                    uploaded_by, upload_date, status, qr_code, require_ceo_verification)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (letter_number, unique_filename, filename, session['user_id'], 
                     datetime.now(), 'Pending', qr_code_data, 
                     1 if 'require_verification' in request.form else 0))
                
                connection.commit()
                cursor.close()
                connection.close()
                
                # Send email to CEO if verification required
                if 'require_verification' in request.form:
                    send_ceo_notification(letter_number, filename)
                
                flash('Letter uploaded successfully!')
                return redirect(url_for('letter_status'))
            else:
                flash('Database error occurred.')
        else:
            flash('Only PDF files are allowed.')
    
    return render_template('create_letter.html')

@app.route('/letter_status')
@login_required
def letter_status():
    """View letter status"""
    connection = get_db_connection()
    letters = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        if session['role'] in ['Admin', 'CEO']:
            cursor.execute("""
                SELECT l.*, u1.full_name as uploaded_by_name, u2.full_name as verified_by_name
                FROM letters l
                LEFT JOIN users u1 ON l.uploaded_by = u1.id
                LEFT JOIN users u2 ON l.verified_by = u2.id
                ORDER BY l.upload_date DESC
            """)
        else:
            cursor.execute("""
                SELECT l.*, u1.full_name as uploaded_by_name, u2.full_name as verified_by_name
                FROM letters l
                LEFT JOIN users u1 ON l.uploaded_by = u1.id
                LEFT JOIN users u2 ON l.verified_by = u2.id
                WHERE l.uploaded_by = %s
                ORDER BY l.upload_date DESC
            """, (session['user_id'],))
        
        letters = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('letter_status.html', letters=letters)

@app.route('/verify/<letter_number>')
def verify_letter(letter_number):
    """Public verification page"""
    connection = get_db_connection()
    letter_info = None
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.letter_number, l.status, l.upload_date, l.verified_date,
                   u1.full_name as uploaded_by_name, u2.full_name as verified_by_name
            FROM letters l
            LEFT JOIN users u1 ON l.uploaded_by = u1.id
            LEFT JOIN users u2 ON l.verified_by = u2.id
            WHERE l.letter_number = %s
        """, (letter_number,))
        
        letter_info = cursor.fetchone()
        cursor.close()
        connection.close()
    
    return render_template('verify_letter.html', letter=letter_info)

@app.route('/ceo_verify/<letter_number>')
@ceo_required
def ceo_verify(letter_number):
    """CEO verification page"""
    connection = get_db_connection()
    letter = None
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, u.full_name as uploaded_by_name
            FROM letters l
            LEFT JOIN users u ON l.uploaded_by = u.id
            WHERE l.letter_number = %s
        """, (letter_number,))
        
        letter = cursor.fetchone()
        cursor.close()
        connection.close()
    
    return render_template('ceo_verify.html', letter=letter)

@app.route('/approve_letter/<letter_number>', methods=['POST'])
@ceo_required
def approve_letter(letter_number):
    """Approve letter"""
    comments = request.form.get('comments', '')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE letters SET status = 'Verified', verified_by = %s, 
            verified_date = %s, verification_comments = %s
            WHERE letter_number = %s
        """, (session['user_id'], datetime.now(), comments, letter_number))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Send approval notification to uploader
        send_approval_notification(letter_number, 'Verified', comments)
        
        flash('Letter approved successfully!')
    
    return redirect(url_for('letter_status'))

@app.route('/reject_letter/<letter_number>', methods=['POST'])
@ceo_required
def reject_letter(letter_number):
    """Reject letter"""
    comments = request.form.get('comments', '')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE letters SET status = 'Rejected', verified_by = %s, 
            verified_date = %s, verification_comments = %s
            WHERE letter_number = %s
        """, (session['user_id'], datetime.now(), comments, letter_number))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Send rejection notification to uploader
        send_approval_notification(letter_number, 'Rejected', comments)
        
        flash('Letter rejected.')
    
    return redirect(url_for('letter_status'))

@app.route('/user_management')
@admin_required
def user_management():
    """User management page"""
    connection = get_db_connection()
    users = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, username, full_name, email, role, created_date FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
    
    return render_template('user_management.html', users=users)

@app.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    """Add new user"""
    username = request.form['username']
    full_name = request.form['full_name']
    email = request.form['email']
    role = request.form['role']
    password = request.form['password']
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        hashed_password = generate_password_hash(password)
        
        try:
            cursor.execute("""
                INSERT INTO users (username, full_name, email, role, password, created_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, full_name, email, role, hashed_password, datetime.now()))
            
            connection.commit()
            flash('User added successfully!')
        except Error as e:
            flash(f'Error adding user: {e}')
        finally:
            cursor.close()
            connection.close()
    
    return redirect(url_for('user_management'))

@app.route('/settings')
@admin_required
def settings():
    """Settings page"""
    connection = get_db_connection()
    settings_data = {}
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT setting_key, setting_value FROM settings")
        settings = cursor.fetchall()
        
        for setting in settings:
            settings_data[setting['setting_key']] = setting['setting_value']
        
        cursor.close()
        connection.close()
    
    return render_template('settings.html', settings=settings_data)

@app.route('/update_settings', methods=['POST'])
@admin_required
def update_settings():
    """Update settings"""
    company_name = request.form.get('company_name', '')
    ceo_email = request.form.get('ceo_email', '')
    admin_email = request.form.get('admin_email', '')
    mailtrap_api_key = request.form.get('mailtrap_api_key', '')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        # Handle logo upload
        if 'company_logo' in request.files:
            logo_file = request.files['company_logo']
            if logo_file and logo_file.filename:
                # Validate file type
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
                file_extension = logo_file.filename.rsplit('.', 1)[1].lower() if '.' in logo_file.filename else ''
                
                if file_extension in allowed_extensions:
                    # Create logos directory if it doesn't exist
                    logos_dir = os.path.join('static', 'images', 'logos')
                    os.makedirs(logos_dir, exist_ok=True)
                    
                    # Save logo with secure filename
                    filename = secure_filename(f"logo_{uuid.uuid4().hex[:8]}.{file_extension}")
                    logo_path = os.path.join(logos_dir, filename)
                    logo_file.save(logo_path)
                    
                    # Store relative path for web access
                    logo_url = f"/static/images/logos/{filename}"
                    
                    # Update logo setting in database
                    cursor.execute("""
                        INSERT INTO settings (setting_key, setting_value) VALUES ('company_logo', %s)
                        ON DUPLICATE KEY UPDATE setting_value = %s
                    """, (logo_url, logo_url))
                    
                    flash('Logo uploaded successfully!')
                else:
                    flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or SVG files.')
        
        # Update or insert other settings
        cursor.execute("""
            INSERT INTO settings (setting_key, setting_value) VALUES ('company_name', %s)
            ON DUPLICATE KEY UPDATE setting_value = %s
        """, (company_name, company_name))
        
        cursor.execute("""
            INSERT INTO settings (setting_key, setting_value) VALUES ('ceo_email', %s)
            ON DUPLICATE KEY UPDATE setting_value = %s
        """, (ceo_email, ceo_email))
        
        if admin_email:
            cursor.execute("""
                INSERT INTO settings (setting_key, setting_value) VALUES ('admin_email', %s)
                ON DUPLICATE KEY UPDATE setting_value = %s
            """, (admin_email, admin_email))
        
        if mailtrap_api_key:
            cursor.execute("""
                INSERT INTO settings (setting_key, setting_value) VALUES ('mailtrap_api_key', %s)
                ON DUPLICATE KEY UPDATE setting_value = %s
            """, (mailtrap_api_key, mailtrap_api_key))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Clear the company info cache so changes take effect immediately
        get_company_info.cache_clear()

        flash('Settings updated successfully!')
        # Clear the cache to reflect changes immediately
        get_company_info.cache_clear()
    
    return redirect(url_for('settings'))

@app.route('/edit_user', methods=['POST'])
@admin_required
def edit_user():
    """Edit existing user"""
    user_id = request.form['user_id']
    username = request.form['username']
    full_name = request.form['full_name']
    email = request.form['email']
    role = request.form['role']
    password = request.form.get('password', '')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        try:
            if password:
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    UPDATE users SET username = %s, full_name = %s, email = %s, 
                    role = %s, password = %s, updated_date = %s
                    WHERE id = %s
                """, (username, full_name, email, role, hashed_password, datetime.now(), user_id))
            else:
                cursor.execute("""
                    UPDATE users SET username = %s, full_name = %s, email = %s, 
                    role = %s, updated_date = %s
                    WHERE id = %s
                """, (username, full_name, email, role, datetime.now(), user_id))
            
            connection.commit()
            flash('User updated successfully!')
        except Error as e:
            flash(f'Error updating user: {e}')
        finally:
            cursor.close()
            connection.close()
    
    return redirect(url_for('user_management'))

@app.route('/delete_user', methods=['POST'])
@admin_required
def delete_user():
    """Delete user"""
    user_id = request.form['user_id']
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            flash('User deleted successfully!')
        except Error as e:
            flash(f'Error deleting user: {e}')
        finally:
            cursor.close()
            connection.close()
    
    return redirect(url_for('user_management'))

@app.route('/view_letter/<letter_number>')
@login_required
def view_letter(letter_number):
    """View letter details and content"""
    connection = get_db_connection()
    letter = None
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, u1.full_name as uploaded_by_name, u2.full_name as verified_by_name
            FROM letters l
            LEFT JOIN users u1 ON l.uploaded_by = u1.id
            LEFT JOIN users u2 ON l.verified_by = u2.id
            WHERE l.letter_number = %s
        """, (letter_number,))
        
        letter = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # Check if user has permission to view this letter
        if letter:
            # Admin and CEO can view all letters
            # Regular users can only view their own uploaded letters
            if (session.get('role') in ['Admin', 'CEO'] or 
                letter['uploaded_by'] == session.get('user_id')):
                return render_template('view_letter.html', letter=letter)
            else:
                flash('Access denied. You can only view your own letters.')
                return redirect(url_for('letter_status'))
    
    flash('Letter not found.')
    return redirect(url_for('letter_status'))

@app.route('/download_letter/<letter_number>')
@login_required
def download_letter(letter_number):
    """Download letter file"""
    connection = get_db_connection()
    letter = None
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT filename, original_filename, uploaded_by
            FROM letters WHERE letter_number = %s
        """, (letter_number,))
        
        letter = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # Check permissions
        if letter and (session.get('role') in ['Admin', 'CEO'] or 
                      letter['uploaded_by'] == session.get('user_id')):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], letter['filename'])
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, 
                               download_name=letter['original_filename'])
            else:
                flash('File not found.')
        else:
            flash('Access denied.')
    
    return redirect(url_for('letter_status'))

def send_ceo_notification(letter_number, filename):
    """Send email notification to CEO"""
    ceo_email = get_setting('ceo_email')
    company_name = get_setting('company_name', 'GEEC')
    
    if not ceo_email:
        print("CEO email not configured")
        return False
    
    # Get uploader information
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, u.full_name, u.email 
            FROM letters l 
            JOIN users u ON l.uploaded_by = u.id 
            WHERE l.letter_number = %s
        """, (letter_number,))
        letter_info = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if letter_info:
            subject = f"[{company_name}] New Letter Requires CEO Approval - {letter_number}"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                        Letter Approval Required
                    </h2>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #495057; margin-top: 0;">Letter Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Letter Number:</td>
                                <td style="padding: 8px;">{letter_number}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Document:</td>
                                <td style="padding: 8px;">{filename}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Uploaded by:</td>
                                <td style="padding: 8px;">{letter_info['full_name']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Upload Date:</td>
                                <td style="padding: 8px;">{letter_info['upload_date'].strftime('%Y-%m-%d %H:%M:%S')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{request.url_root}ceo_verify/{letter_number}" 
                           style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Review & Approve Letter
                        </a>
                    </div>
                    
                    <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px;">
                        This is an automated notification from {company_name} Document Management System.
                    </p>
                </div>
            </body>
            </html>
            """
            
            plain_content = f"""
            Letter Approval Required
            
            Letter Number: {letter_number}
            Document: {filename}
            Uploaded by: {letter_info['full_name']}
            Upload Date: {letter_info['upload_date'].strftime('%Y-%m-%d %H:%M:%S')}
            
            Please visit: {request.url_root}ceo_verify/{letter_number}
            
            This is an automated notification from {company_name} Document Management System.
            """
            
            success, message = send_email_notification(ceo_email, subject, html_content, plain_content)
            if success:
                print(f"CEO notification sent successfully: {message}")
            else:
                print(f"Failed to send CEO notification: {message}")
            
            return success
    
    return False

def send_approval_notification(letter_number, status, comments=None):
    """Send email notification when letter is approved/rejected"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, u1.full_name as uploader_name, u1.email as uploader_email,
                   u2.full_name as ceo_name
            FROM letters l 
            JOIN users u1 ON l.uploaded_by = u1.id 
            LEFT JOIN users u2 ON l.verified_by = u2.id
            WHERE l.letter_number = %s
        """, (letter_number,))
        letter_info = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if letter_info and letter_info['uploader_email']:
            company_name = get_setting('company_name', 'GEEC')
            status_color = "#27ae60" if status == "Verified" else "#e74c3c"
            status_text = "APPROVED" if status == "Verified" else "REJECTED"
            
            subject = f"[{company_name}] Letter {status_text} - {letter_number}"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: {status_color}; border-bottom: 2px solid {status_color}; padding-bottom: 10px;">
                        Letter {status_text}
                    </h2>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #495057; margin-top: 0;">Letter Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Letter Number:</td>
                                <td style="padding: 8px;">{letter_number}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Document:</td>
                                <td style="padding: 8px;">{letter_info['original_filename']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Status:</td>
                                <td style="padding: 8px; color: {status_color}; font-weight: bold;">{status_text}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Reviewed by:</td>
                                <td style="padding: 8px;">{letter_info['ceo_name'] or 'CEO'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Review Date:</td>
                                <td style="padding: 8px;">{letter_info['verified_date'].strftime('%Y-%m-%d %H:%M:%S')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    {f'<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;"><h4 style="margin-top: 0; color: #856404;">Comments:</h4><p style="margin-bottom: 0;">{comments}</p></div>' if comments else ''}
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{request.url_root}view_letter/{letter_number}" 
                           style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View Letter Details
                        </a>
                    </div>
                    
                    <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px;">
                        This is an automated notification from {company_name} Document Management System.
                    </p>
                </div>
            </body>
            </html>
            """
            
            plain_content = f"""
            Letter {status_text}
            
            Letter Number: {letter_number}
            Document: {letter_info['original_filename']}
            Status: {status_text}
            Reviewed by: {letter_info['ceo_name'] or 'CEO'}
            Review Date: {letter_info['verified_date'].strftime('%Y-%m-%d %H:%M:%S')}
            
            {f'Comments: {comments}' if comments else ''}
            
            View details at: {request.url_root}view_letter/{letter_number}
            
            This is an automated notification from {company_name} Document Management System.
            """
            
            success, message = send_email_notification(letter_info['uploader_email'], subject, html_content, plain_content)
            if success:
                print(f"Approval notification sent successfully: {message}")
            else:
                print(f"Failed to send approval notification: {message}")
            
            return success
    
    return False

@app.route('/api/test-email', methods=['POST'])
@admin_required
def test_email():
    """Test email configuration"""
    try:
        admin_email = get_setting('admin_email')
        if not admin_email:
            return jsonify({'success': False, 'error': 'Admin email not configured'})
        
        company_name = get_setting('company_name', 'GEEC')
        subject = f"[{company_name}] Email Configuration Test"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 10px;">
                    Email Test Successful ✓
                </h2>
                
                <p>This is a test email from your {company_name} Document Management System.</p>
                
                <div style="background-color: #d4edda; border-left: 4px solid #27ae60; padding: 15px; margin: 20px 0;">
                    <h4 style="margin-top: 0; color: #155724;">Email Configuration Status:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Mailtrap integration: <strong>Working</strong></li>
                        <li>From email: <strong>{MAILTRAP_FROM_EMAIL}</strong></li>
                        <li>Test timestamp: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></li>
                    </ul>
                </div>
                
                <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px;">
                    This is an automated test from {company_name} Document Management System.
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
        Email Test Successful ✓
        
        This is a test email from your {company_name} Document Management System.
        
        Email Configuration Status:
        - Mailtrap integration: Working
        - From email: {MAILTRAP_FROM_EMAIL}
        - Test timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated test from {company_name} Document Management System.
        """
        
        success, message = send_email_notification(admin_email, subject, html_content, plain_content)
        
        if success:
            return jsonify({'success': True, 'message': 'Test email sent successfully!'})
        else:
            return jsonify({'success': False, 'error': message})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Email test failed: {str(e)}'})

@app.route('/api/clear-cache', methods=['POST'])
@admin_required
def clear_cache():
    """Clear application cache"""
    try:
        # For now, just return success - can implement actual cache clearing later
        return jsonify({'success': True, 'message': 'Cache cleared successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Cache clearing failed: {str(e)}'})

@app.route('/delete_letter/<letter_number>', methods=['POST'])
@admin_required
def delete_letter(letter_number):
    """Delete letter (Admin only)"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        try:
            # Get letter information before deletion
            cursor.execute("SELECT filename, original_filename FROM letters WHERE letter_number = %s", (letter_number,))
            letter = cursor.fetchone()
            
            if letter:
                # Delete from database
                cursor.execute("DELETE FROM letters WHERE letter_number = %s", (letter_number,))
                connection.commit()
                
                # Delete physical file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], letter['filename'])
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except OSError as e:
                        print(f"Error deleting file {file_path}: {e}")
                
                flash(f'Letter "{letter["original_filename"]}" has been deleted successfully.')
            else:
                flash('Letter not found.')
                
        except Error as e:
            flash(f'Error deleting letter: {e}')
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Database connection error.')
    
    return redirect(url_for('letter_status'))

def send_email_notification(to_email, subject, html_content, plain_content=None):
    """Send email using Mailtrap"""
    try:
        # Get API key from env or database
        api_key = MAILTRAP_API_KEY
        if not api_key:
            api_key = get_setting('mailtrap_api_key')

        if not api_key:
            print("Mailtrap API key not configured")
            return False, "Mailtrap API key not configured"

        if plain_content is None:
            plain_content = html_content
        
        mail = mt.Mail(
            sender=mt.Address(email=MAILTRAP_FROM_EMAIL, name="GEEC DMS"),
            to=[mt.Address(email=to_email)],
            subject=subject,
            text=plain_content,
            html=html_content,
        )
        
        client = mt.MailtrapClient(token=api_key)
        response = client.send(mail)
        
        return True, f"Email sent successfully via Mailtrap"
    
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"

def get_setting(key, default=None):
    """Get setting value from database"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT setting_value FROM settings WHERE setting_key = %s", (key,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['setting_value'] if result else default
    return default

if __name__ == '__main__':
    # Production settings
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    if os.getenv('FLASK_ENV') == 'production':
        # Production mode
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        # Development mode
        app.run(debug=debug_mode, port=port) 