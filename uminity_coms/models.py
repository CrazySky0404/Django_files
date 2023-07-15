"""
This module contains the models for the application.
"""
from django.contrib.auth.models import User
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Topic(models.Model):
    """Тема, яку вивчає користувач."""

    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.text)

    def get_last_comment(self):
        """Get the latest comment datetime for all subtopics in this topic"""
        latest_comment_datetime = SubtopicComment.objects.filter(subtopic__topic=self).aggregate(
            max_date_added=Max("date_added")
        )["max_date_added"]

        # Get the latest comment
        if latest_comment_datetime:
            last_comment = SubtopicComment.objects.filter(
                date_added=latest_comment_datetime, subtopic__topic=self
            ).first()

            return {"comment": last_comment, "subtopic": last_comment.subtopic}
        return {"comment": None, "subtopic": None}

class Subtopic(models.Model):
    """Підтема до теми, яку вивчає користувач."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    description = models.TextField(max_length=1500, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    class Meta:
        """
        Metadata options for the Subtopic model.
        """

        verbose_name_plural = "subtopics"
        ordering = ["-date_added"]

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.text)

    def get_all_comments(self, num_comments):
        """Отримати num_comments останніх коментарів для цієї підтеми, відсортованих за датою створення."""
        comments = SubtopicComment.objects.filter(subtopic=self).order_by("-date_added")[:num_comments]
        return comments


class Books(models.Model):
    """Список книжок."""

    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.text)


class Publication(models.Model):
    """Публікація власного твору користувача."""

    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        """
        Metadata options for the Subtopic model.
        """

        ordering = ["-date_added"]

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.text)


class PublicationComment(MPTTModel):
    """Комернтар до окремої публікації."""

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        """
        Metadata options for the MPTT (Modified Preorder Tree Traversal) behavior of the model.
        """

        order_insertion_by = ["publication"]

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.name)


class SubtopicComment(MPTTModel):
    """Комернтар до окремої публікації."""

    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        """
        Metadata options for the MPTT (Modified Preorder Tree Traversal) behavior of the model.
        """

        order_insertion_by = ["date_added"]

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.name)


class Competition(models.Model):
    """Список конкурсів."""

    text = models.CharField(max_length=300)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique_for_date="date_added")
    objects = models.Manager()

    class Meta:
        """
        Metadata options for the Competition model.
        """

        db_table = "uminity_coms_competition"

    def get_absolute_url(self):
        """
        Returns the absolute URL for the Competition model instance.
        """
        return reverse("uminity_coms:competition", args=[self.slug])

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.text)


class CompetitionSingle(models.Model):
    """Окрема сторінка конкурсної роботи."""

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="single")
    text = models.CharField(max_length=300)
    description = models.TextField(max_length=1500, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique_for_date="date_added")
    publish = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        """
        Returns the absolute URL for the Post model instance.
        """
        return reverse("uminity_coms:post", args=[self.slug])
        # return reverse("uminity_coms:post", args=[self.competition.slug, self.slug])

    class Meta:
        """
        Metadata options for the CompetitionSingle model.
        """

        db_table = "uminity_coms_competitionsingle"
        ordering = ["-date_added"]

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.text)


class CompetitionComment(MPTTModel):
    """Коментар до окремої конкурсної роботи."""

    story = models.ForeignKey(CompetitionSingle, on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        """
        Metadata options for the MPTT (Modified Preorder Tree Traversal) behavior of the model.
        """

        order_insertion_by = ["date_added"]

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return str(self.name)

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "subtopic")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        unique_together = ("user", "subtopic")

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        unique_together = ("user", "subtopic")

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(SubtopicComment, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        unique_together = ("user", "comment")
