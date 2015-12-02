from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator
from .forms import AppointmentForm, RegistrationForm, PasswordChangeForm
from .models import Pet, Appointment, Customer, VeterinaryPhysician


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'view_appointments.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Appointment.objects.filter(pet_owner_id=request.user.id)

        return render(request, self.template_name, {'appointments': self.queryset})

    @method_decorator(login_required(login_url='../login'))
    def dispatch(self, *args, **kwargs):
        return super(AppointmentListView, self).dispatch(*args, **kwargs)


class AppointmentFormView(FormView):
    form_class = AppointmentForm
    template_name = 'add_appointment.html'

    def get(self, request, *args, **kwargs):
        pet_owner_id = request.user.id
        customer = Customer.objects.get(id=pet_owner_id)
        form = self.form_class(initial={
            'pet_owner': customer,
            'pet_owner_name': str(customer),
        })

        return render(request, self.template_name, {'form': form, 'success': False})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            success = True
            form.save()
            customer = form.instance.pet_owner
            form = self.form_class(
                initial={'pet_owner': customer, 'pet_owner_name': str(customer)})
        else:
            success = False

        return render(request, self.template_name, {'form': form, 'success': success})

    @method_decorator(login_required(login_url='../login'))
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentFormView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='../login')
def retrieve_vet_email(request):
    if request.method == 'POST':
        vet_id = request.POST.get('vet_id')
    else:
        vet_id = request.GET.get('vet_id')

    selected_vet = VeterinaryPhysician.objects.get(id=vet_id)

    return JsonResponse({'vet_email': selected_vet.email})


# Need Pet Registration Feature
@login_required(login_url='../login')
def create_test_pet(request):
    if request.method == 'GET':
        customer = Customer.objects.get(id=request.user.id)
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


# Need Separate Registration for Veterinary Physicians
@login_required(login_url='../login')
def create_test_veterinary_physician(request):
    if (request.method == 'GET'):
        veterinary_physician = VeterinaryPhysician.objects.create(
            username=request.GET.get('username'),
            first_name=request.GET.get('first_name'),
            middle_name=request.GET.get('middle_name'),
            last_name=request.GET.get('last_name'),
            email=request.GET.get('email'),
        )
        veterinary_physician.save()
        return JsonResponse({'vet_id': veterinary_physician.id})
    else:
        return JsonResponse({'vet_id': None})


# Need Update Profile Features
@login_required(login_url='../login')
def update_user_details(request):
    if (request.method == 'GET'):
        customer = Customer.objects.get(id=request.user.id)

        print(customer)
        print(type(customer.first_name))
        customer.first_name = request.GET.get('first_name'),
        customer.middle_name = request.GET.get('middle_name'),
        customer.last_name = request.GET.get('last_name'),
        customer.save()

        print(type(customer.first_name))

        return JsonResponse({'result': str(customer)})
    else:
        return JsonResponse({'result': None})


def login_user(request):
    state = ""
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect(request.META.get('HTTP_REFERRER', '../home'))
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Username/Password is incorrect"

    return render_to_response('auth.html', {'state': state, 'username': username})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, auto_id=False)
        if form.is_valid():
            user = Customer.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('../register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response('registration/register.html', variables, )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


@login_required(login_url='../login', redirect_field_name=None)
def home(request):
    pet_owner_id = request.user.id
    customer = Customer.objects.get(id=pet_owner_id)
    return render_to_response('home.html', {'user': request.user, 'pet_owner': customer})


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change_form.html'
