from random import randint

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_vacancies.settings')

import django

django.setup()

from django.contrib.auth.models import User


from vacancies import data
from vacancies.models import Company, Specialty, Vacancy


# uncomment if need to clear database

# Company.objects.all().delete()
# Specialty.objects.all().delete()
# Vacancy.objects.all().delete()

id = 2
for company in data.companies:
    Company.objects.create(name=company['name'],
                           owner = User.objects.get(pk=id),
                           location=company['location'],
                           description='some description',
                           employee_count=randint(2, 1000))
    id += 1

for specialty in data.specialties:
    Specialty.objects.create(code=specialty['code'],
                             title=specialty['title'])

for job in data.jobs:
    Vacancy.objects.create(title=job['title'],
                           specialty=Specialty.objects.get(code=job['cat']),
                           company=Company.objects.get(name=job['company']),
                           skills=job['skills'],
                           description=job['desc'],
                           salary_min=job['salary_from'],
                           salary_max=job['salary_to'],
                           published_at=job['posted'])

# Добавить в начало файла перед импортом моделей, если требуется запустить не черз shell
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_vacancies.settings')

# import django

# django.setup()
