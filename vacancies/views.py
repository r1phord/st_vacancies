from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from st_vacancies.settings import LOGIN_REDIRECT_URL
from vacancies.forms import ApplicationForm, RegisterForm, LoginForm, ResumeForm
from vacancies.models import Company, Vacancy, Specialty, Application, Resume


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


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all().select_related('company', 'specialty')
        return render(request, 'vacancies/vacancies.html', context={
            'title': 'Все вакансии',
            'vacancies': vacancies
        })


class SpecialtyVacanciesView(View):
    def get(self, request, specialty_code):
        spec = Specialty.objects.filter(code=specialty_code).first()
        if not spec:
            raise Http404('no such specialty')

        vacancies = Vacancy.objects.filter(specialty=spec).select_related('company')
        return render(request, 'vacancies/vacancies.html', context={
            'title': spec.title,
            'spec': spec,
            'vacancies': vacancies
        })


class VacancyView(View):
    def get_vacancy(self, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).select_related('company', 'specialty').first()
        if not vacancy:
            raise Http404

        return vacancy

    def get(self, request, vacancy_id):
        vacancy = self.get_vacancy(vacancy_id)
        return render(request, 'vacancies/vacancy.html', context={
            'vacancy': vacancy,
        })

    def post(self, request, vacancy_id):
        vacancy = self.get_vacancy(vacancy_id)
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            data = application_form.cleaned_data
            Application.objects.create(vacancy=vacancy,
                                       user=request.user,
                                       **data)

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
                    return HttpResponseRedirect(LOGIN_REDIRECT_URL)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
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
            return HttpResponseRedirect('/')

        return render(request, 'register.html', context={
            'form': register_form
        })


class ResumeView(View):
    def get(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if resume:
            resume_form = ResumeForm(instance=resume)
            return render(request, 'vacancies/resume-edit.html', context={
                'form': resume_form
            })
        else:
            return render(request, 'vacancies/resume-create.html')

    def post(self, request):
        user = request.user
        resume = Resume.objects.filter(user=user).first()
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            if resume:
                resume_form = ResumeForm(request.POST, instance=resume)
                resume_form.save()
            else:
                resume = resume_form.save(commit=False)
                resume.user = user
                resume.save()
        return render(request, 'vacancies/resume-edit.html', context={
            'form': resume_form,
            'resume': resume,
        })
