from django.contrib import admin

from .models import Topic, Subtopic, Publication, PublicationComment, SubtopicComment, Competition, CompetitionSingle, CompetitionComment
from mptt.admin import MPTTModelAdmin

admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Publication)
admin.site.register(Competition)
admin.site.register(CompetitionSingle)
admin.site.register(PublicationComment, MPTTModelAdmin)
admin.site.register(SubtopicComment, MPTTModelAdmin)
admin.site.register(CompetitionComment, MPTTModelAdmin)

