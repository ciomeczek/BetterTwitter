from django.urls import path
from .views import GetUser, GetUserByID, CreateUser, GetUserByName, Authenticate, AddProfilePicture


urlpatterns = [
    path('current-user/', GetUser.as_view()),
    path('<int:pk>/', GetUserByID.as_view()),
    path('create/', CreateUser.as_view()),
    path('by-name/', GetUserByName.as_view()),
    path('authenticate/', Authenticate.as_view()),
    path('add-pfp/', AddProfilePicture.as_view()),
]
