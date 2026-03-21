import requests
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def verify_paystack_payment(reference):
    """
    Verify a Paystack payment by reference.
    Returns (success: bool, data: dict)
    """
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    url = f"{settings.PAYSTACK_VERIFY_URL}{reference}"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()

        if data.get('status') and data.get('data', {}).get('status') == 'success':
            return True, data['data']
        else:
            logger.warning(f"Paystack verification failed for {reference}: {data}")
            return False, data

    except requests.RequestException as e:
        logger.error(f"Paystack verification request error for {reference}: {e}")
        return False, {}


def send_enrollment_confirmation(user, plan, payment):
    """Send enrollment confirmation email to user and admin notification."""
    # User confirmation email
    subject = f"🎓 Welcome to {plan.name} – Eccentric Academy"
    context = {
        'user': user,
        'plan': plan,
        'payment': payment,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'courses': plan.courses.filter(is_published=True),
    }

    text_content = render_to_string('emails/enrollment_confirmation.txt', context)
    html_content = render_to_string('emails/enrollment_confirmation.html', context)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Admin notification
    admin_subject = f"New Enrollment: {user.email} → {plan.name} (₦{payment.amount:,.0f})"
    admin_text = f"""
New enrollment on Eccentric Academy:

Student: {user.get_full_name() or user.username} ({user.email})
Plan: {plan.name}
Amount: ₦{payment.amount:,.0f}
Reference: {payment.reference}
Date: {payment.paid_at or payment.created_at}
    """

    try:
        from django.core.mail import send_mail
        send_mail(
            admin_subject,
            admin_text,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
    except Exception as e:
        logger.error(f"Admin notification email failed: {e}")
