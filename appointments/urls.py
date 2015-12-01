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
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from .views import AppointmentListView, AppointmentFormView

urlpatterns = [
    url(r'^add/$', AppointmentFormView.as_view(), name='add_appointment', ),
    url(r'^add/get_vet_email/$', 'appointments.views.retrieve_vet_email', name='get_vet_email'),
    url(r'^add/create_test_pet/$', 'appointments.views.create_test_pet', name='create_test_pet'),
    url(r'^add/create_test_vet/$', 'appointments.views.create_test_veterinary_physician', name='create_test_vet'),
    url(r'^view/$', AppointmentListView.as_view(), name='view_appointments'),
    url(r'^login/$', 'appointments.views.login_user', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": reverse_lazy('login')}, name="logout"),
    url(r'^register/$', 'appointments.views.register', name='register'),
    url(r'^register/success/$', 'appointments.views.register_success',name='register_success'),
    url(r'^home/$', 'appointments.views.home', name='home'),
]

