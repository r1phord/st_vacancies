from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from vacancies.views import MainView, CompanyView, custom_handler500, custom_handler404, ResumeView, SearchView
from users.views import MyLoginView, RegisterView

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('companies/<int:pk>/', CompanyView.as_view(), name='company'),
    path('myresume', ResumeView.as_view(), name='myresume'),
    path('vacancies/', include('vacancies.urls')),
    path('mycompany/', include('mycompany.urls')),
    path('search/', SearchView.as_view(), name='search')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
