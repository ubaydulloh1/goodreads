from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    profile_img = models.ImageField(default='default-profile.png')

    def __str__(self):
        return self.username

    def fullName(self):
        return f'{self.first_name} {self.last_name}'
