import json
from decimal import Decimal
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import MobileMoneyPayment, Subscription
from .utils import SUBSCRIPTION_PRICING
from .models import PaymentIntent
from .utils import SUBSCRIPTION_PRICING

def access_locked(request):
    if not request.user.is_authenticated:
        return redirect("login")

    pricing = SUBSCRIPTION_PRICING["ACCESS"]

    intent, created = PaymentIntent.objects.get_or_create(
        user=request.user,
        purpose="ACCESS",
        used=False,
        defaults={
            "amount": pricing["amount"],
            "reference": PaymentIntent.generate_reference(),
        },
    )

    return render(request, "access_locked.html", {
        "reference": intent.reference,
        "amount": intent.amount,
    })



API_KEY = settings.ANDROID_SMS_API_KEY


@csrf_exempt
def confirm_payment(request):
    if request.headers.get("X-API-KEY") != API_KEY:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body.decode())

    approval = data["approval_code"]
    amount = Decimal(data["amount"])
    reference = data.get("reference")

    if MobileMoneyPayment.objects.filter(approval_code=approval).exists():
        return JsonResponse({"status": "DUPLICATE"})

    try:
        intent = PaymentIntent.objects.get(
            reference=reference,
            used=False,
            amount=amount,
        )
    except PaymentIntent.DoesNotExist:
        return JsonResponse({"status": "NO_MATCHING_INTENT"})

    config = SUBSCRIPTION_PRICING["ACCESS"]

    Subscription.objects.create(
        user=intent.user,
        plan="ACCESS",
        expires_at=timezone.now() + timedelta(days=config["days"]),
    )

    MobileMoneyPayment.objects.create(
        approval_code=approval,
        wallet=data["wallet"],
        amount=amount,
        currency=data["currency"],
        raw_message=data["raw_message"],
        user=intent.user,
    )

    intent.used = True
    intent.save()

    return JsonResponse({
        "status": "SUCCESS",
        "user": intent.user.username,
        "access": "GRANTED",
    })
