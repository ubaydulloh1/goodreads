from django.test import TestCase
from books.models import Book, Book_Review, Author_Book, Author
from django.urls import reverse
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_books_list(self):
        Book.objects.create(title='Book1', description='description1')
        Book.objects.create(title='Book2', description='description2')
        Book.objects.create(title='Book3', description='description3')
        Book.objects.create(title='Book4', description='description4')
        Book.objects.create(title='Boo5', description='description5')

        response = self.client.get(reverse("books:books-list")+"?page=1")
        self.assertContains(response, 'Book3')
        self.assertNotContains(response, 'Book4')
        response = self.client.get(reverse("books:books-list")+"?page=2")
        self.assertContains(response, 'Book4')
        self.assertNotContains(response, 'Book1')

        # search with pagination
        response = self.client.get(reverse("books:books-list")+"?q=book&page=2")
        self.assertContains(response, 'Book4')
        self.assertNotContains(response, 'description5')


    def test_no_books(self):
        response = self.client.get(reverse('books:books-list'))
        books_count = Book.objects.count()

        self.assertEqual(books_count, 0)
        self.assertContains(response, 'No Books Found!')
    

    def test_book_detail(self):
        Book.objects.create(title='Book1', description='description1')
        # Author.objects.create(first_name='author1', last_name='authorov', bio='some bio', email='email@gmail.com')
        user = CustomUser.objects.create(first_name='author1', last_name='authorov', username='author1', email='email@gmail.com')
        user.set_password('some_password')
        user.save()

        author1 = Author.objects.get(user__first_name='author1')
        book1 = Book.objects.get(title='Book1')
        Author_Book.objects.create(author=author1, book=book1)
        
        books_count = Book.objects.count()
        self.assertEqual(books_count, 1)
        self.assertEqual(book1.author_book_set.count(), 1)
        author_name = book1.author_book_set.get(book=book1)
        self.assertEqual(author_name.author.user.first_name, 'author1')

        response = self.client.get(reverse('books:book-detail', kwargs={'id': book1.id}))
        self.assertContains(response, 'Book1')
        self.assertContains(response, 'description1')


    def test_books_search(self):
        Book.objects.create(title='Book1', description='description1')
        Book.objects.create(title='Book2', description='description2')
        Book.objects.create(title='Boo', description='description3')

        response = self.client.get(reverse('books:books-list')+'?q=Book')
        self.assertContains(response, 'description1')
        self.assertContains(response, 'description2')
        self.assertNotContains(response, 'description3')


class BookReviewTestCase(TestCase):
    def test_book_reviews(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'ubaydulloh', 
                'first_name': 'Ubaydulloh',
                'last_name': 'Qochqarov',
                'email': 'email@gmail.com',
                'password': 'somepassword',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.client.login(username='ubaydulloh', password='somepassword')
        # user = self.client.get_user()
        response = self.client.get(reverse('users:user-profile', kwargs={'username': 'ubaydulloh'}))
        self.assertEqual(response.status_code, 200)
        book = Book.objects.create(title='Elon Musk', description='most money owner!')
        
        self.client.post(
            reverse("books:book-detail", kwargs={'id': book.id}),
            data={
                'body':'This is test comment!',
                'stars_given': 3,
            }
        )
        review = Book_Review.objects.get(body__icontains='this is test comment')
        self.assertEqual(Book_Review.objects.count(), 1)
        self.assertEqual(review.body, 'This is test comment!')


    def test_invalid_reviews_post(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'ubaydulloh', 
                'first_name': 'Ubaydulloh',
                'last_name': 'Qochqarov',
                'email': 'email@gmail.com',
                'password': 'somepassword',
            }
        )
        self.client.login(username='ubaydulloh', password='somepassword')
        book = Book.objects.create(title='Elon Musk', description='most money owner!')
        
        self.client.post(
            reverse("books:book-detail", kwargs={'id': book.id}),
            data={
                'body':'This is test comment!',
                'stars_given': 6,
            }
        )
        self.assertEqual(Book_Review.objects.count(), 0)
        # self.assertEqual(review.body, 'This is test comment!')

    def test_review_updated_successfully(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'email': 'email@gmail.com',
                'password': 'somepassword',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='somepassword')

        Book.objects.create(
            title='New Book for Review Update',
            description='Description for Book', 
        )

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get(title__icontains="New")
        self.assertEqual(book.title, 'New Book for Review Update')
        response = self.client.post(
            reverse('books:book-detail', kwargs={'id':book.id}),
            data={
                'stars_given': 5,
                'body': 'Hello world!',
            }
        )
        self.assertEqual(response.status_code, 302)
        review = Book_Review.objects.get(body__icontains='hello world')
        self.assertEqual(review.stars_given, 5)

        self.client.post(
            reverse('books:book-review-edit', kwargs={'id':review.id}),
            data={
                'stars_given': 4,
                'body': 'Hello world!(Updated!)',
            }
        )
        review.refresh_from_db()
        self.assertEqual(review.stars_given, 4)
        self.assertEqual(review.body, 'Hello world!(Updated!)')

        # delete review test
        response = self.client.get(reverse('books:book-review-delete', kwargs={'id': review.id}) + '?delete=yes')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book_Review.objects.count(), 0)
