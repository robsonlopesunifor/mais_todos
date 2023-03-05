from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django_cryptography.fields import encrypt

User = get_user_model()


class CreditCard(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    exp_date = models.DateField()
    holder = models.CharField(max_length=200)
    number = encrypt(models.CharField(max_length=200))
    cvv = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)

    def __str__(self):
        return f"credit_card {self.id}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
