from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db import connection
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime, now
from .forms import AppointmentForm, RegistrationForm, PasswordChangeForm, UserDetailsForm
from .models import Appointment


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'view_appointments.html'

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cursor = connection.cursor()

        cursor.execute((
            "SELECT appointment.*, auth_user.first_name, auth_user.last_name, appointment_status.name as status "
            "FROM appointment, auth_user, patient, user_details, appointment_status "
            "WHERE id = doctor_id AND patient.patient_id = %s AND user_details_id = patient.patient_id "
            "AND appointment.patient_id = patient.patient_id AND appointment_status.status_id = appointment.status_id;"
        ), [user_id])

        appointments = dict_fetchall(cursor)

        return render(request, self.template_name, {'appointments': appointments})

    @method_decorator(login_required(login_url='../login'))
    def dispatch(self, *args, **kwargs):
        return super(AppointmentListView, self).dispatch(*args, **kwargs)


class AppointmentFormView(FormView):
    form_class = AppointmentForm
    template_name = 'add_appointment.html'

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cursor = connection.cursor()

        cursor.execute((
            "SELECT * FROM user_role, auth_user, patient, user_details "
            "WHERE id = %s AND patient_id = id AND user_details_id = id AND user_id = id;"
        ), [user_id])

        patient = dict_fetchall(cursor)

        if (len(patient) > 1 or len(patient) < 1):
            self.template_name = 'error/error.html'
            context = {'error_message': 'Cannot Process your Request this time.'}
        elif ():
            self.template_name = 'error/error.html'
            context = {'error_message': 'You cannot access this page.'}
        else:
            form = self.form_class(initial={
                'patient_name': '%s %s' % (patient[0].get('first_name'), patient[0].get('last_name')),
                'patient': patient[0].get('patient_id'),
            })
            context = {'form': form, 'success': False}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            try:
                user_id = request.user.id
                cursor = connection.cursor()

                # Update User and User Details
                cursor.execute((
                    "INSERT INTO appointment (patient_id, doctor_id, status_id, appointment_date) "
                    "VALUES (%s, %s, 1, %s);"
                ), [form.cleaned_data['patient'].patient_id, form.cleaned_data['doctor'].doctor_id,
                    form.cleaned_data['appointment_date']])

                cursor.execute((
                    "SELECT * FROM auth_user, patient, user_details "
                    "WHERE id = %s AND patient_id = id AND user_details_id = id;"
                ), [user_id])

                patient = dict_fetchall(cursor)

                form = self.form_class(initial={
                    'patient_name': '%s %s' % (patient[0].get('first_name'), patient[0].get('last_name')),
                    'patient': patient[0].get('patient_id'),
                })

                context = {'form': form, 'success': True}
            except Exception as e:
                self.template_name = 'error/error.html'
                context = {'error_message': 'Cannot Process your Request this time.'}
        else:
            context = {}

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='../login'))
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentFormView, self).dispatch(request, *args, **kwargs)


class UserDetailsFormView(FormView):
    form_class = UserDetailsForm
    template_name = 'update_profile.html'

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cursor = connection.cursor()

        cursor.execute((
            "SELECT * FROM auth_user, patient, user_details "
            "WHERE id = %s AND patient_id = id AND user_details_id = id;"
        ), [user_id])

        patient = dict_fetchall(cursor)

        if (len(patient) > 1):
            self.template_name = 'error/error.html'
            context = {'error_message': 'Cannot Process your Request this time.'}
        elif (len(patient) < 1):
            form = self.form_class()
            context = {'form': form, 'success': False}
        else:
            form = self.form_class(initial={
                'first_name': patient[0].get('first_name'),
                'last_name': patient[0].get('last_name'),
                'gender': patient[0].get('gender'),
                'date_of_birth': patient[0].get('date_of_birth'),
                'phone_number': patient[0].get('phone_number'),
                'mobile_number': patient[0].get('mobile_number'),
                'address': patient[0].get('address'),
            })
            context = {'form': form, 'success': False}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user_id = request.user.id
            cursor = connection.cursor()

            try:
                # Update User and User Details
                cursor.execute((
                    "UPDATE auth_user SET first_name = %s, last_name = %s WHERE id = %s;"
                    "UPDATE user_details "
                    "SET gender = %s, date_of_birth = %s, phone_number = %s, mobile_number = %s, address = %s, last_updated = %s "
                    "WHERE user_details_id = %s"
                ), [form.cleaned_data['first_name'], form.cleaned_data['last_name'], user_id,
                    form.cleaned_data['gender'],
                    form.cleaned_data['date_of_birth'], form.cleaned_data['phone_number'],
                    form.cleaned_data['mobile_number'], form.cleaned_data['address'], localtime(now()), user_id])

                cursor.execute((
                    "SELECT * FROM auth_user, patient, user_details "
                    "WHERE id = %s AND patient_id = id AND user_details_id = id;"
                ), [user_id])
                patient = dict_fetchall(cursor)

                form = self.form_class(initial={
                    'first_name': patient[0].get('first_name'),
                    'last_name': patient[0].get('last_name'),
                    'gender': patient[0].get('gender'),
                    'date_of_birth': patient[0].get('date_of_birth'),
                    'phone_number': patient[0].get('phone_number'),
                    'mobile_number': patient[0].get('mobile_number'),
                    'address': patient[0].get('address'),
                })

                context = {'form': form, 'success': True}
            except Exception as e:
                self.template_name = 'error/error.html'
                context = {'error_message': 'Cannot Process your Request this time.'}
        else:
            context = {}

        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='../login'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailsFormView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='../login')
def retrieve_doc_email(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')
    else:
        doc_id = request.GET.get('doc_id')

    cursor = connection.cursor()
    cursor.execute((
        "SELECT * FROM auth_user WHERE id = %s;"
    ), [doc_id])

    doctor = dict_fetchall(cursor)

    return JsonResponse({'doc_email': doctor[0].get('email')})


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


# TODO: Change to Transactions
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, auto_id=False)
        if form.is_valid():
            encrypted_password = make_password(form.cleaned_data['password1'])
            cursor = connection.cursor()

            # Create User
            cursor.execute((
                "INSERT INTO auth_user (password, is_superuser, username, email, is_staff, is_active, date_joined)"
                "VALUES (%s, 0, %s, %s, 0, 1, %s)"
            ), [encrypted_password, form.cleaned_data['username'], form.cleaned_data['email'], localtime(now())])

            # Fetch User Details
            cursor.execute((
                "SELECT id FROM auth_user WHERE username = %s"
            ), [form.cleaned_data['username']])

            user = dict_fetchall(cursor)

            # Create User Details and Patient
            cursor.execute((
                "INSERT INTO user_details (user_details_id) VALUES (%s);"
                "INSERT INTO patient (patient_id, patient_since) VALUES (%s, %s);"
                "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s);"
            ), [user[0].get('id'), user[0].get('id'), localtime(now()), user[0].get('id'), 4])

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
    user_id = request.user.id
    cursor = connection.cursor()
    cursor.execute((
        "SELECT * FROM auth_user, user_details "
        "WHERE id = %s AND user_details_id = id;"
    ), [user_id])

    user = dict_fetchall(cursor)

    if (len(user) > 1 or len(user) < 1):
        return render_to_response('error/error.html', {'error_message': 'Cannot Process your Request this time.'})
    else:
        if (user[0].get('last_updated') is None):
            is_profile_updated = False
        else:
            is_profile_updated = True

        return render_to_response('home.html', {'user': request.user, 'is_profile_updated': is_profile_updated})


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change_form.html'
