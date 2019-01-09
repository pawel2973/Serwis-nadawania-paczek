from sqlite3 import IntegrityError

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse

from .forms import FormParcelSize
from .models import Courier, EnvelopePricing, Address, RecipientAddress, SenderAddress, PackPricing, PalletPricing, \
    Parcel, Order, Profile, Opinion


# Test for models.py
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

        RecipientAddress.objects.create(address=self.address_object)
        SenderAddress.objects.create(address=self.address_object)

        Parcel.objects.create(length=4, width=4, height=5, weight=2, type='Koperta')
        Parcel.objects.create(length=4, width=4, height=5, weight=2, type='Koperta')

        User.objects.create_user(username='Tester', password='for_test')
        User.objects.create_user(username='Tester2', password='for_test')

        Order.objects.create(profile=Profile.objects.get(pk=1), courier=Courier.objects.get(pk=1),
                             parcel=Parcel.objects.get(pk=1), recipient=RecipientAddress.objects.get(pk=1),
                             sender=SenderAddress.objects.get(pk=1), price=22.5)
        Order.objects.create(profile=Profile.objects.get(pk=2), courier=Courier.objects.get(pk=1),
                             parcel=Parcel.objects.get(pk=2), recipient=RecipientAddress.objects.get(pk=1),
                             sender=SenderAddress.objects.get(pk=1), price=22.5)

        Opinion.objects.create(order=Order.objects.get(pk=1), content='Wszystko poszlo sprawnie 10/10', rating=10)

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
        show_nip = self.address_object.nip
        show_apartment_number = self.address_object.apartment_number
        show_company = self.address_object.company_name

        if show_nip is None:
            show_nip = ""
        else:
            show_nip = " - nip: " + show_nip
        if show_apartment_number is None:
            show_apartment_number = ""
        else:
            show_apartment_number = "/" + str(show_apartment_number)
        if show_company is None:
            show_company = ""
        self.assertEqual(self.address_object.__str__(),
                         str(self.address_object.name) + " " + str(self.address_object.surname) + " | " + str(
                             self.address_object.zip_code) + " " + str(self.address_object.city) + " ul. " + str(
                             self.address_object.street) + " " + str(self.address_object.house_number) +
                         str(show_apartment_number) + " | tel: " + str(
                             self.address_object.telephone_number) + " | " + str(
                             self.address_object.email_address) + " | " + str(show_company) + str(show_nip))

    def test_address_rec_self(self):
        address_recipient = RecipientAddress.objects.get(pk=1)
        self.assertTrue(isinstance(address_recipient, RecipientAddress))
        self.assertEqual(address_recipient.__str__(),
                         address_recipient.address.name + " " + address_recipient.address.surname)

    def test_address_sender_self(self):
        address_sender = SenderAddress.objects.get(pk=1)
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

    def test_parcel_self(self):
        parcel = Parcel.objects.get(pk=1)
        self.assertTrue(isinstance(parcel, Parcel))
        self.assertEqual(parcel.__str__(),
                         parcel.type + " / " + str(parcel.weight) + " kg / " + str(parcel.length) + " x " + str(
                             parcel.weight) + " x " + str(parcel.height) + " cm ")

    def test_profile_self(self):
        profile = Profile.objects.get(pk=1)
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.__str__(), profile.user.__str__())

    def test_order_self(self):
        PACK_STATUS = (
            (0, 'Przygotowane do wysyłki'),
            (1, 'W drodze'),
            (2, 'Dostarczono'),
            (3, 'Anulowano'),
        )
        order = Order.objects.get(pk=1)
        self.assertTrue(isinstance(order, Order))
        self.assertEqual(order.__str__(), "#" + str(order.id) + " | " + str(order.courier) + " | " + str(
            order.parcel) + " | status: " + str(PACK_STATUS[order.status][1]) + " | cena: " + str(order.price) + " zł")

    def test_opinion_self(self):
        opinion = Opinion.objects.get(pk=1)
        self.assertTrue(isinstance(opinion, Opinion))
        self.assertEqual(opinion.__str__(),
                         "Ocena: " + str(opinion.rating) + " | " + str(opinion.order.courier) + "  | Dnia: " + str(
                             opinion.date))

    def test_opinion_view(self):
        url = reverse('order:opinion_create')
        self.client.login(username='Tester', password='for_test')

        # without entering order_id
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)

        # entering opinion with order_id
        order_id = Order.objects.get(pk=1).id
        response = self.client.get(url, {'order_id': order_id})
        self.assertEqual(200, response.status_code)

        # entering opinion with other user order_id
        order_id = Order.objects.get(pk=2).id
        response = self.client.get(url, {'order_id': order_id})
        self.assertEqual(302, response.status_code)

        self.client.logout()
        self.client.login(username='Tester2', password='for_test')

        # entering without post data
        response = self.client.post('/courier-opinion-create/?order_id=2', {})
        self.assertEqual(response.status_code, 200)
        exp_data = {
            'rating': ['To pole jest wymagane.'],
            'content': ['To pole jest wymagane.'],
        }
        self.assertEqual(exp_data, response.context['form'].errors)

        # entering with post data
        req_data = {
            'content': 'Super szybka przesylka!',
            'rating': 10,
        }
        response = self.client.post('/courier-opinion-create/?order_id=2', req_data)
        self.assertRedirects(response,
                             reverse('order:pricing_company', kwargs={'pk': Order.objects.get(pk=order_id).courier_id}))
        # creating when there is opinino for this order
        with transaction.atomic():
            response = self.client.post('/courier-opinion-create/?order_id=2', req_data)
        self.assertEqual('To zamowienie juz ma dodana opinie',response.context['error_unique'])


