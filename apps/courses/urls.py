from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_catalog, name='catalog'),
    path('pricing/', views.pricing, name='pricing'),
    path('plans/<slug:slug>/', views.plan_detail, name='plan_detail'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
]
