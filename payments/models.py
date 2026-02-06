from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MobileMoneyPayment(models.Model):
    approval_code = models.CharField(max_length=64, unique=True)
    wallet = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5)
    raw_message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)


class Subscription(models.Model):
    PLAN_CHOICES = [
        ("ACCESS", "Monthly Access"),
        ("ADVERT_DAY", "1 Day Advert"),
        ("ADVERT_WEEK", "1 Week Advert"),
        ("ADVERT_BIWEEK", "2 Week Advert"),
        ("ADVERT_MONTH", "1 Month Advert"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_active(self):
        return self.active and self.expires_at > timezone.now()
from django.db import models

# Create your models here.
