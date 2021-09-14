from django.template.loader import render_to_string


def send_confirmation_code(user):
    context = {
        'user': user,
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


def remind_confirmation_code(user):
    context = {
        'user': user,
    }
    subject = render_to_string(
        'emails/remind_confirmation_code_subject.txt',
        context
    )
    body_text = render_to_string(
        'emails/remind_confirmation_code_body.txt',
        context
    )
    user.email_user(subject, body_text)
