from django.contrib import admin

from vacancies.models import Vacancy, Application, Specialty


class SpecialtyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Specialty, SpecialtyAdmin)


class VacancyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Application, ApplicationAdmin)
