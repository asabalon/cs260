from datetime import timedelta
from django.test import TestCase
from django.forms import ModelForm, ValidationError
from django.utils.timezone import localtime, now
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Reset, HTML
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.test import Client
from .forms import AppointmentForm
from .models import Pet, Customer, Appointment, VeterinaryPhysician


class AddAppointmentPageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AddAppointmentPageTests, cls).setUpClass()
        cls.client = Client()
        user = User.objects.create_user('temp', 'temporary@gmail.com', 'secret')
        user.save()

    @classmethod
    def tearDownClass(cls):
        super(AddAppointmentPageTests, cls).tearDownClass()

    def setUp(self):
        self.client.login(username='temp', password='secret')

    def tearDown(self):
        pass

    def goto_add_appointment_with_params(self, dictionary):
        return self.client.post(
            '/appointments/add/',
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
            first_name='My',
            middle_name='First',
            last_name='Customer',
        )
        customer.save()

        return customer

    def create_veterinary_physician(self):
        veterinary_physician = VeterinaryPhysician.objects.create(
            first_name='My',
            middle_name='First',
            last_name='Veterinary Physician',
            email_address='cs2602015project@gmail.com',
        )
        veterinary_physician.save()

        return veterinary_physician

    def test_correct_uri_resolves_to_add_appointment_page(self):
        customer = self.create_customer()

        self.assertTemplateUsed(self.goto_add_appointment_with_params(
            {'pet_owner_name': str(customer), 'pet_owner': customer.id}), 'add_appointment.html')

    def test_add_appointment_page_has_form_in_context(self):
        customer = self.create_customer()

        self.assertTrue('form' in self.goto_add_appointment_with_params(
            {'pet_owner_name': str(customer), 'pet_owner': customer.id}).context)

    def test_add_appointment_page_uses_appointment_form(self):
        customer = self.create_customer()

        self.assertTrue(type(self.goto_add_appointment_with_params(
            {'pet_owner_name': str(customer), 'pet_owner': customer.id}).context['form']) is AppointmentForm)

    def test_add_appointment_form_is_a_model_form(self):
        self.assertTrue(AppointmentForm.__base__ is ModelForm)

    def test_appointment_form_uses_appointment_model(self):
        self.assertTrue(AppointmentForm._meta.model is Appointment)

    def test_appointment_model_refers_to_pet_model(self):
        pet_field = None

        for field in Appointment._meta.get_fields():
            if (field.related_model is Pet):
                pet_field = field
            else:
                continue

        self.assertTrue(pet_field)

    def test_appointment_model_refers_to_customer_model(self):
        customer_field = None

        for field in Appointment._meta.get_fields():
            if (field.related_model is Customer):
                customer_field = field
            else:
                continue

        self.assertTrue(customer_field)

    def test_appointment_model_refers_to_veterinary_physician_model(self):
        veterinary_physician_field = None

        for field in Appointment._meta.get_fields():
            if (field.related_model is VeterinaryPhysician):
                veterinary_physician_field = field
            else:
                continue

        self.assertTrue(veterinary_physician_field)

    def test_add_appointment_form_contains_pet_owner_name_before_post(self):
        customer = self.create_customer()

        form = self.client.get('/appointments/add/?pet_owner=%s' % (customer.id)).context['form']

        self.assertEqual(form['pet_owner_name'].value(), str(customer))

    def test_add_appointment_page_contains_pet_owner_name_after_post(self):
        customer = self.create_customer()

        form = \
            self.goto_add_appointment_with_params(
                {'pet_owner_name': str(customer), 'pet_owner': customer.id}).context[
                'form']

        self.assertEqual(form['pet_owner_name'].value(), str(customer))

    def test_form_helper_adds_necessary_buttons(self):
        index = 0
        for i, object in enumerate(AppointmentForm.helper.layout):
            if (type(object) is FormActions):
                index = i
                break

        for button in AppointmentForm.helper.layout[index]:
            if (type(button) is Submit or Reset or HTML):
                continue
            else:
                self.fail("Unrecognized Layout Object")

        self.assertEqual(len(AppointmentForm.helper.layout[index]), 3)

    def test_appointment_model_uses_regex_validator_for_pet_description_field(self):
        index = 0
        validator_list = Appointment._meta.get_field('pet_description').validators
        for i, validator in enumerate(validator_list):
            if (type(validator) is RegexValidator):
                index = i
                break

        self.assertTrue(type(validator_list[index]) is RegexValidator)

    def test_appointment_model_uses_regex_validator_for_visit_description_field(self):
        index = 0
        validator_list = Appointment._meta.get_field('visit_description').validators
        for i, validator in enumerate(validator_list):
            if (type(validator) is RegexValidator):
                index = i
                break

        self.assertTrue(type(validator_list[index]) is RegexValidator)

    def test_appointment_model_form_has_onchange_behavior_for_veterinary_physician(self):
        form = AppointmentForm()

        self.assertTrue(form.Meta.widgets.get('veterinary_physician').attrs.get('onchange') is not None)

    def test_appointment_model_form_has_queryset_for_pet_name_field(self):
        customer = self.create_customer()

        response = self.goto_add_appointment_with_params(
            {'pet_owner_name': str(customer), 'pet_owner': customer.id})

        self.assertTrue(response.context['form'].fields['pet_name'].queryset is not None)

    def test_appointment_page_has_success_variable_in_context(self):
        customer = self.create_customer()
        pet = self.create_pet(customer)
        veterinary_physician = self.create_veterinary_physician()
        current_datetime = format(localtime(now()) + timedelta(hours=25), '%m/%d/%Y %I:%M %p').replace(' 0',
                                                                                                       ' ').lower()

        response = self.goto_add_appointment_with_params(
            {'pet_owner_name': str(customer), 'pet_name': pet.id,
             'pet_owner': customer.id, 'pet_description': 'Siberian Husky',
             'visit_schedule': current_datetime,
             'visit_description': 'Checkup',
             'veterinary_physician': veterinary_physician.id})

        self.assertEqual(response.context['success'], True)
        self.assertTrue(Appointment.objects.count() == 1)
