from django.urls import path
from .views import *


urlpatterns = [
    path('get-wait-list/<int:group_pk>/', GetGroupWaitList.as_view()),
    path('add-self/<int:group_pk>/', AddSelfToWaitList.as_view()),
    path('cancel-self/<int:group_pk>/', CancelSelfFromWaitList.as_view()),
    path('accept/<int:group_pk>/', AcceptUserFromWaitList.as_view()),
    path('remove/<int:group_pk>/', RemoveUserFromWaitList.as_view()),
]
