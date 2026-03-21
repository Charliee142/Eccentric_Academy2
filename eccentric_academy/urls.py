from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.core.urls')),
    path('courses/', include('apps.courses.urls')),
    path('payments/', include('apps.payments.urls')),
    path('contact/', include('apps.contact.urls')),
    path('dashboard/', include('apps.accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'
