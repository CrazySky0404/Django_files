from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Topic(models.Model):
    """Тема, яку вивчає користувач."""
    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


class Subtopic(models.Model):
    """Підтема до теми, яку вивчає користувач."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    description = models.TextField(max_length=1500, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'subtopics'
        ordering = ['-date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


# class Entry(models.Model):
#     """Конкретна інформація до підтеми."""
#     subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
#     text = models.CharField(max_length=300)
#     date_added = models.DateTimeField(auto_now_add=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'entries'
#         # ordering = ['-date_added']
#
#     def __str__(self):
#         """Повернути рядкове представлення моделі."""
#         return self.text


class Publication(models.Model):
    """Публікація власного твору користувача."""
    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


class PublicationComment(MPTTModel):
    """Комернтар до окремої публікації."""
    publication = models.ForeignKey(Publication,
                                    on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['publication']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.name


class SubtopicComment(MPTTModel):
    """Комернтар до окремої публікації."""
    subtopic = models.ForeignKey(Subtopic,
                                    on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.name


class Competition(models.Model):
    """Список конкурсів."""
    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


class CompetitionSingle(models.Model):
    """Окрема сторінка конкурсної роботи."""
    stories = models.ForeignKey(Competition, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    description = models.TextField(max_length=1500, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        #verbose_name_plural = 'subtopics'
        ordering = ['-date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text


class CompetitionComment(MPTTModel):
    """Коментар до окремої конкурсної роботи."""
    story = models.ForeignKey(CompetitionSingle,
                                    on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['date_added']

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.name