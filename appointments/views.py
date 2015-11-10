from django.shortcuts import render

from .forms import AppointmentForm
# Create your views here.

def add_appointment(request):
	return render(request, 'add_appointment.html', {'form' : AppointmentForm()})
