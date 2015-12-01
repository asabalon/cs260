from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# Create your models here.

class Customer(User):
    middle_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s, %s %s" % (self.last_name, self.first_name, self.middle_name)


class Pet(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    owner = models.ForeignKey(Customer)
    age_in_months = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "%s : %s" % (self.name, self.breed)


class VeterinaryPhysician(User):
    middle_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s, %s %s" % (self.last_name, self.first_name, self.middle_name)


class Appointment(models.Model):
    without_special_chars = RegexValidator(r'^[0-9a-zA-Z\s,.?!-]*$', 'No Special Characters are allowed in this field')

    pet_owner = models.ForeignKey(Customer)
    pet_name = models.ForeignKey(Pet)
    pet_description = models.CharField(max_length=500, blank=True, validators=[without_special_chars])
    visit_schedule = models.DateTimeField(auto_now=False, auto_now_add=False)
    visit_description = models.CharField(max_length=500, validators=[without_special_chars])
    veterinary_physician = models.ForeignKey(VeterinaryPhysician)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "%s : %s : %s" % (self.pet_owner, self.visit_schedule, self.veterinary_physician)
