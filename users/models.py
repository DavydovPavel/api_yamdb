from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_('email'), max_length=40, unique=True)
    bio = models.TextField(_('description'), max_length=500, blank=True)
    role = models.CharField(_('role'), max_length=30, default='user')
    token = models.CharField(_('token'), max_length=36, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def check_token(self, token):
        return self.token == token
