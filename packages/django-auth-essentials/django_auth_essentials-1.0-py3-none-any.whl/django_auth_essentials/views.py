from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.conf import settings

from .forms import RegistrationForm
from .email import verification_mail


User = get_user_model()


def profile(request):
    return render(request, 'accounts/profile.html')

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if settings.ALLOW_VERIFICATION:
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                verification_mail(request, username, email)
                messages.info(request, "We've sent you an email with a verification link. Please verify your email as you won't be able to login if you don't.")
            else:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password2']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
            return redirect('login')

    return render(request, 'accounts/registration.html', context={'form': form})

def verify_account(request, uemb64, token):
    if uemb64 == 'account' and token == 'email':
    
        valid = False
        user_email = force_text(urlsafe_base64_decode(request.session['ACCOUNT_VERIFICATION_BASE64_ENCODE']))
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)

            if default_token_generator.check_token(user, request.session['ACCOUNT_VERIFICATION_TOKEN']):
                valid = True
                user.is_active = True
                user.save()

        del request.session['ACCOUNT_VERIFICATION_BASE64_ENCODE']
        del request.session['ACCOUNT_VERIFICATION_TOKEN']

        context = {'valid': valid}
        return render(request, 'accounts/verify.html', context)

    else:
        request.session['ACCOUNT_VERIFICATION_BASE64_ENCODE'] = uemb64
        request.session['ACCOUNT_VERIFICATION_TOKEN'] = token

        redirect_to = request.path.replace(uemb64, 'account').replace(token, 'email')

        return redirect(redirect_to)

def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account associated with this email exists in our system.')
            return render(request, 'accounts/resend_verification.html')

        if user.is_active:
            messages.error(request, 'Account associated with this email is already verified.')
        else:
            verification_mail(request, user.username, email)
            messages.info(request, 'An email containing verification link was sent to you email account. Please note that the link will expire in 24 hours.')
        
    return render(request, 'accounts/resend_verification.html')