from rest_framework import serializers
from books.models import Book, Book_Review
from users.models import CustomUser

class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'cover_img', 'isbn', 'created')


class BookReviewSerializer(serializers.ModelSerializer):
    user = CustomUserModelSerializer(read_only=True)
    book = BookModelSerializer(read_only=True)

    book_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Book_Review
        fields = ('id', 'body', 'user','stars_given', 'book', 'created', 'user_id', 'book_id')