from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Pet, Appointment, Customer, VeterinaryPhysician


# Create your views here.

@login_required(login_url='../login')
def add_appointment(request):
    # No Login capabilities yet; Need to input id directly
    if request.method == 'POST':
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

    if form.is_valid():
        success = True
        form.save()
        form = AppointmentForm(initial={'pet_owner': customer, 'pet_owner_name': str(customer)})
    else:
        success = False

    return render(request, 'add_appointment.html', {'form': form, 'success': success})


@login_required(login_url='../login')
def retrieve_vet_email(request):
    if request.method == 'POST':
        vet_id = request.POST.get('vet_id')
    else:
        vet_id = request.GET.get('vet_id')

    selected_vet = VeterinaryPhysician.objects.get(id=vet_id)

    return JsonResponse({'vet_email': selected_vet.email_address})


@login_required(login_url='../login')
def view_appointments(request):
    if request.method == 'POST':
        pet_owner_id = request.POST.get('pet_owner')
    else:
        pet_owner_id = request.GET.get('pet_owner')

    appointments = Appointment.objects.filter(pet_owner_id=pet_owner_id)

    return render(request, 'view_appointments.html', {'appointments': appointments})


@login_required(login_url='../login')
def create_test_pet(request):
    if request.method == 'GET':
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


@login_required(login_url='../login')
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


@login_required(login_url='../login')
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


def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect(request.META.get('HTTP_REFERRER', '../add'))
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html', {'state': state, 'username': username})

