from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def searchBooks(books, request):
    search_query_value = ''
    search_query = request.GET.get('q')
    if search_query is not None:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        search_query_value=search_query
    
    return books, search_query_value


def paginationBooks(books, request, each_page_items_count):
    p = Paginator(books, each_page_items_count)
    page_from_get = request.GET.get('page')
    try:
        page = p.page(page_from_get)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    
    pages_count = range(1, p.num_pages+1)
    return page, pages_count
