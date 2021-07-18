from django.urls import path
from .views import GetBanList, BanMember, UnBanMember


urlpatterns = [
    path('get-ban-list/<int:group_pk>/', GetBanList.as_view()),
    path('ban-user/<int:group_pk>/', BanMember.as_view()),
    path('unban-user/<int:group_pk>/', UnBanMember.as_view()),
]
