from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.urls import reverse
from .models import ProductCategory, Product, Purchase


class StoreRegressionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('buyer', password='TestOnly-8381!')
        self.category = ProductCategory.objects.create(title='Books')
        self.product = Product.objects.create(
            title='A book', category=self.category, price='10.00', description='Test'
        )

    def test_public_registration_cannot_assign_privileges(self):
        response = self.client.post(reverse('store:register'), {
            'username': 'visitor', 'password1': 'TestOnly-8381!',
            'password2': 'TestOnly-8381!', 'is_escalated': 'on',
            'is_staff': 'on', 'is_superuser': 'on',
        })
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='visitor')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_purchase_requires_positive_quantity(self):
        self.client.force_login(self.user)
        for quantity in (0, -3):
            response = self.client.post(reverse('store:new_purchase'), {
                'product': self.product.pk, 'quantity': quantity,
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('quantity', response.context['form'].errors)
        self.assertFalse(Purchase.objects.exists())
        response = self.client.post(reverse('store:new_purchase'), {
            'product': self.product.pk, 'quantity': 2,
        })
        self.assertRedirects(response, reverse('store:index'))
        self.assertEqual(Purchase.objects.get().quantity, 2)

    def test_database_rejects_nonpositive_quantity(self):
        for quantity in (0, -1):
            with self.assertRaises(IntegrityError), transaction.atomic():
                Purchase.objects.create(user=self.user, product=self.product, quantity=quantity)

    def test_unknown_category_returns_not_found(self):
        response = self.client.get(reverse('store:product_list', args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_report_filters_return_validation_errors(self):
        for params in ({'start_date': 'invalid'}, {'category_id': 'invalid'},
                       {'start_date': '2024-02-02', 'end_date': '2024-01-01'}):
            response = self.client.get(reverse('store:purchase_report'), params)
            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.context['filter_form'].errors)

    def test_valid_report_filters_still_work(self):
        Purchase.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.get(reverse('store:purchase_report'), {'category_id': self.category.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_revenue'], 20)
