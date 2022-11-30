from django.contrib import admin

from .models import Topic, Subtopic, Entry, Publication, Comment
from mptt.admin import MPTTModelAdmin

admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Entry)
admin.site.register(Publication)
admin.site.register(Comment, MPTTModelAdmin)

