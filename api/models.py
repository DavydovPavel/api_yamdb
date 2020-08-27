from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()

def range_of_1_10(value):
    if not (1 <= value <= 10):
        raise ValidationError('Оценка должна быть в диапазоне от 1 до 10')

class BaseForCommAndRev(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comments",
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.text


class Comments(BaseForCommAndRev):
    review = models.ForeignKey(
        Review, 
        on_delete=models.CASCADE, 
        related_name="comments",
        verbose_name='Отзыв'
    )    

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


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
