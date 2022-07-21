"""Визначає регулярні вирази URL."""

from django.urls import path, include

app_name = 'users'
urlpatterns = [
    # Додати уставні URL auth (автентифікації).
    path('', include('django.contrib.auth.urls')),
]