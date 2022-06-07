from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from books.models import Author

from django.conf import settings
from users.tasks import send_email_celery



@receiver(post_save, sender=CustomUser)
def send_email_user_created(sender, instance, created, **kwargs):

    if created:
        Author.objects.create(
            user=instance,
        )
    
    if instance.email:
        subject = "Welcome to Goodreads Clone!"
        message = f"Hi {instance.username}, thank you for registering our website! "
        email_from = settings.EMAIL_HOST_USER
        receipent_list = [instance.email,]
        send_email_celery(subject, message, email_from, receipent_list)
