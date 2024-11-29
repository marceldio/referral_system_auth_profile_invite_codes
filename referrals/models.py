from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        extra_fields.setdefault('username', phone_number)  # Устанавливаем username
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True)

    # Указываем, что для аутентификации используется phone_number
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # Поля, которые обязательны при создании суперпользователя

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number  # Автоматически присваиваем username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number


class Profile(models.Model):
    user = models.OneToOneField('referrals.CustomUser', on_delete=models.CASCADE, related_name='profile')
    activated_invite_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Referral(models.Model):
    inviter = models.ForeignKey('referrals.CustomUser', on_delete=models.CASCADE, related_name='referrals')
    invited = models.OneToOneField('referrals.CustomUser', on_delete=models.CASCADE, related_name='invited_by')

    def __str__(self):
        return f"{self.inviter.phone_number} referred {self.invited.phone_number}"



