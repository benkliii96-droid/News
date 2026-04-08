from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('newsapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(url='/news/', permanent=True)),
]