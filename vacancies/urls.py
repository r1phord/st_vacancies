from django.urls import path

from vacancies.views import VacanciesView, VacancyView, SpecialtyVacanciesView, SendApplicationView

urlpatterns = [
    path('', VacanciesView.as_view(), name='vacancies'),
    path('<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('cat/<str:specialty_code>/', SpecialtyVacanciesView.as_view(), name='cat_vacancy'),
    path('<int:vacancy_id>/send/', SendApplicationView.as_view(), name='send_application'),

]
