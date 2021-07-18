from django.db import models
from django.contrib.auth import get_user_model
from group_wait_list.models import GroupWaitList
from group_ban_list.models import GroupBanList


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="groups/", default="groups/default.png")
    admins = models.ManyToManyField(get_user_model(), related_name="admin_in_groups")
    members = models.ManyToManyField(get_user_model(), related_name="user_groups")
    wait_list = models.OneToOneField(GroupWaitList, on_delete=models.CASCADE, related_name="group", null=True)
    ban_list = models.OneToOneField(GroupBanList, on_delete=models.CASCADE, related_name="group", null=True)

    def __str__(self):
        return self.name

    def add_user(self, user):
        if user in self.members.all():
            return

        self.members.add(user)

    def is_user_group_admin(self, user):
        return user in self.admins.all()

    def is_user_group_member(self, user):
        return user in self.members.all()
