"""ODDISEAPROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from translator import views as translator_views
from django.conf import settings
from django.conf.urls.static import static


# Definición de urlpatterns
from django.contrib import admin
from django.urls import path
from translator import views as translator_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('text_translation/', translator_views.text_translation, name='text_translation'),
    path('upload/', translator_views.upload_image, name='upload_image'),  
    path('upload/file/', translator_views.upload_file, name='upload_file'),  
    path('capture_and_translate/', translator_views.capture_and_translate, name='capture_and_translate'),
    path('', include('accounts.urls')),

]

# Servir archivos de medios en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
