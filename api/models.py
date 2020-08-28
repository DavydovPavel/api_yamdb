from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=40, unique=True)
    username = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


def range_of_1_10(value):
    if not (1 <= value <= 10):
        raise ValidationError('Оценка должна быть в диапазоне от 1 до 10')


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField('Genre', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class BaseForCommAndRev(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Review(BaseForCommAndRev):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(validators=[range_of_1_10])

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Comment(BaseForCommAndRev):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
