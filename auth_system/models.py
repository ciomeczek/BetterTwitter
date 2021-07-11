from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_manager import UserManager
from user_settings.models import UserSettings


class CustomUser(AbstractUser):
    pfp = models.ImageField(upload_to="users/", default="users/default.png")
    settings = models.OneToOneField(UserSettings, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'email']

    objects = UserManager()

    def __unicode__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
