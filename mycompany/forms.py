from django import forms
from django.forms import Textarea

from vacancies.models import Company, Vacancy


class CompanyForm(forms.ModelForm):
    fields_with_form_control_class = ['name', 'location', 'employee_count']

    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count', 'logo']
        widgets = {
            'description': Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'color:#000;'})
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        for field in self.fields_with_form_control_class:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


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
