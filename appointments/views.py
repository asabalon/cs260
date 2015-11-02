from django.shortcuts import render

# Create your views here.

def add_appointment(request):
	return render(request, 'add_appointment.html')
