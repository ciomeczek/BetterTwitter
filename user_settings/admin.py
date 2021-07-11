from django.contrib import admin
from .models import UserSettings, VisibilityStatus


admin.site.register(UserSettings)
admin.site.register(VisibilityStatus)
