from django.conf import settings
from django.core.mail import send_mail


def my_send_mail(email, url=None):
    recipient_list = [email]
    if url is not None:
        subject = 'Регистрация на сайте обследований'
        message = (f'Добро пожаловать на сайт медицинский обследований.'
                   f'\nПройдите по ссылке для активации аккаунта: {url}')

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list
    )
