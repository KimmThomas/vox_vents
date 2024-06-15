from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
import re


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    user_type = forms.ChoiceField(choices=[('artist', 'Artist'), ('client', 'Client')])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type')


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Password must contain at least one digit")
        if not re.search(r'[\W_]', password1):  # Special characters
            raise ValidationError("Password must contain at least one special character")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class CustomPasswordResetForm(PasswordResetForm):
    # You can customize this form if needed
    pass

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Password must contain at least one digit")
        if not re.search(r'[\W_]', password1):  # Special characters
            raise ValidationError("Password must contain at least one special character")
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2