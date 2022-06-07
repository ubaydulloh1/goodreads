from django.urls import path
from books.views import (
    AuthorsListPageView, 
    BooksListView, 
    BookDetailView, 
    BookAddView,
    BookUpdateView,
    BookReviewEditView, 
    DeleteReviewView,
    BookDeleteView
)


app_name = 'books'
urlpatterns = [
    path('authors/', AuthorsListPageView.as_view(), name='authors'),

    path('', BooksListView.as_view(), name='books-list'),
    path('<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('add-book/', BookAddView.as_view(), name='add-book'),
    path('<int:id>/edit/', BookUpdateView.as_view(), name='edit-book'),
    path('<int:id>/delete/', BookDeleteView.as_view(), name='delete-book'),
    
    path('reviews/<int:id>/edit/', BookReviewEditView.as_view(), name='book-review-edit'),
    path('reviews/<int:id>/delete/', DeleteReviewView.as_view(), name='book-review-delete'),

]