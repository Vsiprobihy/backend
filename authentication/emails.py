from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from djoser.email import (
    ActivationEmail,
    PasswordChangedConfirmationEmail,
    PasswordResetEmail,
)


class CustomActivationEmail(ActivationEmail):
    template_name = 'email/activation.html'


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = 'email/password_reset.html'


class CustomPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = 'email/password_reset_confirmation.html'


def send_activation_email(user, uid, token, site_name, domain, protocol='http'):
    subject = f'Account activation on {site_name}'
    from_email = 'no-reply@example.com'
    to_email = [user.email]

    context = {
        'site_name': site_name,
        'protocol': protocol,
        'domain': domain,
        'uid': uid,
        'token': token,
    }

    text_content = render_to_string('email/activation.html', context)
    html_content = render_to_string('email/activation.html', context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')

    email.send()
