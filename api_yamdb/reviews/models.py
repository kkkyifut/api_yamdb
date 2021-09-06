import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# здесь надо подумать над диапазоном годов (может же быть и до н.э. произведение)
YEAR_CHOICES = [(r, r) for r in range(1000, datetime.date.today().year)]
SCORE_CHOICES = [(r, r) for r in range(1, 11)]

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    first_name = models.CharField('first name', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLES,
        default='user'
    )
    confirmation_code = models.PositiveIntegerField(
        'Код подтверждения',
        blank=True,
        null=True,
    )


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.SmallIntegerField('Год', choices=YEAR_CHOICES)
    description = models.TextField('Описание', max_length=200)
    genre = models.ManyToManyField('Genre', through='TitleGenre')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,  # SET_NULL???
        null=True,
        related_name='titles'
    )


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField()


class Genre(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField()


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
