from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from landingPage import views
from healthcheckup import views

urlpatterns = [
    path('/', views.index, name='index'),
    path('/overview/', views.overview, name='overview'),
    path('/reportinpdf/', views.websitePdfReport, name='websitePdfReport'),
    path('/test/', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


