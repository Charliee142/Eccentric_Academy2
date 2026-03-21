from django.shortcuts import render
from apps.courses.models import Plan, Course
from apps.payments.models import Enrollment


def home(request):
    """Landing page."""
    plans = Plan.objects.filter(is_active=True).prefetch_related('courses')
    featured_courses = Course.objects.filter(is_published=True, is_featured=True)[:6]
    total_students = Enrollment.objects.filter(is_active=True).values('user').distinct().count()
    total_courses = Course.objects.filter(is_published=True).count()

    context = {
        'plans': plans,
        'featured_courses': featured_courses,
        'total_students': total_students,
        'total_courses': total_courses,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
