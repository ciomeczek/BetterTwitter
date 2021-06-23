from django.urls import path
from .views import InviteFriend, AcceptFriend, RejectFriend, CancelRequest, RemoveFriend


urlpatterns = [
    path('invite/', InviteFriend.as_view()),
    path('accept/', AcceptFriend.as_view()),
    path('reject/', RejectFriend.as_view()),
    path('cancel/', CancelRequest.as_view()),
    path('remove/', RemoveFriend.as_view()),
]
