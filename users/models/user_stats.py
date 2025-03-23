from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .validators import PhoneNumberValidator
from .managers import UserManager
# Create your models here.

phone_number_validator = PhoneNumberValidator()

class User(AbstractBaseUser):
    username = models.CharField(unique = True)
    phone_number = models.CharField(validators=[phone_number_validator], max_length=11)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'avatars/', default = "avatars/default_avatar.png", null = True)
