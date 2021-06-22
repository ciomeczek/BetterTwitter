from django.urls import path
from .views import CreatePost, SeePostsOfUser, SeePostsOfUserByID, SeePostDetailsByID, HomePage
from post_reaction.views import Reactions


urlpatterns = [
    path('create-post/', CreatePost.as_view()),
    path('see-your-posts/', SeePostsOfUser.as_view()),
    path('see-posts-of-user/<int:pk>/', SeePostsOfUserByID.as_view()),
    path('see-post-details/<int:post_pk>/', SeePostDetailsByID.as_view()),
    path('reactions/<int:pk>/', Reactions.as_view()),
    path('home-page/', HomePage.as_view()),
]
