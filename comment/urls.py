from django.urls import path
from .views import CreateComment
from comment_reaction.views import Reactions


urlpatterns = [
    path('create-comment/<int:post_pk>/', CreateComment.as_view()),
    path('reactions/<int:pk>/', Reactions.as_view()),
]
