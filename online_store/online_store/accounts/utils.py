from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from online_store.accounts.models import AppUser
from online_store.accounts.tokens import token_generator


def send_email(request, user, subject_value, path):
    current_site = get_current_site(request)
    subject = subject_value
    message = render_to_string(path, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })

    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    return email.send()


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = int(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Успешно активирахте своя акаунт. Може да се логнете с имейл и парола.')
        return redirect('login')
    else:
        return redirect('register')


def reset_password_validate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
        user = None
        uid = None

    if user is not None and token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Успешно удостоверихте своя имейл. Моля изберете нова парола за акаунта.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Тази връзка е изтекла. Моля опитайте отново!')
        return redirect('login')
