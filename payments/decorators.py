from django.shortcuts import redirect
from django.utils import timezone
from .models import Subscription


def subscription_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        active = Subscription.objects.filter(
            user=request.user,
            active=True,
            expires_at__gt=timezone.now()
        ).exists()

        if not active:
            return redirect("access_locked")

        return view_func(request, *args, **kwargs)
    return wrapper
