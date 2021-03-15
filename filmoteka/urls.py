# Import modulu admin z balíku django.contrib
from django.contrib import admin
# Import modulu path z balíku django.urls
from django.urls import path
# Import metody include() -pomocí ní připojíme cesty nastavené v souboru urls.py, který je součástí aplikace movies
from django.urls import include
# Třída RedirectView, která je součástí balíku django.views.generic umožňuje přesměrování pohledů (stránek)
from django.views.generic import RedirectView
# Z balíku django.conf importujeme nastavení (settings)
from django.conf import settings
# Z balíku django.conf.urls.static importujeme metodu static(),
# # pomocí které zajistíme obsluhu statických souborů (jen ve vývojové fázi aplikace)
from django.conf.urls.static import static

# Mapování URL adres webu -propojení URL s jejich obsluhou
urlpatterns = [
# URL "admin/" je namapováno na administrační rozhraní webu
path('admin/', admin.site.urls),
# URL "movies/" je namapováno na aplikaci movies a její vlastní soubor 'movies.urls'
path('movies/', include('movies.urls')),
# domovská stránka webu ('') je automaticky přesměrována na url z předešlého řádku ('movies')
path('', RedirectView.as_view(url='movies/')),] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Metodou static() zajistíme správné mapování adres statických souborů webu (css, js, obrázků atd.).
# Jejich umístění bude definováno konstantami STATIC_URL a STATIC_ROOT v souboru settings.py

"""filmoteka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
