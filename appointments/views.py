from django.shortcuts import render
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Pet, Appointment, Customer, VeterinaryPhysician


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
        customer = None
        pet_owner_id = None

    form = AppointmentForm(data=request.POST or None, initial={'pet_owner': customer, 'pet_owner_name': str(customer)})
    form.fields['pet_name'].queryset = Pet.objects.filter(owner_id=pet_owner_id)

    if (form.is_valid()):
        success = True
        form.save()
        form = AppointmentForm(initial={'pet_owner': customer, 'pet_owner_name': str(customer)})
    else:
        success = False

    return render(request, 'add_appointment.html', {'form': form, 'success': success})


def retrieve_vet_email(request):
    if (request.method == 'POST'):
        vet_id = request.POST.get('vet_id')
    else:
        vet_id = request.GET.get('vet_id')

    selected_vet = VeterinaryPhysician.objects.get(id=vet_id)

    return JsonResponse({'vet_email': selected_vet.email_address})


def view_appointments(request):
    if (request.method == 'POST'):
        pet_owner_id = request.POST.get('pet_owner')
    else:
        pet_owner_id = request.GET.get('pet_owner')

    appointments = Appointment.objects.filter(pet_owner_id=pet_owner_id)

    return render(request, 'view_appointments.html', {'appointments': appointments})


def create_test_pet(request):
    if (request.method == 'GET'):
        customer = Customer.objects.get(id=request.GET.get('owner'))
        pet = Pet.objects.create(
            name=request.GET.get('name'),
            breed=request.GET.get('breed'),
            owner=customer,
            age_in_months=request.GET.get('age'),
        )
        pet.save()
        return JsonResponse({'pet_id': pet.id})
    else:
        return JsonResponse({'pet_id': None})


def create_test_customer(request):
    if (request.method == 'GET'):
        customer = Customer.objects.create(
            first_name=request.GET.get('first_name'),
            middle_name=request.GET.get('middle_name'),
            last_name=request.GET.get('last_name'),
        )
        customer.save()
        return JsonResponse({'pet_owner_id': customer.id})
    else:
        return JsonResponse({'pet_owner_id': None})


def create_test_veterinary_physician(request):
    if (request.method == 'GET'):
        veterinary_physician = VeterinaryPhysician.objects.create(
            first_name=request.GET.get('first_name'),
            middle_name=request.GET.get('middle_name'),
            last_name=request.GET.get('last_name'),
            email_address=request.GET.get('email'),
        )
        veterinary_physician.save()
        return JsonResponse({'vet_id': veterinary_physician.id})
    else:
        return JsonResponse({'vet_id': None})
