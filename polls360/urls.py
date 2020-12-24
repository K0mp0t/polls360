# polls360 URL Configuration

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('users/', include('login.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('polls/', include('polls.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
