from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    'password', forms.ValidationError('Password is wrong'))
        except models.User.DoesNotExist:
            self.add_error(
                'email', forms.ValidationError('User does not exist'))


class SignUpForm(UserCreationForm):

    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    class Meta:
        model = models.User
        fields = ('language', 'first_name', 'last_name', 'email')
        widgets = {
            'language': forms.Select(attrs={'placeholder': 'Language'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                'That email is already raken', code='existing_user'
            )
        except models.User.DoesNotExist:
            return email

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        language = self.cleaned_data.get('language')
        currency_dict = {'en': 'usd', 'kr': 'krw'}
        currency = currency_dict[language]
        user.username = email
        user.set_password(password)
        user.currency = currency
        user.save()
