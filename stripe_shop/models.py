from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import stripe
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(verbose_name=_("first name"), max_length=50)
    stripe_customer_id = models.CharField(max_length=120)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name


# @receiver(post_save, sender=CustomUser)
# def _on_update_user(sender, instance, created, **kwargs):

#     if created:  # If a new user is created
#         print(f"Instance is {instance.name}")

#         # Create Stripe user
#         customer = stripe.Customer.create(
#             email=instance.email,
#             #name=instance.name,
#         )
#         print(f"---"*100)

#         # Create profile
#         profile = CustomUser.objects.create(email=instance.email,stripe_customer_id=customer.id)
#         profile.save()

