# 🤝 Donation & Volunteer Management System

A comprehensive web application built with **Python Django** designed to facilitate donations and volunteer management with role-based access control for Admins, Donors, and Volunteers.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [User Roles & Functionality](#user-roles--functionality)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [Payment Integration](#payment-integration)
- [Screenshots & Usage](#screenshots--usage)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Donation & Volunteer Management System is a full-stack web application that bridges donors and volunteers to facilitate charitable work efficiently. The platform supports three distinct user roles:

1. **Admin** - Manages the entire system (donations, volunteers, donations areas)
2. **Donor** - Can donate items or contribute money
3. **Volunteer** - Can request donations and collect them from donors

This system streamlines the donation process by connecting donors with volunteers who collect and deliver donations to needy areas.

---

## ✨ Features

### 🔐 Authentication & Authorization
- Role-based login system (Admin, Donor, Volunteer)
- Secure user registration with email verification
- Password reset functionality via email
- Session management

### 👨‍💼 Admin Dashboard
- View and manage all donations (pending, accepted, rejected, delivered)
- Allocate volunteers to donation tasks
- Create and manage donation areas
- Monitor donor and volunteer profiles
- Approve/reject new volunteers
- Track donation collection status
- Generate donation reports

### 💝 Donor Features
- Create donor account with profile picture and contact info
- Post donations (Food, Clothes, Footwear, Books, Furniture, Vessels, Other)
- Upload donation images
- Specify collection location
- Track donation status in real-time
- Make monetary donations via Razorpay payment gateway
- View donation history
- Receive email confirmations

### 🙋 Volunteer Features
- Create volunteer account with ID verification
- Request donation collection assignments
- View assigned donations
- Track collection status
- Add remarks and collection proof (images)
- View collection history with delivery status
- Accept/reject collection requests

### 💳 Payment Integration
- **Razorpay Payment Gateway** integration
- Secure monetary donations
- Payment success/failure handling
- Transaction tracking

### 📸 Gallery & Media
- Upload donation images during registration
- Share delivery proof photos
- View donation collection history with images

### 📧 Email Notifications
- Account registration confirmation
- Donation status updates
- Volunteer assignment notifications
- Payment success emails

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 5.1 (Python Web Framework)
- **Database**: MySQL
- **Authentication**: Django Built-in Auth System
- **Email Service**: Django Mail
- **Payment Gateway**: Razorpay API

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with custom stylesheets
- **Bootstrap 5** - Responsive UI Framework
- **JavaScript** - Client-side interactivity
- **jQuery** - DOM manipulation
- **DataTables** - Advanced table functionality (sorting, searching, pagination)
- **Font Awesome** - Icon library

### Additional Libraries
- **Pillow** - Image processing
- **python-decouple** - Environment variable management

---

## 📁 Project Structure

```
Donation-Volunteer-System/
├── don_vol_system/                 # Main Django project folder
│   ├── don_vol_system/
│   │   ├── settings.py            # Django configuration
│   │   ├── urls.py                # Main URL routing
│   │   ├── wsgi.py                # WSGI configuration
│   │   └── asgi.py                # ASGI configuration
│   │
│   ├── app/                        # Main Django app
│   │   ├── models.py              # Database models
│   │   ├── views.py               # View logic (Admin, Donor, Volunteer)
│   │   ├── forms.py               # Django forms
│   │   ├── admin.py               # Django admin configuration
│   │   │
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   ├── bootstrap.css
│   │   │   │   ├── style.css      # Main stylesheet
│   │   │   │   └── style-admin.css # Admin dashboard styles
│   │   │   ├── js/
│   │   │   │   └── myscript.js    # Custom JavaScript
│   │   │   └── images/
│   │   │       ├── logo1.png
│   │   │       └── helping-hand.png
│   │   │
│   │   ├── templates/
│   │   │   ├── base.html          # Base template (navbar, footer)
│   │   │   ├── base-footer.html   # Footer template
│   │   │   ├── base-db-donor.html     # Donor dashboard base
│   │   │   ├── base-db-volunteer.html # Volunteer dashboard base
│   │   │   ├── base-db-admin.html     # Admin dashboard base
│   │   │   │
│   │   │   ├── index.html         # Home page
│   │   │   ├── gallery.html       # Gallery page
│   │   │   │
│   │   │   ├── login-admin.html
│   │   │   ├── login-donor.html
│   │   │   ├── login-volunteer.html
│   │   │   ├── signup_donor.html
│   │   │   ├── signup_volunteer.html
│   │   │   │
│   │   │   ├── makepayment.html   # Payment form
│   │   │   ├── success.html       # Payment success page
│   │   │   │
│   │   │   ├── password_reset.html
│   │   │   ├── password_reset_done.html
│   │   │   ├── password_reset_confirm.html
│   │   │   └── password_reset_complete.html
│   │   │
│   │   └── migrations/            # Database migrations
│   │
│   ├── manage.py                  # Django management script
│   └── db.sqlite3                 # SQLite database (local dev)
│
└── README.md                       # This file

```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/tushar75083/Donation-Volunteer-System.git
cd Donation-Volunteer-System
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
Edit `don_vol_system/don_vol_system/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "don_vol_system",
        "USER": "root",              # Your MySQL username
        "PASSWORD": "tushar@123",    # Your MySQL password
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

Create the MySQL database:
```bash
# Open MySQL command line and run:
CREATE DATABASE don_vol_system;
```

### Step 5: Run Migrations
```bash
cd don_vol_system
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create admin credentials.

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

---

## 🔧 Configuration

### Email Configuration
Edit `don_vol_system/settings.py` for email settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Razorpay Payment Gateway
1. Sign up at [Razorpay](https://razorpay.com)
2. Get your API keys
3. Update in `makepayment.html`:
```javascript
data-key="YOUR_RAZORPAY_KEY_ID"
```

### Static Files & Media
Create directories for uploads:
```bash
mkdir -p media/donor
mkdir -p media/volunteer
mkdir -p media/donation
```

Configure in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 👥 User Roles & Functionality

### 🔑 Admin Dashboard

**URL**: `/index-admin/`

**Capabilities**:
- **Donation Management**
  - View pending donations → Accept/Reject
  - Allocate volunteers to donations
  - Track collection status
  - View received/not received donations
  - View delivered donations
  
- **Volunteer Management**
  - Approve new volunteer registrations
  - View all volunteer profiles
  - Add remarks to volunteer applications
  
- **Donor Management**
  - View all registered donors
  - Monitor donation history
  
- **Donation Areas**
  - Create new donation collection areas
  - Manage area information

### 💝 Donor Dashboard

**URL**: `/index-donor/`

**Capabilities**:
- Post item donations (Food, Clothes, Books, etc.)
- Make monetary donations
- Track donation status (Pending → Accepted → Assigned → Collected → Delivered)
- View delivery gallery/proof
- See complete donation history
- Manage profile information

### 🙋 Volunteer Dashboard

**URL**: `/index-volunteer/`

**Capabilities**:
- View donation collection requests
- Accept/reject collection assignments
- Track assigned donations
- Add collection remarks
- Upload delivery proof images
- View collection history
- Update profile status

---

## 📊 Database Schema

### User Model (Django Built-in)
- `id`, `username`, `password`, `first_name`, `last_name`, `email`, `is_staff`, etc.

### Donor Model
```python
- user (ForeignKey to User)
- contact (CharField)
- address (CharField)
- userpic (ImageField)
- regdate (DateTimeField)
```

### Volunteer Model
```python
- user (ForeignKey to User)
- contact (CharField)
- address (CharField)
- userpic (ImageField)
- idpic (ImageField)
- aboutme (CharField)
- status (CharField)
- adminremark (CharField)
- regdate (DateTimeField)
- updationdate (DateField)
```

### DonationArea Model
```python
- areaname (CharField)
- description (CharField)
- creationdate (DateTimeField)
```

### Donation Model
```python
- donor (ForeignKey to Donor)
- donationname (CharField - choices)
- donationpic (ImageField)
- collectionloc (CharField)
- description (CharField)
- status (CharField - Pending/Accepted/Assigned/Collected/Delivered)
- donationdate (DateField)
- volunteer (ForeignKey to Volunteer)
- donationarea (ForeignKey to DonationArea)
- volunteerremark (CharField)
- updationdate (DateField)
```

### Gallery Model
```python
- donation (ForeignKey to Donation)
- deliverypic (FileField)
- creationdate (DateTimeField)
```

### Payment Model
```python
- name (CharField)
- amount (IntegerField)
- razorpay_order_id (CharField)
- razorpay_payment_id (CharField)
- razorpay_signature (CharField)
- ispaid (BooleanField)
- created_at (DateTimeField)
```

---

## 🌐 API Routes

### Public Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/gallery/` | GET | View donation gallery |

### Authentication Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/login-admin/` | GET, POST | Admin login |
| `/login-donor/` | GET, POST | Donor login |
| `/login-volunteer/` | GET, POST | Volunteer login |
| `/signup-donor/` | GET, POST | Donor registration |
| `/signup-volunteer/` | GET, POST | Volunteer registration |

### Password Recovery
| Route | Method | Purpose |
|-------|--------|---------|
| `/password-reset/` | GET, POST | Request password reset |
| `/password-reset/done/` | GET | Reset link sent confirmation |
| `/password-reset-confirm/<uidb64>/<token>/` | GET, POST | Reset password |
| `/password-reset-complete/` | GET | Reset successful |

### Admin Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/index-admin/` | GET | Admin dashboard |
| `/pending-donation/` | GET | View pending donations |
| `/accepted-donation/` | GET | View accepted donations |
| `/rejected-donation/` | GET | View rejected donations |
| `/volunteerallocated-donation/` | GET | View allocated donations |
| `/donationrec-admin/` | GET | Donations received |
| `/donationnotrec-admin/` | GET | Donations not received |
| `/donationdelivered-admin/` | GET | Delivered donations |
| `/all-donations/` | GET | All donations list |
| `/manage-donor/` | GET | Manage donors |
| `/new-volunteer/` | GET | New volunteer approvals |
| `/accepted-volunteer/` | GET | Accepted volunteers |

### Donor Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/index-donor/` | GET | Donor dashboard |
| `/donate-now/` | GET, POST | Create donation |
| `/payment/` | GET, POST | Make monetary donation |
| `/success/` | POST | Payment success |
| `/donation-history/` | GET | View donation history |

### Volunteer Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/index-volunteer/` | GET | Volunteer dashboard |
| `/collection-req/` | GET | View collection requests |
| `/collection-history/` | GET | View collection history |

---

## 💳 Payment Integration

### Razorpay Integration
The system integrates **Razorpay** for secure online payments:

1. **Payment Flow**:
   - Donor enters donation amount
   - Payment form is generated with Razorpay checkout
   - Razorpay handles payment securely
   - On success, record is saved to database
   - Success page displays confirmation

2. **Implementation Files**:
   - `makepayment.html` - Payment form template
   - `success.html` - Success confirmation page
   - `views.py` - Payment processing logic

3. **Payment Status Tracking**:
   - Donations marked as paid in database
   - Transaction history maintained
   - Email confirmations sent

---

## 📸 Screenshots & Usage

### Home Page
- Navigation with login/signup options
- Information about donation system
- Donation and volunteer sections
- Contact information

### Donor Workflow
1. Sign up with profile picture
2. Login to dashboard
3. Post donations with images
4. Track status in real-time
5. Receive updates on collection
6. View delivery proof in gallery

### Volunteer Workflow
1. Sign up with ID verification
2. Await admin approval
3. Login to dashboard
4. View collection requests
5. Accept/reject assignments
6. Upload delivery proof
7. Track collection history

### Admin Workflow
1. Login to admin dashboard
2. Approve new volunteers
3. Review donations
4. Allocate volunteers
5. Monitor collection status
6. View completion reports

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Write descriptive commit messages
- Test changes before submitting PR
- Update documentation accordingly

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📧 Contact & Support

For issues, suggestions, or questions:
- **GitHub**: [tushar75083](https://github.com/tushar75083)
- **Email**: tushar75083@gmail.com

---

## 🚀 Future Enhancements

- [ ] Mobile app for iOS/Android
- [ ] Real-time notifications (WebSockets)
- [ ] SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Export donation reports (PDF)
- [ ] QR code donation tracking
- [ ] Rating system for volunteers
- [ ] Donation impact metrics
- [ ] Multi-language support
- [ ] API REST endpoints

---

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Razorpay Documentation](https://razorpay.com/docs/)
- [jQuery Documentation](https://jquery.com/)

---

**Last Updated**: October 2024  
**Version**: 1.0.0
