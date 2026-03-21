# Eccentric_Academy2
**Eccentric Academy** — Nigeria's Premier Ethical Hacking &amp; Web Development School
<div align="center">

<img src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"/>
<img src="https://img.shields.io/badge/Paystack-NGN-00C3F7?style=for-the-badge&logo=stripe&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-Production_Ready-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>

<br/><br/>


### Nigeria's Premier Ethical Hacking & Web Development School

*A production-grade, plan-based cybersecurity learning platform — built with Django, secured by design, and optimised for Nigerian students.*

<br/>

 [📞 WhatsApp Us](https://wa.me/2349136823282) 

</div>

---

## 📌 Project Name

**Eccentric Academy** — A Plan-Based Cybersecurity Learning Platform Built with Django

---

## 📖 Description

Eccentric Academy is a **production-grade cybersecurity and web development learning platform** built specifically for Nigerian students and professionals. It delivers three structured training programmes — from absolute beginners to advanced red team operators — through a plan-based enrollment model where students pay once and unlock every course in their tier.

The platform is built **security-first**, using the same defensive principles taught in its curriculum. Every feature — from payment verification to session management — reflects real-world security best practices, making it both a learning tool and a live demonstration of secure Django development.

> *"Your future is coded — let us help you write it."*

---

## ❗ Problem It Solves

Most online learning platforms suffer from the same critical failures:

| Problem | How Eccentric Academy Solves It |
|---------|--------------------------------|
| 🔓 Weak post-payment access enforcement | Server-side ownership validation before every course load |
| 💳 Fragmented per-course purchases | Plan-based enrollment — pay once, access everything in your tier |
| 🌍 No Nigerian payment support | Full Paystack integration (Naira, cards, bank transfer, USSD) |
| 🤷 Jargon-heavy, inaccessible teaching | Taught in plain Naija English with everyday Nigerian examples |
| 🕳️ No real projects to show employers | 8+ signature projects built by the instructor — students build their own versions |
| 🛡️ No defensive security training | Dedicated Blue Team module — most hacking courses never teach defence |
| 📉 Poor UX conversion flows | Countdown CTA, seat scarcity indicators, AJAX forms, WhatsApp CTAs |

---

## ✨ Features

### 🎓 Learning Platform
- **3 Structured Programmes** — Cybersecurity for Beginners (11 phases), Cisco Introduction to Cybersecurity (5 modules), Web Development with Django (full stack)
- **Plan-Based Enrollment** — Beginner (₦45,000), Intermediate (₦85,000), Advanced (₦150,000) — pay once, access all courses in your tier
- **Access Control Middleware** — course pages verify plan ownership on every request
- **Admin Dashboard** — full management of plans, courses, enrollments, and payments
- **Course Catalog** — filter by category and difficulty, locked/unlocked state per user

### 💳 Payments & Enrollment
- **Paystack Integration** — Nigeria's most trusted payment gateway
- **Server-Side Payment Verification** — no client-side spoofing possible
- **UUID-Based Payment Records** — tamper-resistant payment references
- **Flexible Payment Plans** — monthly installment options for every tier
- **Ownership Validation** — "You already own this plan" detection

### 🔒 Security Architecture
- **Django Allauth** — email-based authentication, email verification, secure session management
- **CSRF Protection** — Django middleware active on every form and POST request
- **XSS-Safe Rendering** — Django template auto-escaping throughout
- **Honeypot Spam Protection** — hidden field on contact form to block bots
- **Environment Variables** — all secrets in `.env`, never committed to version control
- **Production Hardening** — HSTS, secure cookies, SSL redirect, X-Frame-Options

### 🎨 UX & Design
- **Dark Terminal Theme** — midnight black + cyber green palette built for cybersecurity context
- **Space Mono + DM Sans** — distinctive font pairing (heading/code + body)
- **Animated Terminal Hero** — live typing effect simulating a real hacking session
- **Countdown Timer** — early-bird enrollment urgency
- **AJAX Contact Form** — no page reload, inline feedback, auto-reply email
- **Fully Responsive** — Bootstrap 5, mobile-first layout

### 📧 Communication
- **Enrollment Confirmation Email** — HTML + plain text, sent on verified payment
- **Admin Notification Email** — instant alert on every new enrollment
- **Contact Auto-Reply** — user gets immediate confirmation on form submit

---

## 🧰 Tech Stack

```
Backend         Django 5.0 · Python 3.12 · Django Allauth · python-dotenv
Frontend        Bootstrap 5.3 · Space Mono · DM Sans · Vanilla JS (AJAX)
Database        SQLite (development) · PostgreSQL-ready (production)
Payments        Paystack API (NGN — cards, bank transfer, USSD, mobile money)
Static Files    WhiteNoise · Django staticfiles
Email           Django SMTP (Gmail) · HTML + plain text dual-format
Deployment      PythonAnywhere-ready · Gunicorn · WSGI
Security        Django Allauth · CSRF · XSS-safe · HSTS · Honeypot · python-dotenv
```

---

## 🛡️ Security Measures

Eccentric Academy was designed with **security-first principles** — the same practices taught in the curriculum.

### Authentication & Sessions
```python
# settings.py — production security headers
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_HSTS_SECONDS             = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_PRELOAD             = True
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
X_FRAME_OPTIONS                 = 'DENY'
```

### Payment Security
```python
# payments/utils.py — server-side Paystack verification
def verify_paystack_payment(reference):
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    response = requests.get(f"{PAYSTACK_VERIFY_URL}{reference}", headers=headers)
    data = response.json()
    # Access granted ONLY if Paystack confirms status == 'success'
    if data.get('status') and data['data']['status'] == 'success':
        return True, data['data']
    return False, {}
```

### Access Control
```python
# courses/views.py — ownership check before every course load
@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    has_access = Enrollment.objects.filter(
        user=request.user,
        plan__in=course.plans.all(),
        is_active=True
    ).exists()
    if not has_access:
        messages.warning(request, "You need an active plan to access this course.")
        return redirect('courses:pricing')
```

### Secrets Management
```bash
# .env — never committed to version control
SECRET_KEY=your-secret-key-here
PAYSTACK_PUBLIC_KEY=pk_live_xxxx
PAYSTACK_SECRET_KEY=sk_live_xxxx
EMAIL_HOST_PASSWORD=your-app-password
```

### Anti-Spam
```python
# contact/forms.py — honeypot field
class ContactForm(forms.Form):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        """Honeypot — must always be empty. Bots fill it, humans don't."""
        if self.cleaned_data.get('website'):
            raise forms.ValidationError("Spam detected.")
        return ''
```

---

## 📸 Screenshots / Demo

> **Note:** Replace the placeholder paths below with actual screenshots before pushing to GitHub. Use `git lfs` or a public image hosting service for large images.

### 🏠 Landing Page — Hero Section
```
screenshots/01_hero.png
Dark terminal aesthetic with animated typing effect, WhatsApp contact pills,
programme stats (3 programmes · 11 phases · 8+ real projects), and dual CTA buttons.
```

### 📋 Curriculum Section — 3 Programmes
```
screenshots/02_programmes.png
Colour-coded programme cards: green for Cybersecurity Beginners (11 phases listed),
orange for Cisco, blue for Django Web Development.
```

### 💰 Pricing Cards — Plan-Based Enrollment
```
screenshots/03_pricing.png
Three pricing tiers (₦45,000 / ₦85,000 / ₦150,000) with live countdown timer,
seat availability bar, feature lists, and Paystack enrollment buttons.
```

### 🔒 Login / Signup Pages
```
screenshots/04_auth.png
Dark-themed auth cards with show/hide password toggle, security indicators,
Space Mono branding, and responsive layout.
```

### 📊 Student Dashboard
```
screenshots/05_dashboard.png
Stat boxes (active plans, accessible courses, payments), enrollment cards
with plan details, course grid, and payment history sidebar.
```

### 💳 Paystack Checkout
```
screenshots/06_checkout.png
Secure checkout summary card with plan details, NGN amount,
security trust indicators, and Paystack redirect button.
```

### 📬 Contact Page
```
screenshots/07_contact.png
Standalone contact page with AJAX form, WhatsApp quick-chat cards,
FAQ accordion, and social links.
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/eccentric-academy.git
cd eccentric-academy
```

### 2. Create & Activate Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
# Generate a secret key:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-generated-secret-key

DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Paystack — get keys from paystack.com/dashboard
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxx
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxx

# Email (Gmail SMTP — use an App Password, not your main password)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=Eccentric Academy <youremail@gmail.com>
ADMIN_EMAIL=youremail@gmail.com

SITE_NAME=Eccentric Academy
SITE_URL=http://localhost:8000
```

> 💡 **Gmail App Password:** Go to Google Account → Security → 2-Step Verification → App passwords. Generate one for "Mail".

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Load Sample Data (Plans & Courses)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 7. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 9. Start the Development Server

```bash
python manage.py runserver
```

Open your browser:

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Landing page |
| `http://localhost:8000/admin/` | Admin dashboard |
| `http://localhost:8000/accounts/login/` | Login |
| `http://localhost:8000/accounts/signup/` | Sign up |
| `http://localhost:8000/dashboard/` | Student dashboard |
| `http://localhost:8000/courses/` | Course catalog |
| `http://localhost:8000/courses/pricing/` | Pricing plans |
| `http://localhost:8000/contact/` | Contact page |

---

## 🚀 Deployment (PythonAnywhere)

PythonAnywhere is the recommended hosting for this project — it's Django-native and Nigeria-accessible.

```bash
# 1. Upload your project to PythonAnywhere via Git or zip upload

# 2. Open a Bash console on PythonAnywhere and run:
pip install -r requirements.txt --user
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py collectstatic --noinput

# 3. In the PythonAnywhere Web tab:
#    - Set WSGI file to point to: eccentric_academy/wsgi.py
#    - Add static files: /static/ → /home/yourusername/eccentric_academy/staticfiles/
#    - Add environment variables (the contents of your .env file)
#    - Set DEBUG=False

# 4. Reload your web app and visit your URL
```

For **PostgreSQL** in production, add to `.env`:
```env
DATABASE_URL=postgresql://username:password@hostname:5432/dbname
```

---

## 📁 Project Structure

```
eccentric_academy/
│
├── eccentric_academy/          # Django project configuration
│   ├── settings.py             # All settings, env-based
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI entry point
│
├── apps/
│   ├── core/                   # Landing page, home, about, error pages
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── context_processors.py
│   │
│   ├── accounts/               # Student dashboard
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── courses/                # Plans, courses, catalog, access control
│   │   ├── models.py           # Plan, Course, Category, Module, Lesson
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── urls.py
│   │
│   ├── payments/               # Paystack integration, enrollments
│   │   ├── models.py           # Payment (UUID PK), Enrollment
│   │   ├── views.py            # initiate_payment, verify_payment
│   │   ├── utils.py            # verify_paystack_payment(), send_enrollment_confirmation()
│   │   ├── admin.py
│   │   └── urls.py
│   │
│   └── contact/                # AJAX contact form + standalone page
│       ├── views.py            # contact_page(), contact_submit()
│       ├── forms.py            # ContactForm with honeypot
│       └── urls.py
│
├── templates/
│   ├── base.html               # Navbar, footer, messages — inherited by all pages
│   ├── account/                # Django Allauth auth pages
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── logout.html
│   │   ├── password_reset.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_from_key.html
│   │   ├── password_reset_from_key_done.html
│   │   ├── password_change.html
│   │   ├── email_confirm.html
│   │   └── email.html
│   ├── core/                   # home.html, about.html
│   ├── accounts/               # dashboard.html
│   ├── courses/                # catalog.html, pricing.html, plan_detail.html, course_detail.html
│   ├── payments/               # checkout.html, history.html
│   ├── contact/                # contact.html (standalone page)
│   └── emails/                 # HTML + text email templates
│       ├── enrollment_confirmation.html
│       ├── enrollment_confirmation.txt
│       ├── contact_autoreply.html
│       └── contact_autoreply.txt
│
├── static/
│   ├── css/main.css            # Full custom CSS — dark theme, all components
│   ├── js/main.js              # AJAX contact, countdown timer, animations
│   ├── downloads/              # Eccentric_Academy_Full_Brochure.pdf
│   └── images/                 # Flyer and other assets
│
├── fixtures/
│   └── initial_data.json       # 3 plans + 6 courses + categories seed data
│
├── .env.example                # Template for environment variables
├── .gitignore                  # Excludes .env, db.sqlite3, __pycache__, media/
├── requirements.txt            # All Python dependencies
└── manage.py
```

---

## 🧠 What I Learned

Building Eccentric Academy was a full-stack, real-world learning experience. Here are the key lessons from every layer of the project:

### 1. Django Architecture at Scale
Structuring a Django project as a **multi-app system** (`core`, `accounts`, `courses`, `payments`, `contact`) rather than a monolithic app taught me how to think about separation of concerns. Each app owns its models, views, URLs, and admin — making the codebase maintainable and scalable. I learned when to put logic in views vs. utility functions (like `verify_paystack_payment()` living in `payments/utils.py`).

### 2. Payment Integration Is About Trust, Not Just Code
Integrating **Paystack** taught me that payment security is not just about making an API call — it is about verifying the result server-side and never trusting client-side data. The biggest lesson: always re-verify payment status from the payment provider's server before granting any access. I also learned how to generate tamper-resistant references using UUIDs and timestamps.

### 3. Django Allauth Customisation
Out of the box, Allauth handles authentication well — but customising its templates to match a specific design system required understanding how Allauth's template discovery works (`templates/account/` not `templates/accounts/`), how to pass context to allauth views, and how to override specific flows like email verification and password reset with custom UI.

### 4. Access Control Is a Business Logic Problem
I learned that **who can see what** is not just a Django permissions question — it is a business logic question. Building the plan-based access system (`has_access = Enrollment.objects.filter(user, plan__in=course.plans.all(), is_active=True).exists()`) taught me to always verify ownership server-side on every request, never cache access state on the frontend, and design models that make access queries efficient.

### 5. Security Is a Mindset, Not a Checklist
Implementing CSRF, XSS-safe templates, honeypot spam protection, HSTS headers, secure session cookies, and server-side payment verification taught me that security is not something you add at the end — it is something you design into every feature from the start. The most impactful lesson: **client-side data is always untrusted**.

### 6. Environment Variables and Secrets Management
Learning to properly use `python-dotenv` with a `.env.example` template, `.gitignore` enforcement, and separating `DEBUG=True` (development) from `DEBUG=False` (production) settings taught me how professional teams manage secrets across environments. I now understand why hardcoding API keys is catastrophic — a single commit can expose credentials permanently.

### 7. Email in Production Is Hard
Getting Django email to work correctly — HTML + plain text dual format, SMTP configuration, app passwords vs. account passwords, email deliverability to Nigerian inboxes, and graceful failure handling (`try/except` around every `send_mail()`) — taught me that email is a first-class feature that requires as much thought as the database or payment layer.

### 8. Frontend Without a Framework
Building a full, production-quality UI with **Bootstrap 5 + vanilla JavaScript + CSS custom properties** — without React or Vue — taught me how much you can achieve with the fundamentals. The AJAX contact form, countdown timer, show/hide password toggle, and intersection observer animations are all plain JS. I learned that a deep understanding of the DOM is more valuable than framework knowledge.

### 9. UX Conversion Principles
Designing the landing page with Nigerian users in mind — plain language, WhatsApp CTAs, Naira pricing, scarcity indicators (seat counts), a countdown timer, and a personal message section — taught me that UX is fundamentally about removing friction for your specific audience. A conversion-optimised page for a Nigerian audience looks very different from a generic SaaS landing page.

### 10. The Gap Between Working and Production-Ready
The difference between "the feature works locally" and "this is production-ready" is enormous. I learned about `collectstatic`, WhiteNoise for static file serving, `ALLOWED_HOSTS`, `DEBUG=False` implications, database migration management, fixture data for reproducible deployments, and writing a README that lets another developer run the project in under 10 minutes.

---

## 🌍 Nigerian Localisation

| Aspect | Implementation |
|--------|---------------|
| Currency | Nigerian Naira (₦) throughout — `₦45,000`, `₦85,000`, `₦150,000` |
| Timezone | `Africa/Lagos` (WAT — West Africa Time) |
| Payments | Paystack — cards, bank transfer, USSD, mobile money |
| Language | Plain Naija English — everyday examples (GTBank, MTN, JAMB, WhatsApp) |
| Contact | WhatsApp-first — clickable `wa.me` links with pre-filled messages |
| Support | Mon–Fri, 8AM–6PM WAT |
| Audience | Beginners, students, NYSC corps members, professionals, businesses |

---

## 👥 Discounts & Special Offers

| Offer | Discount |
|-------|---------|
| 🐣 Early Bird (first 20 students) | 20% off any level |
| 👫 Refer a Friend | ₦5,000 off your next payment |
| 👩 Women in Tech | 15% off any level |
| 🎓 NYSC / Student ID | 10% off immediately |
| 📦 Full Bundle (all 3 levels) | ₦230,000 — save ₦50,000 |
| 🏢 Corporate / Group (5+) | 30% group discount |

---

## 📞 Contact & Social

| Channel | Details |
|---------|---------|
| 📱 WhatsApp | [+234 9136823282](https://wa.me/2349136823282) |
| 📱 WhatsApp | [+234 9035505885](https://wa.me/2349035505885) |
| 📸 Instagram | [@eccentricacademy](https://instagram.com/eccentricacademy) |
| 🎵 TikTok | [@eccentricacademy](https://tiktok.com/@eccentricacademy) |
| ▶️ YouTube | [@eccentricacademy](https://youtube.com/@eccentricacademy) |
| 🐦 X (Twitter) | [@eccentricacademy](https://x.com/eccentricacademy) |

---

## 📄 License

This project is **proprietary** — all rights reserved by Eccentric Academy.  
The codebase is shared publicly for educational and portfolio purposes.  
You may not use, distribute, or deploy this code commercially without written permission.

---

<div align="center">

Built with 🛡️ by **Eccentric Academy**

*Defending Nigeria's Digital Future — one student at a time.*

**⭐ Star this repo if it helped you learn something new**

</div>
