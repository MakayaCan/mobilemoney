from django.urls import path
from .views import confirm_payment, access_locked

urlpatterns = [
    path("access-locked/", access_locked, name="access_locked"),
    path("api/mobile-money/confirm/", confirm_payment),
]
