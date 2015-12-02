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
from .views import AppointmentListView, AppointmentFormView

urlpatterns = [
    url(r'^add/$', AppointmentFormView.as_view(), name='add_appointment', ),
    url(r'^add/get_vet_email/$', 'appointments.views.retrieve_vet_email', name='get_vet_email'),
    url(r'^add/create_test_pet/$', 'appointments.views.create_test_pet', name='create_test_pet'),
    url(r'^add/create_test_vet/$', 'appointments.views.create_test_veterinary_physician', name='create_test_vet'),
    url(r'^view/$', AppointmentListView.as_view(), name='view_appointments'),
    url(r'^login/$', 'appointments.views.login_user', name='login'),
    url(r'^register/$', 'appointments.views.register', name='register'),
    url(r'^register/success/$', 'appointments.views.register_success', name='register_success'),
    url(r'^home/$', 'appointments.views.home', name='home'),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': 'appointments:login'}
    ),
    url(
        r'^password_change$',
        'django.contrib.auth.views.password_change',
        name='password_change',
        kwargs={
            'template_name': 'accounts/password_change_form.html',
            'post_change_redirect': 'appointments:password_change_done',
        }
    ),
    url(
        r'^password_change_done$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done',
        kwargs={'template_name': 'accounts/password_change_done.html'}
    ),
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset_form',
        kwargs={
            'template_name': 'registration/password_reset_form.html',
            'post_reset_redirect' : 'appointments:password_reset_done'}),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done',
        kwargs={
            'template_name': 'registration/password_reset_done.html'}),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm',
        kwargs={
            'template_name': 'registration/password_reset_confirm.html',
            'post_reset_redirect' : 'appointments:password_done'}),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_done'),


]