# tests for forms.py
class FormsTest(TestCase):
    def test_parcel_size_valid_form(self):
        data = {'type': 'koperta', 'weight': 0.5, 'length': 1, 'width': 1, 'height': 1}
        form = FormParcelSize(data=data)
        self.assertTrue(form.is_valid())

    def test_parcel_size_invalid_form(self):
        data = {'type': 'koperta', 'weight': -1, 'length': 1, 'width': 1, 'height': 1}
        form = FormParcelSize(data=data)
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

    def test_choose_courier_view_without_entering_the_data(self):
        response = self.client.get(reverse('order:choose_courier'))
        self.assertEqual(302, response.status_code)

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
        response = self.client.get(reverse('order:choose_courier'))
        self.assertEqual(302, response.status_code)

    def test_profile_view_logged_in(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:profile'))
        self.assertEqual(200, response.status_code)

    # test for anonymously entering profile url
    def test_profile_view_anon(self):
        response = self.client.get(reverse('order:profile'))
        self.assertEqual(302, response.status_code)

    def test_profile_address_create_view_logged_in(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:profile_address_create'))
        self.assertEqual(200, response.status_code)

    # test for anonymously entering editing profile
    def test_profile_address_create_view_anon(self):
        response = self.client.get(reverse('order:profile_address_create'))
        self.assertEqual(302, response.status_code)

    def test_orders_view(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:orders'))
        self.assertEqual(200, response.status_code)

    def test_summary_without_entering_data(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:summary'))
        self.assertEqual(302, response.status_code)

    def test_recipient_without_previous_data_for_order(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:recipient_address'))
        self.assertEqual(302, response.status_code)

    def test_sender_without_previous_data_for_order(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:sender_address'))
        self.assertEqual(302, response.status_code)

    def test_orders_anon(self):
        response = self.client.get(reverse('order:orders'))
        self.assertEqual(302, response.status_code)

    # checking ranking without couriers in database
    def test_ranking_view(self):
        response = self.client.get(reverse('order:ranking'))
        self.assertEqual(200, response.status_code)

    # checking creating opinion without loggin in
    def test_create_opinion_view(self):
        response = self.client.get(reverse('order:opinion_create'))
        self.assertEqual(302, response.status_code)

    # checking creating opinion logged in without having order-id
    def test_create_opinion_logged_in(self):
        self.client.login(username='Tester', password='for_test')
        response = self.client.get(reverse('order:opinion_create'))
        self.assertEqual(302, response.status_code)

    def test_made_up_page(self):
        response = self.client.get('/order/made_up_url.html')
        self.assertEqual(404, response.status_code)
