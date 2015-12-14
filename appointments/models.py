from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey('Patient')
    doctor = models.ForeignKey('Doctor')
    status = models.ForeignKey('AppointmentStatus')
    appointment_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


class AppointmentStatus(models.Model):
    status_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment_status'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Doctor(models.Model):
    doctor = models.ForeignKey('UserDetails', primary_key=True)
    specialization = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'doctor'


class Patient(models.Model):
    patient = models.ForeignKey('UserDetails', primary_key=True)
    patient_since = models.DateField()
    followup_date = models.DateField(blank=True, null=True)
    referred_by = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    display_name = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserDetails(models.Model):
    user_details = models.ForeignKey(User, primary_key=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, blank=True, null=True)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_details'


class UserRole(models.Model):
    user_role_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)
    role = models.ForeignKey(Role, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_role'
