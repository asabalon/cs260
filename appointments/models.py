# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient')
    doctor = models.ForeignKey('Doctor')
    status = models.ForeignKey('AppointmentStatus')
    appointment_date = models.DateTimeField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


class AppointmentStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment_status'


class Doctor(models.Model):
    doctor = models.ForeignKey('UserDetails', primary_key=True)
    specialization = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'doctor'

    def __str__(self):
        user = User.objects.get(id=self.doctor.user_details_id)
        return '%s | %s %s' % (
            self.doctor.user_details_id, user.first_name, user.last_name)


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


class UserDetails(models.Model):
    user_details = models.ForeignKey(User, primary_key=True)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=(('M', 'Male',), ('F', 'Female',)))
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_details'
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'

    def __str__(self):
        return '%s | %s %s' % (self.user_details.id, self.user_details.first_name, self.user_details.last_name)


class UserRole(models.Model):
    user = models.ForeignKey(User)
    role = models.ForeignKey(Role)

    class Meta:
        managed = False
        db_table = 'user_role'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    pass
