from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

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


class SignUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'language')

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='Confirm Password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password confirmation does not match')
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        language = self.cleaned_data.get('language')
        currency_dict = {'en': 'usd', 'kr': 'krw'}
        currency = currency_dict[language]
        user.username = email
        user.set_password(password)
        user.currency = currency
        user.save()
