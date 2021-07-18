from django.db import models
from django.contrib.auth import get_user_model


class GroupWaitList(models.Model):
    members = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return f"Wait list of {self.group}"

    def add_user(self, user):
        if user in self.group.members.all():
            return

        self.members.add(user)

    def remove_user(self, user):
        self.members.remove(user)

    def accept(self, user):
        if user not in self.members.all():
            return

        self.remove_user(user)
        self.group.add_user(user)
