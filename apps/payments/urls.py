from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<slug:plan_slug>/', views.initiate_payment, name='checkout'),
    path('verify/<str:reference>/', views.verify_payment, name='verify'),
    path('history/', views.payment_history, name='history'),
]
