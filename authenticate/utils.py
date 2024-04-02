import random
import smtplib

from django.core.cache import cache
from django.core.mail import send_mail

from authenticate.models import User
from diploma import settings


def generate_random_activation_code() -> int:
    random_number = random.randint(1000, 9999)

    return random_number


def save_generated_activation_code(cache_key, email) -> int or None:
    try:
        user_id = User.objects.get(login=email).id
        activation_code = generate_random_activation_code()
        cache.set(f'{cache_key}_{user_id}', activation_code, timeout=60*5)
        return activation_code

    except User.DoesNotExist:
        return None


def check_activation_code(cache_key, email, activation_code) -> bool:
    try:
        user_id = User.objects.get(login=email).id
        saved_activation_code = cache.get(f'{cache_key}_{user_id}')
        if saved_activation_code == activation_code:
            return True
        else:
            return False

    except User.DoesNotExist:
        return False


def send_activation_code(cache_key, email):
    activation_code = save_generated_activation_code(cache_key, email)

    subject = 'User activation code'
    message = f'Your activation code: {activation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    # server.sendmail(from_email, recipient_list, message)
    # server.close()

    send_mail(subject, message, from_email, recipient_list)
