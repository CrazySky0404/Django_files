"""
This module contains the Django admin configuration for the UMINITY models.

It includes the admin classes for Topic, Subtopic, Publication, and other related models.
"""

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    Topic,
    Subtopic,
    Publication,
    PublicationComment,
    SubtopicComment,
    Competition,
    CompetitionSingle,
    CompetitionComment,
    Books,
)


admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Publication)
admin.site.register(Books)
admin.site.register(Competition)
admin.site.register(CompetitionSingle)
admin.site.register(PublicationComment, MPTTModelAdmin)
admin.site.register(SubtopicComment, MPTTModelAdmin)
admin.site.register(CompetitionComment, MPTTModelAdmin)
