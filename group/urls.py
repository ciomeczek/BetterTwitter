from django.urls import path
from .views import *


urlpatterns = [
    path('create-group/', CreateGroup.as_view()),
    path('add-group-image/<int:group_pk>/', AddGroupImage.as_view()),
    path('get-group-posts/<int:group_pk>/', GetGroupPosts.as_view()),
    path('delete-group/<int:group_pk>/', DeleteGroup.as_view()),
    path('get-group-details/<int:group_pk>/', GetGroupDetails.as_view()),
    path('search-group/', SearchGroup.as_view()),
    path('wait-list/add-self/<int:group_pk>/', AddSelfToWaitList.as_view()),
    path('wait-list/remove/<int:group_pk>/', RemoveMemberFromWaitList.as_view()),
    path('wait-list/cancel-self/<int:group_pk>/', CancelSelfFromWaitList.as_view()),
    path('wait-list/accept/<int:group_pk>/', AcceptMemberFromWaitList.as_view()),
    path('ban-user/<int:group_pk>/', BanMember.as_view()),
    path('unban-user/<int:group_pk>/', UnBanMember.as_view()),
]
