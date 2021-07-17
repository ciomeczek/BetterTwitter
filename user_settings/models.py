from django.db import models
from django.contrib.auth import get_user_model


class VisibilityStatus(models.Model):
    status_name = models.CharField(max_length=55)

    def __str__(self):
        return self.status_name

    @classmethod
    def get_public(cls):
        instance, created = cls.objects.get_or_create(status_name='Public')
        return instance

    @classmethod
    def get_private(cls):
        instance, created = cls.objects.get_or_create(status_name='Private')
        return instance

    @classmethod
    def get_secret(cls):
        instance, created = cls.objects.get_or_create(status_name='Secret')
        return instance


class UserSettings(models.Model):
    account_status = models.ForeignKey(
        VisibilityStatus, on_delete=models.CASCADE)
    can_get_invites = models.BooleanField(
        default=True, blank=False, null=False)

    def __str__(self):
        return f'Settings of {get_user_model().objects.get(settings=self).username}'

    def set_account_status(self, account_status):
        if account_status == 1:
            self.account_status = VisibilityStatus.get_public()
            self.save()
            return True

        if account_status == 2:
            self.account_status = VisibilityStatus.get_private()
            self.save()
            return True

        if account_status == 3:
            self.account_status = VisibilityStatus.get_secret()
            self.save()
            return True
