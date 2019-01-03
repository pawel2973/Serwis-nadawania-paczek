from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import FormParcelSize, ContactForm
from .models import Courier, EnvelopePricing, Address, RecipientAddress, SenderAddress, PackPricing, PalletPricing


class ModelTest(TestCase):
    def setUp(self):
        Courier.objects.create(name='UPC')
        self.courier_object = Courier.objects.get(pk=1)

        EnvelopePricing.objects.create(courier=self.courier_object, up_to_1=1.0)
        PackPricing.objects.create(courier=self.courier_object, up_to_1=1.0, up_to_2=2.0, up_to_5=5.0, up_to_10=10.0,
                                   up_to_15=15.0, up_to_20=20.0, up_to_30=30.0)
        PalletPricing.objects.create(courier=self.courier_object, up_to_300=100.0, up_to_500=200.0, up_to_800=300.0,
                                     up_to_1000=400.0)

        data_address = {'name': 'John', 'surname': 'Tester', 'zip_code': '33-333', 'city': 'Rzeszow',
                        'street': 'Kwiatowa', 'house_number': 52, 'telephone_number': '888000111',
                        'email_address': 'correct@email.ad'}
        self.address_object = Address.objects.create(**data_address)

    def test_courier_content(self):
        expected_object_name = '{}'.format(self.courier_object.name)
        self.assertEqual(expected_object_name, 'UPC')

    def test_envelope_pricing_content(self):
        envelope = EnvelopePricing.objects.get(pk=1)
        expected_price = envelope.up_to_1
        self.assertEqual(expected_price, 1.0)

    def test_courier_self(self):
        courier_object = Courier.objects.get(pk=1)
        self.assertTrue(isinstance(courier_object, Courier))
        self.assertEqual(courier_object.__str__(), courier_object.name)

    def test_address_self(self):
        self.assertTrue(isinstance(self.address_object, Address))
        self.assertEqual(self.address_object.__str__(), self.address_object.zip_code + " " + self.address_object.city)

    def test_address_rec_self(self):
        address_recipient = RecipientAddress.objects.create(address=self.address_object)
        self.assertTrue(isinstance(address_recipient, RecipientAddress))
        self.assertEqual(address_recipient.__str__(),
                         address_recipient.address.name + " " + address_recipient.address.surname)

    def test_address_sender_self(self):
        address_sender = SenderAddress.objects.create(address=self.address_object)
        self.assertTrue(isinstance(address_sender, SenderAddress))
        self.assertEqual(address_sender.__str__(),
                         address_sender.address.name + " " + address_sender.address.surname)

    def test_pricing_self(self):
        envelope = EnvelopePricing.objects.get(pk=1)
        pack = PackPricing.objects.get(pk=1)
        pallet = PalletPricing.objects.get(pk=1)

        self.assertTrue(isinstance(envelope, EnvelopePricing))
        self.assertTrue(isinstance(pack, PackPricing))
        self.assertTrue(isinstance(pallet, PalletPricing))

        self.assertEqual(envelope.__str__(), envelope.courier.__str__())
        self.assertEqual(pack.__str__(), pack.courier.__str__())
        self.assertEqual(pallet.__str__(), pallet.courier.__str__())


class FormsTest(TestCase):
    def test_parcel_size_valid_form(self):
        data = {'type': 'koperta', 'weight': 0.5, 'length': 1, 'width': 1, 'height': 1}
        form = FormParcelSize(data=data)
        self.assertTrue(form.is_valid())

    def test_parcel_size_invalid_form(self):
        data = {'type': 'koperta', 'weight': -1, 'length': 1, 'width': 1, 'height': 1}
        form = FormParcelSize(data=data)
        self.assertFalse(form.is_valid())

    def test_contact_form_valid_form(self):
        data = {'name': 'John', 'email': 'moj@email.com',
                'message': 'Hey guys i just wanted to tell you its just a test.'}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_form(self):
        data = {'name': 'John', 'message': 'Hey guys i just wanted to tell you its just a test.'}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())


class UrlsTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='Tester', password='for_test')

    def test_index_view(self):
        response = self.client.get(reverse('order:index'))
        self.assertEqual(200, response.status_code)

    def test_pricing_view(self):
        response = self.client.get(reverse('order:pricing'))
        self.assertEqual(200, response.status_code)

    def test_calculate_view(self):
        response = self.client.get(reverse('order:calculate'))
        self.assertEqual(200, response.status_code)

    def test_login_view_anon(self):
        response = self.client.get(reverse('order:login'))
        self.assertEqual(200, response.status_code)

    def test_login_view_logged_in(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get('/login/', follow=True)
        # print(response.request['PATH_INFO'])
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('order:index'))

    def test_sign_up_view_anon(self):
        response = self.client.get(reverse('order:signup'))
        self.assertEqual(200, response.status_code)

    def test_sign_up_view_logged_in(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get('/signup/', follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('order:index'))

    def test_logout_user(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get('/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('order:index'))

    def test_courier_view(self):
        response = self.client.get(reverse('order:courier'))
        self.assertEqual(200, response.status_code)

    def test_profile_view_anon(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:profile'))
        self.assertEqual(200, response.status_code)

    def test_profile_address_view_anon(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:profile_address'))
        self.assertEqual(200, response.status_code)

    def test_orders_view(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:orders'))
        self.assertEqual(200, response.status_code)

    def test_made_up_page(self):
        response = self.client.get('/order/made_up_url.html')
        self.assertEqual(404, response.status_code)


# class IndexViewTest(TestCase):
#     def choose_pricing_test(self):
#         response = self.client.get(reverse('order:index'))

