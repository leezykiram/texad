from django.test import TestCase
from light_jets.models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(product_id=9998, description="Testing Jet 1")
        Product.objects.create(product_id=9999, description="Testing Jet 2")

    def test_objects_create(self):
        """Check if data is inserted and saved in the database"""
        jet1 = Product.objects.get(product_id=9998)
        jet2 = Product.objects.get(product_id=9999)
        
        # Retrieve and check the details
        self.assertEqual(jet1.product_id, 9998)
        self.assertEqual(jet2.product_id, 9999)
        self.assertEqual(jet1.description,'Testing Jet 1')
        self.assertEqual(jet2.description,'Testing Jet 2')

    def test_objects_get_or_create(self):
        """Check if data is updated in the database"""
        jet1, created = Product.objects.get_or_create(product_id=9998,
                                                         description="Testing Jet 1")
        # Retrieve and check the details
        self.assertEqual(jet1.product_id, 9998)
        self.assertEqual(jet1.description,'Testing Jet 1')
        self.assertEqual(created,False)

        jet1, created = Product.objects.get_or_create(product_id=9997,
                                                         description="Testing Jet 3")
        # Retrieve and check the details
        self.assertEqual(jet1.product_id, 9997)
        self.assertEqual(jet1.description,'Testing Jet 3')
        self.assertEqual(created,True)

