from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("adverts.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/payments/", include("payments.urls")),
]
