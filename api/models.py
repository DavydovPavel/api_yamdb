from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


def range_of_1_10(value):
    if not (1 <= value <= 10):
        raise ValidationError('Оценка должна быть в диапазоне от 1 до 10')


class Title(models.Model):
    name = models.CharField("Название", max_length=100)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField('Genre', related_name='genres', blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    #rating = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        rate = Title.objects.get(
            pk=self.id).reviews.all().aggregate(models.Avg('score'))
        return rate['score__avg']


class BaseForCategoryGenre(models.Model):
    name = models.CharField("Наименование", max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseForCategoryGenre):
    pass

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseForCategoryGenre):
    pass

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


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
    score = models.PositiveSmallIntegerField(
        'оценка', validators=[range_of_1_10]
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


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
