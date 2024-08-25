import random
from django.core.mail import EmailMessage
from .models import User, OnetimePassword
from django.conf import settings


def generate_otp():
    otp = ''
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def send_otp_email(email):
    subject = 'OTP for account login verification'
    otp_code = generate_otp()
    user = User.objects.get(email=email)
    email_body = (f'Hi {user.username},\n\nYou have requested for a One-Time Password (OTP) to login your account.\n\n'
                  f'OTP: Enter {otp_code} within 6 minutes.\n\nYour faithfully,\nIce Pong Team')
    from_email = settings.EMAIL_HOST_USER

    if OnetimePassword.objects.filter(user=user).exists():
        OnetimePassword.objects.filter(user=user).delete()
    OnetimePassword.objects.create(user=user, code=otp_code)

    send_email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        to=[email],
    )
    send_email.send(fail_silently=True)


def check_otp(user, otp):
    if OnetimePassword.objects.filter(user=user, code=otp).exists():
        OnetimePassword.objects.filter(user=user).delete()
        return True
    return False
