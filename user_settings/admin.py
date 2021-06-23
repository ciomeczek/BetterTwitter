from django.contrib import admin
from .models import UserSettings, AccountStatus


admin.site.register(UserSettings)
admin.site.register(AccountStatus)
