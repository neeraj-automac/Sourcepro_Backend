"""sourcepro2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('sourcepro.urls')),
    path('sourcepro/', include('sourcepro.urls')),
    path('', TemplateView.as_view(template_name='index.html')),

    path('home/', TemplateView.as_view(template_name='index.html')),
    path('home/<int:course_id>/<int:lesson_id>/', TemplateView.as_view(template_name='index.html')),
    path('quiz/<int:course_id>/<int:lesson_id>/', TemplateView.as_view(template_name='index.html')),
    path('mycourses/<int:course_id>/<int:lesson_id>/', TemplateView.as_view(template_name='index.html')),
    path('mycourses/', TemplateView.as_view(template_name='index.html')),
    path('changepassword', TemplateView.as_view(template_name='index.html')),
    path('mydetails/', TemplateView.as_view(template_name='index.html')),
    path('mydetails/editdetails', TemplateView.as_view(template_name='index.html')),
    path('trainingsubscriptions/', TemplateView.as_view(template_name='index.html')),
    path('set-new-password/', TemplateView.as_view(template_name='index.html')),
    # path('changepassword', TemplateView.as_view(template_name='index.html')),

    # path('quiz/',  TemplateView.as_view(template_name='index.html')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
