from django.shortcuts import render
from .forms import AppointmentForm
from .models import Customer


# Create your views here.

def add_appointment(request):
    # No Login capabilities yet; Need to input id directly
    if (request.method == 'POST'):
        pet_owner_id = request.POST.get('pet_owner_id')
    else:
        pet_owner_id = request.GET.get('pet_owner_id')

    # Remove else after developing login features
    if (pet_owner_id):
        customer = Customer.objects.get(id=pet_owner_id)
    else:
        customer = Customer.objects.create()
        customer.first_name = "Default"
        customer.middle_name = "Default"
        customer.last_name = "Default"
        customer.save()

    form = AppointmentForm(data=request.POST or None, initial={'pet_owner': customer, 'pet_owner_name': str(customer)})

    if (form.is_valid()):
        form.save()
    else:
        pass

    return render(request, 'add_appointment.html', {'form': form, 'pet_owner_id': customer.id})
