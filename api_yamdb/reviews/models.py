import datetime

from django.core.exceptions import ValidationError
from django.db import models

from users.models import User

SCORE_CHOICES = [(r, r) for r in range(1, 11)]


def validate_year(value):
    if value < 0 and value > datetime.date.today().year:
        raise ValidationError(f'0 < year <= {datetime.date.today().year}')


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='slug', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=100)
    slug = models.SlugField(verbose_name='slug', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.SmallIntegerField(
        verbose_name='Год', validators=[validate_year], db_index=True
    )
    description = models.TextField(
        verbose_name='Описание', max_length=200, blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', related_name='titles'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-year']

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка', default=1, blank=False, null=False, choices=SCORE_CHOICES
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title, related_name='reviews', on_delete=models.CASCADE
    )

    def __str__(self):
        return(f'{self.id}. {self.text[:50]}')

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        ordering = ['-pub_date']
