"""KindHeart URL Configuration

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Shelter import views
from django.contrib.auth import views

from Shelter.views import home_view, signup_view

urlpatterns = [
                  path('', include('Shelter.urls')),
                  path('admin/', admin.site.urls),
                  path('', home_view, name="home"),
                  path('signup/', signup_view, name="signup"),
                  path('login/', views.LoginView.as_view(), name='login'),
                  path('logout/', views.LogoutView.as_view(), name='logout'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
