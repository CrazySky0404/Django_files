"""Визначає URL patterns для ruminity_coms."""

from django.urls import path

from . import views

app_name = 'ruminity_coms'
urlpatterns = [
    # Головна сторінка.
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми.
    path('topics/', views.topics, name='topics'),
]