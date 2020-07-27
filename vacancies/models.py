from django.contrib.auth.models import User
from django.db import models

from django.conf import settings


class Specialty(models.Model):
    code = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=120)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, default='100x60.jpg')
    description = models.CharField(max_length=350)
    employee_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=75)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=350)
    description = models.CharField(max_length=700)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField()

    def __str__(self):
        return f'{self.title} in {self.company.name}'


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return f'{self.written_username} application to {self.vacancy.title}'


class Resume(models.Model):
    GradeChoices = (
        ('intern', 'intern'),
        ('junior', 'junior'),
        ('middle', 'middle'),
        ('senior', 'senior'),
        ('lead', 'lead')
    )

    SpecialtyChoices = (
        ('frontend', 'Фронтенд'),
        ('backend', 'Бэкенд'),
        ('gamedev', 'Геймдев'),
        ('devops', 'Девопс'),
        ('design', 'Дизайн'),
        ('products', 'Продукты'),
        ('management', 'Менеджмент'),
        ('testing', 'Тестирование')
    )

    WorkStatusChoices = (
        ('not_in_search', 'Не ищу работу'),
        ('consideration', 'Рассматриваю предложения'),
        ('in_search', 'Ищу работу')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    status = models.CharField(max_length=100, choices=WorkStatusChoices)
    salary = models.IntegerField()
    specialty = models.CharField(max_length=20, choices=SpecialtyChoices)
    grade = models.CharField(max_length=15, choices=GradeChoices)
    education = models.CharField(max_length=300)
    experience = models.CharField(max_length=300)
    portfolio = models.CharField(max_length=300)
