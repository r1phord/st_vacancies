from datetime import datetime

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from mycompany.forms import CompanyForm, VacancyForm
from vacancies.models import Company, Vacancy, Specialty, Application

BASE_SPECIALTY = Specialty.objects.get(code='backend')


class MyCompanyView(View):
    def get(self, request):
        company = Company.objects.filter(owner=request.user).first()
        if company:
            company_form = CompanyForm(instance=company)
            return render(request, 'mycompany/company-edit.html', context={
                'company': company,
                'form': company_form
            })
        else:
            return render(request, 'mycompany/company-create.html')

    def post(self, request):
        user = request.user
        company = Company.objects.filter(owner=user).first()
        company_form = CompanyForm(request.POST, request.FILES)
        if company_form.is_valid():
            if company:
                company_form = CompanyForm(request.POST, request.FILES, instance=company)
                company_form.save()
            else:
                company = company_form.save(commit=False)
                company.owner = user
                company.save()
        return render(request, 'mycompany/company-edit.html', context={
            'form': company_form,
            'company': company,
        })


class MyCompanyVacanciesView(ListView):
    model = Vacancy
    template_name = 'mycompany/vacancy-list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company, owner=user)
        return Vacancy.objects.filter(company=company)


def create_vacancy(request):
    company = get_object_or_404(Company, owner=request.user)
    vacancy = Vacancy.objects.create(
        title='default title',
        company=company,
        skills='default skills',
        description='default description',
        salary_min=0,
        salary_max=0,
        published_at=datetime.today().strftime('%Y-%m-%d')
    )
    return HttpResponseRedirect(reverse('edit vacancy', args=[vacancy.id]))


class EditVacancyView(View):
    def get_data_for_context(self, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if not vacancy:
            raise Http404()
        specialties = Specialty.objects.all()
        vacancy_applications = Application.objects.filter(vacancy=vacancy)
        form = VacancyForm(instance=vacancy)

        context = {
            'form': form,
            'vacancy': vacancy,
            'specialties': specialties,
            'applications': vacancy_applications
        }
        return context

    def get(self, request, vacancies_id):
        context = self.get_data_for_context(vacancies_id)
        return render(request, 'mycompany/vacancy-edit.html', context=context)

    def post(self, request, vacancies_id):
        context = self.get_data_for_context(vacancies_id)
        vacancy = context['vacancy']
        vacancy_form = VacancyForm(request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy_form.save()

        context['form'] = vacancy_form
        return render(request, 'mycompany/vacancy-edit.html', context=context)
