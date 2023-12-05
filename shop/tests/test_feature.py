from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, PromoCode


class ShopTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name="Product 1", price=100)
        self.product2 = Product.objects.create(name="Product 2", price=200)
        self.product3 = Product.objects.create(name="Product 3", price=300)
        self.product4 = Product.objects.create(name="Product 4", price=400)
        self.product5 = Product.objects.create(name="Product 5", price=500)

        self.promo_code1 = PromoCode.objects.create(code="PROMO1")
        self.promo_code2 = PromoCode.objects.create(code="PROMO2")

        self.product1.promo_codes.add(self.promo_code1)
        self.product2.promo_codes.add(self.promo_code1)
        self.product3.promo_codes.add(self.promo_code2)

    def test_apply_promo_code_single_product(self):
        client = Client()
        response = client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')
        self.assertContains(response, 'Product 4')
        self.assertContains(response, 'Product 5')
        self.assertNotContains(response, 'Product 3')

    def test_apply_promo_code_multiple_products(self):
        client = Client()
        response = client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO2'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Product 1')
        self.assertNotContains(response, 'Product 2')
        self.assertContains(response, 'Product 3')
        self.assertContains(response, 'Product 4')
        self.assertContains(response, 'Product 5')

    def test_apply_invalid_promo_code(self):
        client = Client()
        response = client.post(reverse('apply_promo_code'), {'promo_code': 'INVALID'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid promo code')
        self.assertNotContains(response, 'Product 1')
        self.assertNotContains(response, 'Product 2')
        self.assertNotContains(response, 'Product 3')
        self.assertContains(response, 'Product 4')
        self.assertContains(response, 'Product 5')

    def test_apply_second_promo_code_after_first(self):
        client = Client()
        client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO1'})
        response = client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO2'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Product 1')
        self.assertNotContains(response, 'Product 2')
        self.assertContains(response, 'Product 3')
        self.assertContains(response, 'Product 4')
        self.assertContains(response, 'Product 5')

    def test_apply_first_promo_code_after_second(self):
        client = Client()
        client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO2'})
        response = client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')
        self.assertNotContains(response, 'Product 3')
        self.assertContains(response, 'Product 4')
        self.assertContains(response, 'Product 5')

    def test_apply_invalid_promo_code_after_valid(self):
        client = Client()
        client.post(reverse('apply_promo_code'), {'promo_code': 'PROMO1'})
        response = client.post(reverse('apply_promo_code'), {'promo_code': 'INVALID'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Product 1')
        self.assertNotContains(response, 'Product 2')
        self.assertNotContains(response, 'Product 3')
        self.assertContains(response, 'Product 4')
        self.assertContains(response, 'Product 5')
