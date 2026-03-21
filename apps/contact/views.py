import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .forms import ContactForm

logger = logging.getLogger(__name__)


@require_POST
@csrf_protect
def contact_submit(request):
    """AJAX contact form handler with spam protection."""
    form = ContactForm(request.POST)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject_choice = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        # Send user auto-reply
        try:
            user_subject = f"We received your message – {settings.SITE_NAME}"
            user_context = {
                'name': name,
                'site_name': settings.SITE_NAME,
                'subject': subject_choice,
            }
            user_text = render_to_string('emails/contact_autoreply.txt', user_context)
            user_html = render_to_string('emails/contact_autoreply.html', user_context)

            msg = EmailMultiAlternatives(
                user_subject, user_text,
                settings.DEFAULT_FROM_EMAIL, [email]
            )
            msg.attach_alternative(user_html, "text/html")
            msg.send()

            # Admin notification
            admin_subject = f"Contact Form: {subject_choice} – {name}"
            admin_text = f"""
New contact form submission:

Name: {name}
Email: {email}
Subject: {subject_choice}

Message:
{message}
"""
            from django.core.mail import send_mail
            send_mail(admin_subject, admin_text, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

        except Exception as e:
            logger.error(f"Contact email error: {e}")

        return JsonResponse({
            'success': True,
            'message': "Thank you! We'll get back to you within 24 hours."
        })

    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)
