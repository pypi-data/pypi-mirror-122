from django.urls.base import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


User = get_user_model()


def verification_mail(request, username, email):
    user = User.objects.get(email=email)
    uemb64 = urlsafe_base64_encode(force_bytes(email))
    token = default_token_generator.make_token(user)
    vf_link = f"{request.scheme}://{request.META['HTTP_HOST']}/{reverse('email_verify', kwargs={'uemb64': uemb64, 'token': token}).lstrip('/')}"
    
    subject, from_email, to_email = 'Verify Your Account', settings.EMAIL_HOST_USER, [email]
    email_data = {'username': username, 'vf_link': vf_link}
    body = get_template('email/verify_email.html').render(email_data)
    mail = EmailMessage(subject=subject, from_email=from_email, to=to_email, body=body, headers={'Content-Type': 'text/html', 'charset': 'utf-8'})
    
    mail.content_subtype = 'html'
    
    return mail.send(fail_silently=False)