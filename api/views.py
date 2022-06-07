from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .serializers import (
        BookModelSerializer, 
        BookReviewSerializer
)
from books.models import Book, Book_Review



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    result = [
            {'GET': 'api/books/'},
            {'GET': 'api/books/<int:id>/'},
            {'GET': 'api/reviews/'},
            {'POST': 'api/reviews/'},
            {'GET': 'api/reviews/<int:id>/'},
            {'PUT': 'api/reviews/<int:id>/'},
            {'DELETE': 'api/reviews/<int:id>/'},
    ]
    return Response(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getBooksList(request):
        books = Book.objects.all()
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(books, request)
        serializer = BookModelSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBookDetail(request, id):
        try:
                book = Book.objects.get(id=id)
                serializer = BookModelSerializer(book, many=False)
        except:
                serializer = 'No Book!'
                return Response(serializer)
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def getBookReviews(request):
        if request.method == "GET":
                reviews = Book_Review.objects.all()
                paginator = PageNumberPagination()
                page_obj = paginator.paginate_queryset(reviews, request)
                serializer = BookReviewSerializer(page_obj, many=True)
                return paginator.get_paginated_response(serializer.data)

        if request.method == "POST":
                serializer = BookReviewSerializer(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def getReviewDetail(request, id):
        if request.method == "GET":
                try:
                        review = Book_Review.objects.get(id=id)
                        result = BookReviewSerializer(review, many=False)
                        return Response(result.data)
                except:
                        return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == "DELETE":
                review = Book_Review.objects.get(id=id)
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        
        if request.method == "PUT":
                review = Book_Review.objects.get(id=id)
                review_update_serializer = BookReviewSerializer(instance=review, data=request.data, many=False, partial=True)

                if review_update_serializer.is_valid():
                        review_update_serializer.save()
                        return Response(data=review_update_serializer.data, status=status.HTTP_200_OK)
                return Response(data=review_update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
