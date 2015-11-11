from django.shortcuts import render

from .forms import AppointmentForm
from .models import Customer
from .models import Appointment
# Create your views here.

def add_appointment(request):

	# No Login capabilities yet; Need to input id directly
	if (request.method == 'POST'):
		pet_owner_id = request.POST.get('pet_owner_id')
	else:
		pet_owner_id = request.GET.get('pet_owner_id')

	# Remove else after developing login features
	if (pet_owner_id is not None):
		customer = Customer.objects.get(id=pet_owner_id)
	else:
		customer = Customer.objects.create()
		customer.first_name = "Default"
		customer.middle_name = "Default"
		customer.last_name = "Default"
		customer.save()

	form = AppointmentForm(request.POST or None)

	# Remove else after developing login features
	if (form.is_valid()):
		model_instance = form.save(commit=False)
		model_instance.pet_owner = customer
		model_instance.save()
	else:
		form = AppointmentForm(initial = {'pet_owner' : customer})

	return render(request, 'add_appointment.html', {'form' : form, 'pet_owner_id' : customer.id})
