from datetime import timedelta
from django.test import TestCase
from django.forms import ModelForm, ValidationError
from django.utils.timezone import localtime, now
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Reset, HTML
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.test import Client
from appointments.forms import AppointmentForm
from appointments.models import Pet, Customer, Appointment, VeterinaryPhysician
from appointments.views import AppointmentListView


class ViewAppointmentsPageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewAppointmentsPageTests, cls).setUpClass()
        cls.client = Client()
        user = User.objects.create_user('temp', 'temporary@gmail.com', 'secret')
        user.save()

    @classmethod
    def tearDownClass(cls):
        super(ViewAppointmentsPageTests, cls).tearDownClass()

    def setUp(self):
        self.client.login(username='temp', password='secret')

    def tearDown(self):
        pass

    def goto_view_appointments_with_params(self, dictionary):
        return self.client.get(
            '/appointments/view/',
            dictionary,
        )

    def create_pet(self, customer):
        pet = Pet.objects.create(
            name='Doggy',
            breed='Siberian Husky',
            owner=customer,
            age_in_months=1,
        )
        pet.save()

        return pet

    def create_customer(self):
        customer = Customer.objects.create(
            username='customer',
            first_name='My',
            middle_name='First',
            last_name='Customer',
        )
        customer.save()

        return customer

    def create_veterinary_physician(self):
        veterinary_physician = VeterinaryPhysician.objects.create(
            username='veterinary_physician',
            first_name='My',
            middle_name='First',
            last_name='Veterinary Physician',
            email='cs2602015project@gmail.com',
        )
        veterinary_physician.save()

        return veterinary_physician

    def create_appointment(self, customer, pet, veterinary_physician):
        current_datetime = localtime(now()) + timedelta(hours=25)
        appointment = Appointment.objects.create(
            pet_name=pet,
            pet_owner=customer,
            visit_description='Checkup',
            visit_schedule=current_datetime,
            veterinary_physician=veterinary_physician
        )
        appointment.save()

        return appointment

    def test_view_appointments_page_is_a_list_view(self):
        self.assertTrue(AppointmentListView.__base__ is ListView)

    def test_correct_uri_resolves_to_view_appointments_page(self):
        customer = self.create_customer()

        self.assertTemplateUsed(self.goto_view_appointments_with_params(
            {'pet_owner': customer.id}), 'view_appointments.html')

    def test_view_appointments_page_uses_appointment_model(self):
        appointment_list_view = AppointmentListView()

        self.assertTrue(appointment_list_view.model is Appointment)

    def test_view_appointments_page_has_correct_queryset(self):
        veterinary_physician = self.create_veterinary_physician()

        customer = self.create_customer()
        other_customer = Customer.objects.create_user('other_user', 'other@email.com', 'other_password')
        other_customer.save()

        pet = self.create_pet(customer)
        other_pet = self.create_pet(other_customer)

        self.create_appointment(customer, pet, veterinary_physician)
        self.create_appointment(other_customer, other_pet, veterinary_physician)

        response = self.goto_view_appointments_with_params(
            {'pet_owner': customer.id}
        )

        self.assertEqual(len(response.context['appointments']), 1)
        self.assertEqual(Appointment.objects.filter(pet_owner_id=customer.id)[0].id,
                         response.context['appointments'][0].id)

    def test_view_appointments_page_has_appointments_in_context(self):
        customer = self.create_customer()

        response = self.goto_view_appointments_with_params(
            {'pet_owner': customer.id}
        )

        self.assertTrue('appointments' in response.context)
