from django.shortcuts import redirect
from django.utils import timezone
from .models import Subscription


def subscription_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        sub = Subscription.objects.filter(
            user=request.user,
            plan="ACCESS",
            active=True,
            expires_at__gt=timezone.now(),
        ).first()

        if not sub:
            return redirect("access_locked")

        return view_func(request, *args, **kwargs)

    return wrapper
