import json
import requests
import logging
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.courses.models import Plan
from .models import Payment, Enrollment
from .utils import verify_paystack_payment, send_enrollment_confirmation

logger = logging.getLogger(__name__)


@login_required
def initiate_payment(request, plan_slug):
    """Initiate payment for a plan."""
    plan = get_object_or_404(Plan, slug=plan_slug, is_active=True)

    # Check if user already has this plan
    existing = Enrollment.objects.filter(
        user=request.user, plan=plan, is_active=True
    ).first()

    if existing:
        messages.info(request, f"You already have access to the {plan.name} plan!")
        return redirect('accounts:dashboard')

    # Check seats availability
    if plan.seats_available > 0 and plan.seats_left == 0:
        messages.error(request, "Sorry, no seats available for this plan.")
        return redirect('courses:pricing')

    if request.method == 'POST':
        # Generate payment reference
        reference = Payment.generate_reference(request.user.id)
        amount_kobo = int(plan.price * 100)  # Paystack uses kobo

        # Create pending payment record
        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            reference=reference,
            amount=plan.price,
            status='pending',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
        )

        # Initialize Paystack transaction
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': request.user.email,
            'amount': amount_kobo,
            'reference': reference,
            'callback_url': request.build_absolute_uri(f'/payments/verify/{reference}/'),
            'metadata': {
                'plan_id': plan.id,
                'plan_name': plan.name,
                'user_id': request.user.id,
                'custom_fields': [
                    {'display_name': 'Plan', 'variable_name': 'plan', 'value': plan.name},
                    {'display_name': 'Customer', 'variable_name': 'customer', 'value': request.user.get_full_name() or request.user.email},
                ]
            }
        }

        try:
            response = requests.post(
                settings.PAYSTACK_INITIALIZE_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            response_data = response.json()

            if response_data.get('status') and response_data.get('data', {}).get('authorization_url'):
                authorization_url = response_data['data']['authorization_url']
                return redirect(authorization_url)
            else:
                logger.error(f"Paystack init failed: {response_data}")
                payment.status = 'failed'
                payment.save()
                messages.error(request, "Payment initialization failed. Please try again.")
                return redirect('courses:pricing')

        except requests.RequestException as e:
            logger.error(f"Paystack request error: {e}")
            payment.status = 'failed'
            payment.save()
            messages.error(request, "Payment service unavailable. Please try again later.")
            return redirect('courses:pricing')

    context = {
        'plan': plan,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'payments/checkout.html', context)


@login_required
def verify_payment(request, reference):
    """Verify payment after Paystack redirect."""
    payment = get_object_or_404(Payment, reference=reference, user=request.user)

    # Prevent re-verification of already processed payments
    if payment.status == 'success':
        messages.success(request, f"You're enrolled in {payment.plan.name}!")
        return redirect('accounts:dashboard')

    if payment.status in ['failed', 'abandoned']:
        messages.error(request, "This payment was not successful.")
        return redirect('courses:pricing')

    # Verify with Paystack
    success, data = verify_paystack_payment(reference)

    if success:
        # Update payment record
        payment.status = 'success'
        payment.paystack_id = str(data.get('id', ''))
        payment.paystack_reference = data.get('reference', '')
        payment.gateway_response = data.get('gateway_response', '')
        payment.channel = data.get('channel', '')
        payment.raw_response = data
        if data.get('paid_at'):
            from django.utils.dateparse import parse_datetime
            payment.paid_at = parse_datetime(data['paid_at'])
        payment.save()

        # Create or activate enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            plan=payment.plan,
            defaults={'is_active': True, 'status': 'active'}
        )
        if not created:
            enrollment.is_active = True
            enrollment.status = 'active'
            enrollment.save()

        payment.enrollment = enrollment
        payment.save()

        # Send confirmation email
        try:
            send_enrollment_confirmation(request.user, payment.plan, payment)
        except Exception as e:
            logger.error(f"Failed to send enrollment email: {e}")

        messages.success(
            request,
            f"🎉 Payment successful! Welcome to the {payment.plan.name} plan. You now have access to all courses."
        )
        return redirect('accounts:dashboard')

    else:
        payment.status = 'failed'
        payment.save()
        messages.error(request, "Payment verification failed. If you were charged, please contact support.")
        return redirect('courses:pricing')


@login_required
def payment_history(request):
    """View user's payment history."""
    payments = Payment.objects.filter(user=request.user).select_related('plan')
    return render(request, 'payments/history.html', {'payments': payments})


def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
