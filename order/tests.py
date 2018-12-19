from django.test import TestCase
from order.forms import MyForm
from order.models import Courier, EnvelopePricing
from django.urls import reverse


#
class CourierTest(TestCase):
    def setUp(self):
       Courier.objects.create(name='UPC')

    def test_courier_content(self):
        courier_object = Courier.objects.get(pk=1)
        expected_object_name = '{}'.format(courier_object.name)
        self.assertEqual(expected_object_name, 'UPC')

    def test_courier_self(self):
        courier_object = Courier.objects.get(pk=1)
        self.assertTrue(isinstance(courier_object,Courier))
        self.assertEqual(courier_object.__str__(), courier_object.name)

class MyFormTest(TestCase):
    def test_valid_form(self):
        data = {'typ_paczki':'koperta', 'waga_paczki':0.5,'dlugosc':1,'szerokosc':1,'wysokosc':1}
        form = MyForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'typ_paczki':'koperta', 'waga_paczki':-1,'dlugosc':1,'szerokosc':1,'wysokosc':1}
        form = MyForm(data=data)
        self.assertFalse(form.is_valid())

class EnvelopePricingTest(TestCase):
    def setUp(self):
        Courier.objects.create(name='UPC')
        courier = Courier.objects.get(pk=1)
        EnvelopePricing.objects.create(courier=courier,up_to_1=1.0)
    def test_envelope_pricing_content(self):
        envelope = EnvelopePricing.objects.get(pk=1)
        expected_price = envelope.up_to_1
        self.assertEqual(expected_price, 1.0)
        
class UrlsTest(TestCase):
    def test_pricing_view(self):
        response = self.client.get(reverse('order:pricing'))
        self.assertEqual(200,response.status_code)
    def test_index_view(self):
        response = self.client.get(reverse('order:index'))
        self.assertEqual(200,response.status_code)
    def test_sign_up_view(self):
        response = self.client.get(reverse('order:signup'))
        self.assertEqual(200,response.status_code)
    def test_made_up_page(self):
        response = self.client.get('/order/made_up_url.html')
        self.assertEqual(404,response.status_code)
