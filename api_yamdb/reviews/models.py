import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from users.models import User

SCORE_CHOICES = [(r, r) for r in range(1, 11)]


def validate_year(value):
    if value < 0 and value > datetime.date.today().year:
        raise ValidationError(f'0 < year <= {datetime.date.today().year}')


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.SmallIntegerField('Год', validators=[validate_year])
    description = models.TextField(
        'Описание',
        max_length=200,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField('Genre', through='TitleGenre')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    class Meta:
        ordering = ['-year']


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ['-id']


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField('Оценка', choices=SCORE_CHOICES)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['-pub_date']
