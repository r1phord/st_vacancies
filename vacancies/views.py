from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from vacancies.forms import ApplicationForm, RegisterForm, ResumeForm, LoginForm
from vacancies.models import Company, Vacancy, Specialty, Resume


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера.')


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all().prefetch_related('vacancies')
        companies = Company.objects.all().prefetch_related('vacancies')
        return render(request, 'index.html', context={
            'specialties': specialties,
            'companies': companies
        })


class CompanyView(View):
    def get(self, request, company_id):
        company = get_object_or_404(Company, id=company_id)
        vacancies = Vacancy.objects.filter(company=company).select_related('specialty')

        return render(request, 'vacancies/company.html', context={
            'company': company,
            'vacancies': vacancies
        })


class VacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        context['title'] = 'Все вакансии'
        return context

    def get_queryset(self):
        return Vacancy.objects.all().select_related('company')


class SpecialtyVacanciesView(View):
    def get(self, request, specialty_code):
        spec = get_object_or_404(Specialty, code=specialty_code)

        vacancies = Vacancy.objects.filter(specialty=spec).select_related('company')
        return render(request, 'vacancies/vacancies.html', context={
            'title': spec.title,
            'spec': spec,
            'vacancies': vacancies
        })


class VacancyView(View):
    def get_vacancy(self, vacancy_id):
        vacancy = get_object_or_404(Vacancy.objects.select_related('company', 'specialty'), id=vacancy_id)
        return vacancy

    def get(self, request, vacancy_id):
        vacancy = self.get_vacancy(vacancy_id)
        return render(request, 'vacancies/vacancy.html', context={
            'vacancy': vacancy,
        })

    def post(self, request, vacancy_id):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        vacancy = self.get_vacancy(vacancy_id)
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.user = user
            application.vacancy = vacancy
            application.save()
            return HttpResponseRedirect(redirect_to='send')

        return render(request, 'vacancies/vacancy.html', context={
            'vacancy': vacancy,
            'form': application_form
        })


class SendApplicationView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancies/sent.html', context={
            'vacancy_id': vacancy_id
        })


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


class ResumeView(View):
    def get(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if resume:
            resume_form = ResumeForm(instance=resume)
            message = 'Страница редактирования'
            return render(request, 'vacancies/resume-edit.html', context={
                'form': resume_form,
                'message': message
            })
        else:
            return render(request, 'vacancies/resume-create.html')

    def post(self, request):
        user = request.user
        resume = Resume.objects.filter(user=user).first()
        resume_form = ResumeForm(request.POST)
        message = 'Заполните анкету'
        if resume_form.is_valid():
            if resume:
                resume_form = ResumeForm(request.POST, instance=resume)
                resume_form.save()
                message = 'Ваше резюме обновлено!'
            else:
                resume = resume_form.save(commit=False)
                resume.user = user
                resume.save()
                message = 'Ваше резюме создано!'
        return render(request, 'vacancies/resume-edit.html', context={
            'form': resume_form,
            'resume': resume,
            'message': message
        })


class SearchView(ListView):
    model = Vacancy
    template_name = 'vacancies/search.html'

    def get_queryset(self):
        query = self.request.GET.get('s')
        return Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(skills__icontains=query)
        )
