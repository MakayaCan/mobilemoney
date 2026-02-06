from django.urls import path
from .views import dashboard, create_advert

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("adverts/new/", create_advert, name="create_advert"),
]
