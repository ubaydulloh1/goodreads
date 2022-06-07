from django.urls import path
from . import views


app_name='api'

urlpatterns = [
    path('', views.getRoutes, name='get-routes'),
    path('books/', views.getBooksList, name='get-books-list'),

    path('books/<int:id>/', views.getBookDetail, name='get-book-detail'),
    path('reviews/', views.getBookReviews, name='get-reviews-list'),
    path('reviews/<int:id>/', views.getReviewDetail, name='get-review-detail'),
]
