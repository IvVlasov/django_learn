from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email'), unique=True)
    is_confirmed = models.BooleanField(('is_confirmed'), default=False)
    is_active = models.BooleanField(('is_active'), default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return str(self.id) + ' ' + self.email

    @property
    def is_staff(self) -> bool:
        return self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
