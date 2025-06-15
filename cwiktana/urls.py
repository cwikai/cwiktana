"""
URL configuration for cwiktana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from . import views  # This is your main project-level views
from accounts import views as accounts_views  # This avoids conflict



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard for logged-in users
    path('manage_members/', views.manage_members, name='manage_members'),#
    path('cookies/', views.cookies, name='cookies'),
    path('privacy/', views.privacy, name='privacy'),   
    path('terms/', views.terms, name='terms'),
    path('add_member/', views.add_member, name='add_member'),
    path('manage_classes/', views.manage_classes, name='manage_classes'),
    path('manage_gradings/', views.manage_gradings, name='manage_gradings'),
    path('licenses/', views.manage_licenses, name='manage_licenses'),
    path('accounts/', include('accounts.urls')),


]
