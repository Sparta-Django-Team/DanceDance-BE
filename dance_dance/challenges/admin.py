from django.contrib import admin

from dance_dance.challenges.models import (
    OriginalVideo,
    OriginalVideoLikesLog,
    OriginalVideoTag,
    PlatformType,
    Tag,
    UserVideo,
    UserVideoLikesLog,
    UserVideoTag,
)

admin.site.register(OriginalVideo)
admin.site.register(UserVideo)
admin.site.register(PlatformType)
admin.site.register(Tag)
admin.site.register(OriginalVideoLikesLog)
admin.site.register(UserVideoLikesLog)
admin.site.register(OriginalVideoTag)
admin.site.register(UserVideoTag)
