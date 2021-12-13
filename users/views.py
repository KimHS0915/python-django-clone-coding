from django.contrib import auth
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'users/login.html', context={'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('common:home'))

        return render(request, 'users/login.html', context={'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('common:home'))
