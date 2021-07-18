from django.db import models
from django.contrib.auth import get_user_model


class GroupBanList(models.Model):
    members = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return f"Ban list of {self.group}"

    def remove_user(self, user):
        self.members.remove(user)

    def add_user(self, user):
        self.members.add(user)
