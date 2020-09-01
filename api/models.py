from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def range_of_1_10(value):
    if not (1 <= value <= 10):
        raise ValidationError('Оценка должна быть в диапазоне от 1 до 10')


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, related_name='categories', null=True)
    genre = models.ManyToManyField('Genre', related_name='genres', blank=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class BaseForCategoryGenre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name


class Category(BaseForCategoryGenre):
    pass


class Genre(BaseForCategoryGenre):
    pass


class BaseForCommAndRev(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='дата создания'
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
        verbose_name='произведение'
    )
    score = models.PositiveSmallIntegerField('оценка', validators=[range_of_1_10])

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Comment(BaseForCommAndRev):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='отзыв'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
