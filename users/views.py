import os
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from mysite import settings
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = 'users/login.html'
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f'Welcome back {user.first_name}')
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get('next')
        if next_arg is not None:
            return next_arg
        else:
            return reverse('common:home')


def log_out(request):
    messages.info(request, f'See you later {request.user.first_name}')
    logout(request)
    return redirect(reverse('common:home'))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = 'users/signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('common:home')

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f'Welcome {user.first_name}')
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass
    return redirect(reverse('common:home'))


def github_login(request):
    client_id = os.environ.get('GITHUB_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get('GITHUB_ID')
        client_secret = os.environ.get('GITHUB_SECRET')
        code = request.GET.get('code', None)
        if code is not None:
            token_request = requests.post(
                f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}',
                headers={'Accept': 'application/json'})
            token_json = token_request.json()
            error = token_json.get('error', None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get('access_token')
                profile_request = requests.get(
                    'https://api.github.com/user',
                    headers={
                        'Authorization': f'token {access_token}',
                        'Accept': 'application/json',
                    }
                )
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f'Please log in with: {user.login_method}')
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        if name is not None:
                            user.name = name
                        if bio is not None:
                            user.bio = bio
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(
                        request, f'Welcome back {user.first_name}')
                    return redirect(reverse('common:home'))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


def kakao_login(request):
    client_id = os.environ.get('KAKAO_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/kakao/callback'
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get('code')
        client_id = os.environ.get('KAKAO_ID')
        redirect_uri = 'http://127.0.0.1:8000/users/login/kakao/callback'
        token_request = requests.get(
            f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}')
        token_json = token_request.json()
        error = token_json.get('error', None)
        if error is not None:
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get('access_token')
        profile_request = requests.get(
            'https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'})
        profile_json = profile_request.json()
        email = profile_json.get('kakao_account').get('email')
        if email is None:
            raise KakaoException('Plase also give me your email')
        nickname = profile_json.get('kakao_account').get(
            'profile').get('nickname')
        profile_image_url = profile_json.get('kakao_account').get(
            'profile').get('profile_image_url')
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(
                    f'Please log in with: {user.login_method}')
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image_url is not None:
                photo_request = requests.get(profile_image_url)
                photo = ContentFile(photo_request.content)
                user.avatar.save(f'{nickname}-avatar', photo)
        login(request, user)
        messages.success(request, f'Welcome back {user.first_name}')
        return redirect(reverse('common:home'))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = 'user_obj'


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    models = models.User
    template_name = 'users/update_profile.html'
    fields = (
        'email',
        'first_name',
        'last_name',
        'avatar',
        'gender',
        'bio',
        'birthdate',
        'language',
        'currency',
    )
    success_message = 'Profile Updated'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        self.object.username = email
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['email'].widget.attrs = {'placeholder': 'email'}
        form.fields['first_name'].widget.attrs = {'placeholder': 'first_name'}
        form.fields['last_name'].widget.attrs = {'placeholder': 'last_name'}
        form.fields['bio'].widget.attrs = {'placeholder': 'Bio'}
        form.fields['birthdate'].widget.attrs = {'placeholder': 'Birthdate'}
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView
):

    template_name = 'users/update_password.html'
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['old_password'].widget.attrs = {
            'placeholder': 'Current password'}
        form.fields['new_password1'].widget.attrs = {
            'placeholder': 'New password'}
        form.fields['new_password2'].widget.attrs = {
            'placeholder': 'Confirm new password'}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session['is_hosting']
    except KeyError:
        request.session['is_hosting'] = True
    return redirect(reverse('common:home'))


def switch_language(request):
    lang = request.GET.get('lang', None)
    response = HttpResponse(status=200)
    if lang is not None:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response


def switch_currency(request):
    currency = request.GET.get('currency', None)
    response = HttpResponse(status=200)
    if currency is not None:
        response.set_cookie(settings.CURRENCY_COOKIE_NAME, currency)
    return response
