"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^add/$', 'appointments.views.add_appointment', name='add_appointment'),
    url(r'^add/get_vet_email/$', 'appointments.views.retrieve_vet_email', name='get_vet_email'),
    url(r'^add/create_test_pet/$', 'appointments.views.create_test_pet', name='create_test_pet'),
    url(r'^add/create_test_vet/$', 'appointments.views.create_test_veterinary_physician', name='create_test_vet'),
    url(r'^add/create_test_customer/$', 'appointments.views.create_test_customer', name='create_test_customer'),
    url(r'^view/$', 'appointments.views.view_appointments', name='view_appointments'),
    url(r'^login/$', 'appointments.views.login_user', name='login'),
]

