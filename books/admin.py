from django.contrib import admin
from books.models import Book, Author, Book_Review, Author_Book


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title','description')



admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Author_Book)
admin.site.register(Book_Review)
