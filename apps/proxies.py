from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db.models import (CASCADE, BooleanField, CharField, DateField,
                              DateTimeField, FileField, ForeignKey, ImageField,
                              IntegerField, Model, PositiveIntegerField,
                              TextChoices, TextField, URLField, SlugField)
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel

from apps.managers import CustomUserManager
from apps.models import User


class AdminUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'admin'
        verbose_name_plural = "adminlar"
