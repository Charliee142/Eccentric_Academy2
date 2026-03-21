from django.contrib import admin
from .models import Payment, Enrollment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'plan', 'amount_formatted', 'status', 'channel', 'created_at']
    list_filter = ['status', 'plan', 'channel', 'currency']
    search_fields = ['reference', 'user__email', 'user__first_name', 'user__last_name', 'paystack_reference']
    readonly_fields = ['id', 'reference', 'user', 'plan', 'amount', 'status', 'paystack_id',
                       'paystack_reference', 'gateway_response', 'paid_at', 'channel',
                       'currency', 'raw_response', 'ip_address', 'user_agent', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def amount_formatted(self, obj):
        return obj.amount_formatted
    amount_formatted.short_description = 'Amount'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'is_active', 'enrolled_at']
    list_filter = ['status', 'is_active', 'plan']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering = ['-enrolled_at']
