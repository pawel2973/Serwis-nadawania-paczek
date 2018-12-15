from django.test import TestCase
from order.models import Courier


#
class CourierTest(TestCase):
    def setUp(self):
       Courier.objects.create(name='UPC')

    def test_text_content(self):
        courier_object = Courier.objects.get(pk=1)
        expected_object_name = '{}'.format(courier_object.name)
        self.assertEqual(expected_object_name, 'UPC')

