from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea

from vacancies.models import Application, Resume


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class ResumeForm(forms.ModelForm):
    SELECT_CLASSES = 'custom-select mr-sm-2'
    selectors = ['status', 'specialty', 'grade']
    inputs = ['name', 'surname', 'salary', 'experience', 'portfolio', 'education']
    text_areas = ['education', 'experience']

    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'education', 'experience', 'portfolio', 'specialty', 'grade']
        widgets = {
            'education': Textarea(attrs={'style': 'color:#000;', 'rows': '4', 'class': 'text-uppercase'}),
            'experience': Textarea(attrs={'style': 'color:#000;', 'rows': '4'})
        }

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        for field in self.selectors:
            self.fields[field].widget.attrs.update({'class': self.SELECT_CLASSES})

        for field in self.inputs:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['portfolio'].widget.attrs.update({'placeholder': 'http://anylink.github.io'})
