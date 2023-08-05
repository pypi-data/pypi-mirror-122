from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm, PasswordChangeForm
from django.utils.translation import ugettext as _
from django.conf import settings


User = get_user_model()


class RegistrationForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        'empty_email' : _("Email field cannot be empty."),
        'email_exists' : _("An account with that email already exists."),
    }
    
    is_active = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_active']

    def clean_is_active(self):
        if settings.ALLOW_VERIFICATION:
            return False
        
        return True

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if settings.REQUIRE_EMAIL or settings.ALLOW_VERIFICATION:    
            if not email:
                raise forms.ValidationError(self.error_messages['empty_email'], code='empty_email')

        if settings.UNIQUE_EMAIL and email or settings.ALLOW_VERIFICATION and email:    
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(self.error_messages['email_exists'], code='email_exists')

        return email


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        'same_password' : _("New password cannot be the same as current password."),
    }
    
    def clean_new_password2(self):
        response = super().clean_new_password2()
        if self.user.check_password(self.cleaned_data['new_password1']):
            raise forms.ValidationError(self.error_messages['same_password'], code='same_password')

        return response


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        **PasswordChangeForm.error_messages,
        'same_password' : _("New password cannot be the same as the old password."),
    }
    
    def clean_new_password2(self):
        response = super().clean_new_password2()
        if self.cleaned_data.get('new_password1') == self.cleaned_data.get('old_password'):
            raise forms.ValidationError(self.error_messages['same_password'], code='same_password')

        return response


class CustomPasswordResetForm(PasswordResetForm):
    error_messages = {
        'nonexistant_email' : _("There is no account in our system associated with this email."),
        'unverified_email' : _('Please verify your email first.'),
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['nonexistant_email'], code='nonexistant_email')

        if not user.is_active:
            raise forms.ValidationError(self.error_messages['unverified_email'], code='unverified_email')

        return email


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'unverified' : _("Please verify your email before trying to login."),
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username, is_active=False).exists():
            raise forms.ValidationError(self.error_messages['unverified'], code='unverified')

        return username