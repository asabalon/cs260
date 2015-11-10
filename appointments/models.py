from django.db import models

# Create your models here.

class Appointment(models.Model):
	petOwnerName = models.CharField(max_length=50, blank=False, editable=False)
	petDescription = models.CharField(max_length=100, blank=False)
	visitSchedule = models.DateTimeField(auto_now=False, auto_now_add=False)
	visitDescription = models.CharField(max_length=100, blank=False)
	veterinaryPhysician = models.CharField(max_length=100, blank=False)


	def __str__(self):
		return "Change Format"