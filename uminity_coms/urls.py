"""Визначає URL patterns для uminity_coms."""

from django.urls import path

from . import views

app_name = "uminity_coms"  # pylint: disable=invalid-name

urlpatterns = [
    # Головна сторінка.
    path("", views.index, name="index"),
    # Сторінка, що відображає всі теми.
    path("topics/", views.topics, name="topics"),
    # Сторінка, що відображає всі підтеми вибраної теми.
    path("topics/<int:topic_id>/", views.subtopics, name="subtopics"),
    # Сторінка, що відображає всі записи до вибраної підтеми.
    path("topic/<int:subtopic_id>/", views.subtopic, name="subtopic"),
    # Сторінка для додавання нової теми.
    path("new_topic/", views.new_topic, name="new_topic"),
    # Сторінка для додавання нової Підтеми.
    path("new_subtopic/<int:topic_id>/", views.new_subtopic, name="new_subtopic"),
    # Сторінка, що відображає всі книги.
    path("books/", views.books, name="books"),
    # Сторінка, що відображає всі твори на розгляд.
    path("publications/", views.publications, name="publications"),
    # Сторінка для публікації твору на розгляд.
    path("publication/<int:publication_id>/", views.publication, name="publication"),
    # Сторінка для додавання нового твору на розгляд.
    path("new_publication/", views.new_publication, name="new_publication"),
    # Сторінка, що відображає всі конкурси.
    path("competitions/", views.competitions, name="competitions"),
    # Сторінка, що відображає всі конкурсні роботи вибраного конкурсу.
    path("competitions/<slug:competition_slug>/", views.stories, name="competitions"),
    # Сторінка, що відображає окрему конкурсну роботу.
    path("competition/<slug:competition_slug>/<slug:post>/", views.post, name="post"),
    # Сторінка профілю.
    path("my_account/", views.my_account, name="my_account"),
]
