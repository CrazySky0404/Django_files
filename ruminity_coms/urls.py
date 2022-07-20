"""Визначає URL patterns для ruminity_coms."""

from django.urls import path

from . import views

app_name = 'ruminity_coms'
urlpatterns = [
    # Головна сторінка.
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми.
    path('topics/', views.topics, name='topics'),
    # Сторінка, що відображає всі підтеми вибраної теми.
    path('topics/<int:topic_id>/', views.subtopics, name='subtopics'),
    # Сторінка, що відображає всі записи до вибраної підтеми.
    path('topic/<int:subtopic_id>/', views.subtopic, name='subtopic'),
]