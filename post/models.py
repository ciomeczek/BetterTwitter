from django.db import models
from django.contrib.auth import get_user_model
from user_settings.models import VisibilityStatus
from group.models import Group


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, blank=True, null=True)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'Post of {self.author}'

    @staticmethod
    def can_see_post(request_user, user):
        if request_user == user:
            return True

        if user.settings.account_status != VisibilityStatus.get_public():
            if not request_user.is_authenticated:
                return False

            if request_user not in user.friend_list.friends.all():
                return False
        return True

    def can_see_post_with_group(self, request_user, user):
        if self.group is not None:
            return request_user in self.group.members.all()

        if request_user == user:
            return True

        if user.settings.account_status != VisibilityStatus.get_public():
            if not request_user.is_authenticated:
                return False

            if request_user not in user.friend_list.friends.all():
                return False
        return True

    def is_private(self):
        return self.author.settings.account_status != VisibilityStatus.get_public()


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')

    def __str__(self):
        return self.image
