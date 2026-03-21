from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plan, Course, Category
from apps.payments.models import Enrollment


def pricing(request):
    """Pricing / plans page."""
    plans = Plan.objects.filter(is_active=True).prefetch_related('courses')

    user_plans = []
    if request.user.is_authenticated:
        user_plans = list(
            Enrollment.objects.filter(user=request.user, is_active=True)
            .values_list('plan_id', flat=True)
        )

    context = {
        'plans': plans,
        'user_plans': user_plans,
    }
    return render(request, 'courses/pricing.html', context)


def plan_detail(request, slug):
    """Detail page for a plan showing all included courses."""
    plan = get_object_or_404(Plan, slug=slug, is_active=True)
    courses = plan.courses.filter(is_published=True).select_related('category')
    categories = Category.objects.filter(courses__plans=plan, courses__is_published=True).distinct()

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user, plan=plan, is_active=True
        ).exists()

    context = {
        'plan': plan,
        'courses': courses,
        'categories': categories,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/plan_detail.html', context)


@login_required
def course_detail(request, slug):
    """Course detail page - requires enrollment in an eligible plan."""
    course = get_object_or_404(Course, slug=slug, is_published=True)

    # Check if user has access via any of the course's plans
    has_access = Enrollment.objects.filter(
        user=request.user,
        plan__in=course.plans.all(),
        is_active=True
    ).exists()

    if not has_access:
        messages.warning(
            request,
            f"You need to enroll in a plan that includes '{course.title}' to access this course."
        )
        return redirect('courses:pricing')

    modules = course.modules.prefetch_related('lessons')

    context = {
        'course': course,
        'modules': modules,
        'has_access': has_access,
    }
    return render(request, 'courses/course_detail.html', context)


def course_catalog(request):
    """Public course catalog showing available courses."""
    courses = Course.objects.filter(is_published=True).select_related('category').prefetch_related('plans')
    categories = Category.objects.filter(courses__is_published=True).distinct()

    selected_category = request.GET.get('category')
    selected_difficulty = request.GET.get('difficulty')

    if selected_category:
        courses = courses.filter(category__slug=selected_category)
    if selected_difficulty:
        courses = courses.filter(difficulty=selected_difficulty)

    user_plan_ids = []
    if request.user.is_authenticated:
        user_plan_ids = list(
            Enrollment.objects.filter(user=request.user, is_active=True)
            .values_list('plan_id', flat=True)
        )

    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': selected_category,
        'selected_difficulty': selected_difficulty,
        'user_plan_ids': user_plan_ids,
    }
    return render(request, 'courses/catalog.html', context)
