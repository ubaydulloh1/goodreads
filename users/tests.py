from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login, get_user

from users.models import CustomUser


class UserRegistrationTestCase(TestCase):
    def test_user_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'ubaydulloh', 
                'first_name': 'Ubaydulloh',
                'last_name': 'Qochqarov',
                'email': 'ubaydulloh@gmail.com',
                'password': 'somepassword',
            } 
        )

        user = CustomUser.objects.get(username='ubaydulloh')

        self.assertEqual(user.username, 'ubaydulloh')
        self.assertEqual(user.first_name, 'Ubaydulloh')
        self.assertEqual(user.last_name, 'Qochqarov')
        self.assertEqual(user.email, 'ubaydulloh@gmail.com')
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))
    

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Ubaydulloh',
                'email': 'ubaydulloh@gmail.com',
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')


    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'ubaydulloh', 
                'first_name': 'Ubaydulloh',
                'last_name': 'Qochqarov',
                'email': 'invalid-email',
                'password': 'somepassword',
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
    

    def test_user_has_not_created_already(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'ubaydulloh', 
                'first_name': 'Ubaydulloh',
                'last_name': 'Qochqarov',
                'email': 'ubaydulloh@gmail.com',
                'password': 'somepassword',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'ubaydulloh', 
                'first_name': 'Ubaydulloh2',
                'last_name': 'Qochqarov2',
                'email': 'ubaydulloh2@gmail.com',
                'password': 'somepassword2',
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')



class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='ubaydulloh',
            email='user@example.com',
        )
        self.user.set_password('somepassword')
        self.user.save()


    def test_succesfully_user_login(self):
        

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'ubaydulloh',
                'password': 'somepassword',
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)


    def test_wrong_login_fields(self):

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong-username',
                'password': 'somepassword',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        # self.assertFormError(response, 'form', 'username', 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'ubaydulloh',
                'password': 'some-wrong-password',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
    

    def test_logout(self):
        self.assertEqual(CustomUser.objects.count(), 1)

        self.client.login(username='ubaydulloh', password='somepassword')

        response = self.client.get(reverse("users:logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:landing-page'))



class UserProfileTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(
            username='ubaydulloh', 
            first_name="Ubaydulloh",
            last_name='Qochqarov', 
            email='ubaydulloh@gmail.com',
        )

        self.db_user.set_password('somepassword')
        self.db_user.save()

    def test_login_required(self):
        self.assertEqual(CustomUser.objects.count(), 1)

        response = self.client.get(reverse('users:user-profile', kwargs={'username': 'ubaydulloh'}))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response., reverse('users:user-profile', kwargs={'username': 'ubaydulloh'}))

        self.client.login(username='ubaydulloh', password='somepassword')
        response = self.client.get(reverse('users:user-profile', kwargs={'username': 'ubaydulloh'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ubaydulloh')
        self.assertContains(response, 'Ubaydulloh')
        self.assertContains(response, 'Qochqarov')
        self.assertContains(response, 'ubaydulloh@gmail.com')
    
    def test_profile_edit(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.client.login(username='ubaydulloh', password='somepassword')
        response = self.client.get(reverse('users:user-profile', kwargs={'username': 'ubaydulloh'}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('users:profile-edit'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username':'ubaydulloh',
                'first_name':'Ubaydulloh(Updated)',
                'email':'ubaydulloh@gmail.com',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user-profile', kwargs={"username": 'ubaydulloh'}))
        self.db_user.refresh_from_db()
        self.assertEqual(self.db_user.first_name, 'Ubaydulloh(Updated)')
        self.assertEqual(self.db_user.email, 'ubaydulloh@gmail.com')
    
    def test_profile_img(self):
        self.assertEqual(self.db_user.profile_img.url, '/images/default-profile.png')