from django.db import models
from django.contrib.auth import get_user_model
from comment.models import Comment


class CommentReaction(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
