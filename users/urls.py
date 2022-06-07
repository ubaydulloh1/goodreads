from django.urls import path
from users.views import (
    index, 
    homePage, 
    RegisterView, 
    LoginView, 
    UserProfilePageView, 
    LogoutView, 
    UserProfileEditView,
    AuthorBooksPageView
    )


app_name = 'users'

urlpatterns = [
    path('', index, name='landing-page'),
    path('home/', homePage, name='home'),

    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),

    path('<str:username>/profile/', UserProfilePageView.as_view(), name='user-profile'),
    path('<str:username>/books/', AuthorBooksPageView.as_view(), name='author-books'),

    path('users/profile/edit/', UserProfileEditView.as_view(), name='profile-edit'),
]