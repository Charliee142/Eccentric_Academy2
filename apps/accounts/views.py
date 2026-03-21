from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.payments.models import Enrollment, Payment
from apps.courses.models import Course


@login_required
def dashboard(request):
    """Student dashboard."""
    enrollments = Enrollment.objects.filter(
        user=request.user, is_active=True
    ).select_related('plan').prefetch_related('plan__courses')

    recent_payments = Payment.objects.filter(
        user=request.user
    ).select_related('plan').order_by('-created_at')[:5]

    # Collect all accessible courses
    accessible_courses = Course.objects.filter(
        plans__enrollments__user=request.user,
        plans__enrollments__is_active=True,
        is_published=True
    ).distinct()

    context = {
        'enrollments': enrollments,
        'recent_payments': recent_payments,
        'accessible_courses': accessible_courses,
    }
    return render(request, 'accounts/dashboard.html', context)
