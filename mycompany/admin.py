from django.contrib import admin

from vacancies.models import Company


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
