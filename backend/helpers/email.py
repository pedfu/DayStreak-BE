from backend.settings import *

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

def send_signup_confirmation_email(email, first_name, last_name, username, email_token):
    name = first_name + ' ' + last_name
    context = {
        'name': name,
        'username': username,
        'email': email,
        'callback': f'{FRONTEND_URL}/api/v1/confirm-email?token={email_token}'
    }

    try:
        print('sending email')
        html_email = render_to_string('account/confirm_email_signup.html', context)
        send_mail(
            subject=_('DayStreak - Email confirmation'),
            message='Email confirmation',
            from_email=EMAIL_SENDER,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_email,
        )
        
        print('email sent')
    except Exception as e:
        print('error', e)