from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

from .utilities import make_confirmation_code, send_confirmation_code

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
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=10,
        blank=True,
        null=True,
    )


def post_save_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user.confirmation_code = make_confirmation_code()
        user.save()
        send_confirmation_code(user)


post_save.connect(post_save_user, sender=User)
