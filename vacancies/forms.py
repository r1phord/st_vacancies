from django import forms
from django.contrib.auth.models import User

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
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'education', 'experience', 'portfolio', 'specialty', 'grade']

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        self.fields['status'].widget.attrs.update({
            'class': "custom-select mr-sm-2",
            'id': "userReady",
            'name': "status"
        })
        self.fields['specialty'].widget.attrs.update({
            'class': "custom-select mr-sm-2",
            'id': "userSpecialization",
            'name': "specialty"
        })
        self.fields['grade'].widget.attrs.update({
            'class': "custom-select mr-sm-2",
            'id': "userQualification",
            'name': "grade"
        })
