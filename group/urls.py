from django.urls import path
from .views import *


urlpatterns = [
    path('create-group/', CreateGroup.as_view()),
    path('delete-group/<int:group_pk>/', DeleteGroup.as_view()),
    path('get-my-groups/', GetMyGroups.as_view()),
    path('add-group-image/<int:group_pk>/', AddGroupImage.as_view()),
    path('get-group/<int:group_pk>/', GetGroupNoDetails.as_view()),
    path('get-group-posts/<int:group_pk>/', GetGroupPosts.as_view()),
    path('get-group-details/<int:group_pk>/', GetGroupDetails.as_view()),
    path('search-group/', SearchGroup.as_view()),
]
