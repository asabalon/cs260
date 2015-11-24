from django.shortcuts import render
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Customer
from .models import VeterinaryPhysician


# Create your views here.

def add_appointment(request):
    # No Login capabilities yet; Need to input id directly
    if (request.method == 'POST'):
        pet_owner_id = request.POST.get('pet_owner')
    else:
        pet_owner_id = request.GET.get('pet_owner')

    # Remove else after developing login features
    if (pet_owner_id):
        customer = Customer.objects.get(id=pet_owner_id)
    else:
        customer = Customer.objects.create()
        customer.first_name = 'Default'
        customer.middle_name = 'Default'
        customer.last_name = 'Default'
        customer.save()
        veterinary_physician = VeterinaryPhysician.objects.create()
        veterinary_physician.first_name = 'Default'
        veterinary_physician.middle_name = 'Default'
        veterinary_physician.last_name = 'Default'
        veterinary_physician.email_address = 'cs2602015project@gmail.com'
        veterinary_physician.save()

    form = AppointmentForm(data=request.POST or None, initial={'pet_owner': customer, 'pet_owner_name': str(customer)})

    if (form.is_valid()):
        form.save()
    else:
        pass

    return render(request, 'add_appointment.html', {'form': form})


def retrieve_vet_email(request):
    if (request.method == 'POST'):
        vet_id = request.POST.get('vet_id')
    else:
        vet_id = request.GET.get('vet_id')

    selected_vet = VeterinaryPhysician.objects.get(id=vet_id)

    return JsonResponse({'vet_email': selected_vet.email_address})
