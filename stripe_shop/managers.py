from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, name,**extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))


        email = self.normalize_email(email)


        customer = stripe.Customer.create(
            email=email,
            name=name,
        )

        print("--"*100)

        user = self.model(email=email,name=name, stripe_customer_id=customer.id ,**extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password,name,**extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, name,**extra_fields)