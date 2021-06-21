from django.db import models
from django.contrib.auth import get_user_model
from post.models import Post


class PostReaction(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
