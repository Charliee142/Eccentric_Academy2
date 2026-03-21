# 🛡️ Eccentric Academy
### Nigeria's Premier Cybersecurity Learning Platform

A **production-grade, plan-based cybersecurity learning platform** built with Django — designed for Nigerian security professionals and students. Featuring Paystack payments in Naira, security-first architecture, and a dark terminal-themed UI.

---

## ✨ Features

- **Plan-Based Enrollment** — Pay once per tier (Beginner/Intermediate/Advanced), unlock all courses
- **Paystack Integration** — Secure NGN payments via card, bank transfer, USSD
- **Server-Side Verification** — Fraud-proof payment verification before granting access
- **Django Allauth Auth** — Secure email-based authentication with CSRF & XSS protection
- **AJAX Contact Form** — No page reload, honeypot spam protection, auto-reply emails
- **Admin Dashboard** — Full course, plan, enrollment & payment management
- **Nigeria-Optimized** — WAT timezone, Naira pricing, locally relevant course content

---

## 🚀 Quick Start

### 1. Clone & Set Up

```bash
git clone https://github.com/yourname/eccentric-academy.git
cd eccentric-academy

python -m venv venv

venv\Scripts\activate


pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings:
# - SECRET_KEY (generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# - PAYSTACK_PUBLIC_KEY and PAYSTACK_SECRET_KEY (from paystack.com/dashboard)
# - Email SMTP settings
```

### 3. Database & Static Files

```bash
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py collectstatic --noinput
```

### 4. Create Superuser & Run

```bash
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://localhost:8000  
Admin: http://localhost:8000/admin/

---

## 💳 Paystack Setup (Nigeria)

1. Register at [paystack.com](https://paystack.com)
2. Get your **Test Keys** from Dashboard → Settings → API Keys
3. Add to `.env`:
   ```
   PAYSTACK_PUBLIC_KEY=pk_test_xxxx
   PAYSTACK_SECRET_KEY=sk_test_xxxx
   ```
4. For production, switch to **Live Keys** and verify your business

**Supported payment channels:** Cards (Verve, Mastercard, Visa), Bank Transfer, USSD, Mobile Money

---

## 📁 Project Structure

```
eccentric_academy/
├── eccentric_academy/     # Django project config
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── core/              # Landing page, home, about
│   ├── accounts/          # Student dashboard
│   ├── courses/           # Plans, courses, catalog
│   ├── payments/          # Paystack integration, enrollments
│   └── contact/           # AJAX contact form
├── templates/
│   ├── base.html
│   ├── core/, accounts/, courses/, payments/
│   └── emails/            # HTML + text email templates
├── static/
│   ├── css/main.css       # Dark cyberpunk theme
│   └── js/main.js         # AJAX, countdown, animations
├── fixtures/
│   └── initial_data.json  # Sample plans & courses
├── .env.example
└── requirements.txt
```

---

## 🛡️ Security Architecture

| Layer | Implementation |
|-------|---------------|
| Auth | Django Allauth — email-based, session management |
| CSRF | Django middleware on all forms |
| XSS | Django auto-escaping in templates |
| Payments | Server-side Paystack verification (`/transaction/verify/`) |
| Spam | Honeypot field on contact form |
| Secrets | python-dotenv — no credentials in code |
| Production | HSTS, secure cookies, SSL redirect via settings |

---

## 🌍 Nigerian Localization

- **Currency:** Nigerian Naira (NGN) — ₦ symbol throughout
- **Timezone:** Africa/Lagos (WAT)
- **Payment:** Paystack (Nigeria's leading gateway)
- **Content:** Nigerian instructors, local context, Nigerian cybersecurity focus
- **Support Hours:** Mon–Fri, 8AM–6PM WAT

---

## 📧 Email Flow

1. **Enrollment Confirmation** → User gets beautiful HTML email with payment reference
2. **Admin Notification** → Admin gets instant alert on new enrollments
3. **Contact Auto-Reply** → Contact form submitters get auto-reply within seconds

---

## 🚢 Deployment (PythonAnywhere)

```bash
# 1. Upload project to PythonAnywhere
# 2. Create virtualenv and install requirements
# 3. Set DEBUG=False in .env
# 4. Configure WSGI file to point to eccentric_academy/wsgi.py
# 5. Add static files mapping in PythonAnywhere dashboard
# 6. Set all environment variables in PythonAnywhere's .env
```

For PostgreSQL in production, set `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

---

## 🎨 UI Theme

- **Design:** Dark cyberpunk / terminal aesthetic
- **Colors:** Midnight black (#0a0d14) + Cyber green (#00e5a0)
- **Fonts:** Space Mono (headings/code) + DM Sans (body)
- **Components:** Bootstrap 5 + custom CSS variables
- **Animations:** CSS keyframes, intersection observer, countdown timer

---

## 📞 Support

- **Email:** hello@eccentricacademy.ng
- **WhatsApp:** +234 (0) 800 ECCENTRIC
- **Location:** Lagos & Abuja, Nigeria

---

*Built with 🛡️ by Eccentric Academy — Defending Nigeria's Digital Future*
