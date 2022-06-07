from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from users.models import CustomUser
from books.models import Book, Book_Review


class BookReviewApiTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='ubaydulloh', 
            first_name="Ubaydulloh",
            last_name='Qochqarov', 
            email='ubaydulloh@gmail.com',
        )
        self.user.set_password('somepassword')
        self.user.save()
        self.client.login(username='ubaydulloh', password='somepassword')

    def test_api_book_review_list(self):
        user_2 = CustomUser.objects.create(
            username='ubaydulloh2', 
            first_name="Ubaydulloh2",
            last_name='Qochqarov2', 
            email='ubaydulloh2@gmail.com',
        )
        book1 = Book.objects.create(
            title='Book of Api',
            description='This book is written about APIs!',
            isbn='35344326464',
        )
        b_r = Book_Review.objects.create(
            user=self.user,
            book=book1,
            stars_given=4,
            body=f'This Review is belongs to {book1.title}'
        )
        b_r2 = Book_Review.objects.create(
            user=user_2,
            book=book1,
            stars_given=5,
            body=f'This Review is second review from {user_2.username}'
        )

        response = self.client.get(reverse('api:get-reviews-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][1]['id'], b_r2.id)
        self.assertEqual(response.data['results'][0]['id'], b_r.id)
        self.assertEqual(response.data['results'][1]['stars_given'], 5)
        self.assertEqual(response.data['results'][0]['stars_given'], 4)
        self.assertEqual(response.data['results'][0]['body'], 'This Review is belongs to Book of Api')
        self.assertEqual(response.data['results'][1]['body'], 'This Review is second review from ubaydulloh2')
        self.assertEqual(response.data['results'][1]['user']['username'], 'ubaydulloh2')
        self.assertEqual(response.data['results'][1]['user']['first_name'], 'Ubaydulloh2')
        self.assertEqual(response.data['results'][1]['user']['last_name'], 'Qochqarov2')
        self.assertEqual(response.data['results'][1]['user']['email'], 'ubaydulloh2@gmail.com')
        self.assertEqual(response.data['results'][0]['book']['title'], 'Book of Api')
        self.assertEqual(response.data['results'][0]['book']['description'], 'This book is written about APIs!')
        self.assertEqual(response.data['results'][0]['book']['isbn'], '35344326464')


    def test_api_review_create(self):
        book = Book.objects.create(title='book1', description='book1 description')
        response = self.client.post(
            reverse("api:get-reviews-list"),
            data={
                "stars_given":5,
                "body":"Test Review",
                "user_id":self.user.id,
                "book_id":book.id
            }
        )
        self.assertEqual(Book_Review.objects.count(), 1)
        self.assertEqual(response.status_code, 201)



    def test_api_review_detail(self):
        book1 = Book.objects.create(
            title='Book of Api',
            description='This book is written about APIs!',
            isbn='35344326464',
        )
        b_r = Book_Review.objects.create(
            user=self.user,
            book=book1,
            stars_given=4,
            body=f'This Review is belongs to {book1.title}'
        )

        response = self.client.get(reverse('api:get-review-detail', kwargs={'id': b_r.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], b_r.id)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['body'], 'This Review is belongs to Book of Api')
        self.assertEqual(response.data['user']['username'], 'ubaydulloh')
        self.assertEqual(response.data['user']['first_name'], 'Ubaydulloh')
        self.assertEqual(response.data['user']['last_name'], 'Qochqarov')

        response = self.client.put(
            reverse('api:get-review-detail', kwargs={'id': b_r.id}),
            data={
                "stars_given":1,
                "body":"Test Updated!!!!!!!!"
            }
        )
        self.assertEqual(response.data['body'], 'Test Updated!!!!!!!!')
        self.assertEqual(response.data['stars_given'], 1)

        response = self.client.delete(reverse('api:get-review-detail', kwargs={'id': b_r.id}),)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book_Review.objects.count(), 0)