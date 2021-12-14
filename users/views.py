from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):

    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('common:home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse('common:home'))
