from django.conf import settings


def site_settings(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
        'PAYSTACK_PUBLIC_KEY': getattr(settings, 'PAYSTACK_PUBLIC_KEY', ''),
    }
