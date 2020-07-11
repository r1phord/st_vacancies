from django import forms

from vacancies.models import Company, Vacancy


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count', 'logo']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'skills', 'specialty', 'description', 'salary_min', 'salary_max']

    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)
        self.fields['specialty'].widget.attrs.update({
            'class': 'custom-select mr-sm-2',
            'name': 'specialty',
            'id': 'userSpecialization'
        })
