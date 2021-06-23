from django.urls import path
from .views import SetSettings


urlpatterns = [
    path('set-settings/', SetSettings.as_view())
]
