from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import random
import string
from .models import Register
from .utils import send_email


def generate_verification_code(length=6):
    characters = string.digits
    verification_code = ''.join(random.choice(characters) for i in range(length))
    return verification_code

@receiver(post_save, sender=Register)
def send_book_email(instance, created, **kwargs):
    if created:
        verification_code = generate_verification_code()
        instance.email_token = verification_code
        instance.save()
        subject = 'Verification Code'
        message = f'Your verification code is: {verification_code}'
        recipient_list = [instance.email]

        send_email(subject=subject,
                   message=message,
                   recipient_list=recipient_list)