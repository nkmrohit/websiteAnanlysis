from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('', include('landingPage.urls')),
    url('healthcheckup', include('healthcheckup.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


