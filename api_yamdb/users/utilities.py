from django.template.loader import render_to_string
from django.utils.crypto import get_random_string


def make_confirmation_code(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                                    'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                                    '23456789'):
    return get_random_string(length, allowed_chars)


def send_confirmation_code(user):
    context = {
        'username': user.username,
        'email': user.email,
        'confirmation_code': user.confirmation_code,
    }
    subject = render_to_string(
        'emails/send_confirmation_code_subject.txt',
        context
    )
    body_text = render_to_string(
        'emails/send_confirmation_code_body.txt',
        context
    )
    user.email_user(subject, body_text)
