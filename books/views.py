from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from books.utils import paginationBooks, searchBooks
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Book_Review, Author, Author_Book
from .forms import Book_ReviewForm, BookForm




class BooksListView(View):
    def get(self, request):
        books = Book.objects.all()
        books, search_query_value = searchBooks(books, request)
        page, pages_count = paginationBooks(books, request, 3)

        context = {
            'search_query_value': search_query_value,
            'page': page,
            'pages':pages_count,
        }
        return render(request, 'books/books_list.html', context)


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        authors_books = book.author_book_set.all()
        authors = []
        for author in authors_books:
            authors.append(author.author)
        
        review_form = Book_ReviewForm()
        context = {
            'book': book, 
            'review_form': review_form,
            'authors':authors
        }
        return render(request, 'books/book_detail.html', context)
    
    def post(self, request, id):
        review_form = Book_ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.book = Book.objects.get(id=id)
            review.save()
            messages.success(request, "Your Review successfully saved!")
            return redirect('books:book-detail', id=id)

        context = {'review_form': review_form}
        return render(request, 'books/book_detail.html', context)



class BookAddView(LoginRequiredMixin, View):
    def get(self, request):
        page = 'add-book'
        book_add_form = BookForm()
        context = {'form': book_add_form, 'page': page}
        return render(request, 'books/book_form.html', context)
    

    def post(self, request):
        book_add_form = BookForm(request.POST, files=request.FILES)

        if book_add_form.is_valid():
            book = book_add_form.save()
            Author_Book.objects.create(
                author=request.user.author,
                book=book
            )
            messages.success(request, "Successfully added your new book detail.")
            return redirect('books:books-list')
        else:
            messages.error(request, "Invalid form input!")
            context = {'form': book_add_form}
            return render(request, 'books/book_form.html', context)



class BookUpdateView(View):
    def get(self, request, id):

        page = 'edit-book'
        book = Book.objects.get(id=id)
        book_add_form = BookForm(instance=book)
        context = {'form': book_add_form, 'page':page, 'book':book}
        return render(request, 'books/book_form.html', context)

    def post(self, request, id):
        book = Book.objects.get(id=id)
        book_edit_form = BookForm(instance=book, data=request.POST, files=request.FILES)
        if book_edit_form.is_valid():
            book_edit_form.save()
            messages.success(request, "Successfully edited book.")
            return redirect('books:book-detail', id=id)
        else:
            context = {'form': book_edit_form}
            return render(request, 'books/book_form.html', context)



class BookDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        try:
            delete = request.GET.get('delete')
            if delete=='yes':
                book.delete()
                messages.info(request, 'Successfully deleted Book')
                return redirect('users:user-profile', username=request.user.username)
        except:
            pass

        context = {'book':book}
        return render(request, 'books/book_delete.html', context)



class BookReviewEditView(View):
    def get(self, request, id):
        review = Book_Review.objects.get(id=id)
        review_form = Book_ReviewForm(instance=review)

        context = {'review_form': review_form}
        return render(request, 'books/book_review_edit.html', context)
    
    def post(self, request, id):
        review = Book_Review.objects.get(id=id)
        review_form = Book_ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Successfully updated your Review!')
            return redirect('books:book-detail', id=review.book.id)
        messages.error(request, 'Something went wrong! Please fill valid data!')
        context = {'review_form', review_form}
        return render(request, 'books/book_review_edit.html', context)


class DeleteReviewView(View):
    def get(self, request, id):
        review = Book_Review.objects.get(id=id)
        try:
            sure = request.GET.get('delete')
            if sure == 'yes':
                review.delete()
                messages.success(request, 'Successfully deleted your Review!')
                return redirect('books:book-detail', id=review.book.id)
        except:
            pass
        context = {'obj': review}
        return render(request, 'books/delete_review.html', context)


class AuthorsListPageView(View):
    def get(self, request):
        authors = Author.objects.all()
        context = {'authors': authors}
        return render(request, 'books/authors.html', context)
    