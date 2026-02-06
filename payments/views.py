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


def access_locked(request):
    return render(request, "access_locked.html")


API_KEY = settings.ANDROID_SMS_API_KEY


@csrf_exempt
def confirm_payment(request):
    if request.headers.get("X-API-KEY") != API_KEY:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    data = json.loads(request.body.decode())
    approval = data["approval_code"]
    amount = Decimal(data["amount"])

    if MobileMoneyPayment.objects.filter(approval_code=approval).exists():
        return JsonResponse({"status": "DUPLICATE"})

    matched_plan = None
    for plan, config in SUBSCRIPTION_PRICING.items():
        if config["amount"] == amount:
            matched_plan = plan
            break

    if not matched_plan:
        return JsonResponse({"status": "INVALID_AMOUNT"})

    payment = MobileMoneyPayment.objects.create(
        approval_code=approval,
        wallet=data["wallet"],
        amount=amount,
        currency=data["currency"],
        raw_message=data["raw_message"],
    )

    user = User.objects.order_by("-date_joined").first()

    if user:
        config = SUBSCRIPTION_PRICING[matched_plan]

        Subscription.objects.create(
            user=user,
            plan=matched_plan,
            expires_at=timezone.now() + timedelta(days=config["days"]),
        )

        payment.user = user
        payment.save()

    return JsonResponse({"status": "SUCCESS", "plan": matched_plan})
