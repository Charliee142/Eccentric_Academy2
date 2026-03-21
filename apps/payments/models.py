from django.db import models
from django.contrib.auth.models import User
from apps.courses.models import Plan
import uuid


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='enrollments')
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'plan']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.email} → {self.plan.name}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='payments')
    enrollment = models.OneToOneField(Enrollment, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')

    # Payment details
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount in Naira")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Paystack response data
    paystack_id = models.CharField(max_length=100, blank=True)
    paystack_reference = models.CharField(max_length=100, blank=True)
    gateway_response = models.CharField(max_length=200, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    channel = models.CharField(max_length=50, blank=True, help_text="card, bank, ussd, etc.")
    currency = models.CharField(max_length=10, default='NGN')

    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.reference} - {self.user.email} ({self.status})"

    @classmethod
    def generate_reference(cls, user_id):
        """Generate a unique payment reference."""
        import time
        return f"EA-{user_id}-{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"

    @property
    def amount_formatted(self):
        return f"₦{self.amount:,.0f}"
