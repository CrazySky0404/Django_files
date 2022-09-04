from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """Тема, яку вивчає користувач."""
    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text
        #return f'{[self.text, self.description]!r}'


class Subtopic(models.Model):
    """Підтема до теми, яку вивчає користувач."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'subtopics'
        ordering = ['-date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


class Entry(models.Model):
    """Конкретна інформація до підтеми."""
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


class Publication(models.Model):
    """Публікація власного твору користувача."""
    text = models.CharField(max_length=300)
    description = models.TextField(max_length=10000, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text
