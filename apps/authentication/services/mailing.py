from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from functools import lru_cache
from email.mime.image import MIMEImage


@lru_cache()
def img_data(name: str) -> MIMEImage:
    with open(f'static/mailing/{name}.gif', 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', f'<{name}>')
    return logo


def send_confirm_code(code: int, user_email: str) -> None:
    html_message = render_to_string(
        'mail.html', {
            'code_confirm': code,
            'site_url': settings.BASE_URL,
        }
    )
    message_text = strip_tags(html_message)

    subject = 'Пароль доступа на сайт'
    from_email = settings.EMAIL_HOST_USER
    to = user_email

    msg = EmailMultiAlternatives(subject, message_text, from_email, [to])
    msg.content_subtype = "related"

    msg.attach_alternative(html_message, "text/html")

    msg.attach(img_data('vk'))
    msg.attach(img_data('tg'))
    msg.attach(img_data('icon'))
    msg.send(fail_silently=False)
