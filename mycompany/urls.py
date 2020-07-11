from django.urls import path

from mycompany.views import MyCompanyView, MyCompanyVacanciesView, EditVacancyView, create_vacancy

urlpatterns = [
    path('', MyCompanyView.as_view(), name='my company'),
    path('vacancies/', MyCompanyVacanciesView.as_view(), name='mycompany vacancies'),
    path('vacancies/create/', create_vacancy, name='create vacancy'),
    path('vacancies/<int:vacancies_id>/', EditVacancyView.as_view(), name='edit vacancy'),
]
