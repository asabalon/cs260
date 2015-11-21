from django.db import models


# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s, %s %s" % (self.last_name, self.first_name, self.middle_name)

class VeterinaryPhysician(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s, %s %s" % (self.last_name, self.first_name, self.middle_name)


class Appointment(models.Model):
    pet_owner = models.ForeignKey(Customer)
    pet_description = models.CharField(max_length=500)
    visit_schedule = models.DateTimeField(auto_now=False, auto_now_add=False)
    visit_description = models.CharField(max_length=500)
    veterinary_physician = models.ForeignKey(VeterinaryPhysician)

    def __str__(self):
        return "%s : %s : %s" % (self.pet_owner, self.visit_schedule, self.veterinary_physician)
