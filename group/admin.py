from django.contrib import admin
from .models import Group, GroupWaitList, GroupBanList


admin.site.register(Group)
admin.site.register(GroupWaitList)
admin.site.register(GroupBanList)
