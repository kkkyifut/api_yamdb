import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

from .utilities import send_confirmation_code


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    ]

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        editable=False,
        max_length=36,
        default=uuid.uuid4(),
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


def post_save_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        send_confirmation_code(user)


post_save.connect(post_save_user, sender=User)
