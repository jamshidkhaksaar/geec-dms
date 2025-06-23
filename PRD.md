# Product Requirements Document (PRD)  
## GEEC Online DMS (Document Management System)

### 1. Overview
**Product Name:** GEEC Online DMS  
**Purpose:** A mobile-responsive web application designed to facilitate the upload, verification, and status checking of official letters within an organization. The system will allow users to upload PDF letters, have them verified by the CEO, and enable third parties to check the verification status via a unique barcode or URL.  
**Target Audience:**  
- Internal users (Admin, CEO, and staff uploading letters)  
- External third parties (for verification of letter status)  
**Platform:** Web application, mobile-responsive  
**Hosting:** Shared hosting environment  

### 2. Objectives
- Enable secure upload of PDF letters by authorized users for CEO verification.  
- Provide a dashboard for users and admin to track letter statuses (Verified, Pending, Rejected).  
- Generate unique barcodes for each uploaded letter for tracking and verification.  
- Allow third parties to verify letter status via barcode scanning or manual entry without accessing the letter content.  
- Notify the CEO via email for pending verifications with direct links to approve or reject.  
- Offer admin capabilities to manage users and customize the dashboard with company branding (logo and name).  

### 3. Key Features

#### 3.1 User Management
- **Admin Panel:**  
  - Create, edit, and remove users.  
  - Assign user roles: Admin, CEO, User.  
- **Authentication:**  
  - Secure login for internal users (Admin, CEO, User).  
  - Role-based access control to restrict functionalities based on user type.  

#### 3.2 Dashboard
- **Summary View:**  
  - Display counts of Verified, Pending, and Rejected letters.  
  - Visual charts or widgets for quick status overview.  
- **Branding:**  
  - Customizable company logo and name displayed on the dashboard.  

#### 3.3 Letter Management
- **Upload Letter:**  
  - Users can upload PDF letters.  
  - Option to mark for CEO verification.  
  - Automatic generation of a unique barcode and number for each letter upon upload.  
- **CEO Verification:**  
  - CEO receives email notification with a direct link to review the letter.  
  - Options to Approve or Reject the letter with comments (optional).  
  - Status updates reflected in the system immediately.  
- **Status Tracking:**  
  - Internal users can view detailed status (Uploaded by, Upload Date, Verified by, Verified Date).  
  - Third parties can access a public-facing page via barcode scan or URL to view limited status information (Approved or Not Approved) without seeing the letter content.  

#### 3.4 Barcode Generation and Verification
- **Unique Identifier:**  
  - Each letter generates a unique barcode and associated number.  
- **Public Verification:**  
  - Third parties can scan the barcode or manually enter the number to access a public page showing the letter’s verification status.  
  - Displayed information: Uploaded by (Full Name), Verified by CEO (Full Name), Upload Date, Verified Date.  

#### 3.5 Email Notifications
- **CEO Notification:**  
  - Automated email sent to CEO upon new letter upload for verification.  
  - Email includes a direct link to review and action (Approve/Reject).  
- **SMTP Integration:**  
  - Use SendGrid API for email delivery.  
- **Email Templates:**  
  - Customizable templates for notification emails (e.g., new letter pending, status update).  

#### 3.6 Sidebar Navigation
- **Menu Items:**  
  - Dashboard (Summary View).  
  - Create New Letter (Upload PDF).  
  - Letter Status (View all letters and their statuses).  
  - User Management (Admin only).  
  - Settings (Branding customization, email settings).  

#### 3.7 Mobile Responsiveness
- Ensure all features are fully functional and visually optimized on mobile devices.  
- Responsive design for dashboard, forms, and public verification page.  

### 4. Technical Requirements
#### 4.1 Tech Stack
- **Backend:** Python with Flask or Django framework for simplicity and speed, suitable for shared hosting.  
- **Frontend:** HTML, CSS, JavaScript (with frameworks like Bootstrap for responsive design).  
- **Database:** MySQL for storing user data, letter metadata, and verification statuses.  
- **Email Service:** SendGrid API for SMTP email notifications.  
- **Barcode Generation:** Use a Python library like `python-barcode` or `qrcode` for generating unique barcodes/QR codes.  

#### 4.2 Hosting
- Deployable on shared hosting with support for Python, MySQL, and basic web server configurations (e.g., Apache/Nginx).  

#### 4.3 Security
- Secure file uploads (PDF only, size limits, virus scanning if feasible).  
- Encrypted storage of sensitive data (e.g., user credentials).  
- Public verification page restricted to status information only, no access to letter content.  
- HTTPS enforcement for all connections.  

### 5. User Roles and Permissions
| Role      | Permissions                                                                 |
|-----------|-----------------------------------------------------------------------------|
| Admin     | Full access: Manage users, view all letters, customize branding, settings. |
| CEO       | View letters assigned for verification, approve/reject letters.            |
| User      | Upload letters, view own uploaded letters’ status.                         |
| Third Party | Access public verification page via barcode/URL (status only).             |

### 6. Workflow
1. **Letter Upload:**  
   - User logs in, navigates to "Create New Letter," uploads PDF, and marks for CEO verification if needed.  
   - System generates unique barcode and number, stores metadata in database.  
2. **CEO Notification:**  
   - Email sent to CEO with link to review letter.  
3. **CEO Action:**  
   - CEO clicks link, reviews PDF, selects Approve or Reject.  
   - Status updated in system, optional notification to uploader.  
4. **Third-Party Verification:**  
   - External party scans barcode or enters number on public page, views status (Approved/Not Approved) and metadata (Uploader, Verifier, Dates).  
5. **Admin Oversight:**  
   - Admin monitors dashboard, manages users, and customizes system settings.  

### 7. Non-Functional Requirements
- **Performance:** System should handle up to 100 concurrent users with minimal latency on shared hosting.  
- **Scalability:** Design database and architecture to allow future scaling if moved to dedicated hosting.  
- **Usability:** Intuitive UI/UX, minimal training required for internal users.  
- **Accessibility:** Follow WCAG 2.1 Level AA standards for web accessibility.  

### 8. Constraints
- Must be deployable on shared hosting with limited server control.  
- Budget-friendly tech stack (open-source tools preferred).  
- Development timeline: To be determined, but simplicity prioritized for quick deployment.  

### 9. Future Enhancements
- Integration with digital signature tools for electronic signing by CEO.  
- Multi-language support for international third-party access.  
- Advanced analytics for letter processing times and user activity.  

### 10. Deliverables
- Fully functional web application meeting all specified requirements.  
- Documentation for deployment on shared hosting.  
- User manuals for Admin, CEO, User, and third-party verification process.  
- Email templates for notifications.  

### 11. Approval
**Prepared by:** [Your Name/Team]  
**Date:** [Insert Date]  
**Approved by:** [Stakeholder Name]  
**Date:** [Insert Date]  