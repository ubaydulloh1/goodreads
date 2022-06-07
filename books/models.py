from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser



class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    social_telegram = models.CharField(max_length=100, null=True, blank=True)
    social_instagram = models.CharField(max_length=100, null=True, blank=True)
    social_twitter = models.CharField(max_length=100, null=True, blank=True)
    social_facebook = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # def fullName(self):
    #     return f'{self.user.first_name} {self.user.last_name}'




class Book(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    cover_img = models.ImageField(default='default_book_cover_img.jpg')
    isbn = models.CharField(max_length=17, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    reviews_count = models.FloatField(null=True, blank=True)
    reviews_average = models.FloatField(null=True, blank=True)

    def reviewQuality(self):
        reviews = self.book_review_set.all()
        reviews_count = len(reviews)
        average_review = 0
        for review in reviews:
            average_review += review.stars_given
        if reviews_count:
            average_review = average_review / reviews_count
                
        self.reviews_average = average_review
        self.reviews_count = reviews_count
        self.save()

    class Meta:
        ordering = ['-reviews_average', '-reviews_count', '-created']
        

    def __str__(self):
        return self.title
    



class Author_Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book} by {self.author}'




class Book_Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        super(Book_Review, self).save(**kwargs)
        self.book.reviewQuality()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.book} commented by {self.user.username} {self.stars_given} star!'
