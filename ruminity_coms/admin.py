from django.contrib import admin

from .models import Topic, Subtopic, Entry, Publication

admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Entry)
admin.site.register(Publication)

