from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegisterForm
from st_vacancies import settings

class MyLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
                else:
                    login_form.add_error(None, 'Disabled account')
            else:
                login_form.add_error(None, 'invalid login or password')
        return render(request, 'login.html', context={
            'form': login_form
        })


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            User.objects.create_user(**data)
            user = authenticate(username=register_form.data['username'],
                                password=register_form.data['password'])
            login(request, user)
            return HttpResponseRedirect('/')

        return render(request, 'register.html', context={
            'form': register_form
        })
