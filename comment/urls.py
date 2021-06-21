from django.urls import path
from .views import CreateComment
from comment_reaction.views import AddReact, DeleteReact


urlpatterns = [
    path('create-comment/<int:post_pk>/', CreateComment.as_view()),
    path('add-reaction/', AddReact.as_view()),
    path('delete-reaction/', DeleteReact.as_view()),
]
