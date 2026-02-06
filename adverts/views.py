from django.shortcuts import render, redirect
from .models import Advert
from payments.decorators import subscription_required


@subscription_required
def dashboard(request):
    adverts = Advert.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"adverts": adverts})


@subscription_required
def create_advert(request):
    if request.method == "POST":
        Advert.objects.create(
            user=request.user,
            title=request.POST["title"],
            description=request.POST["description"],
            price=request.POST["price"],
        )
        return redirect("dashboard")

    return render(request, "advert_create.html")
