import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Payment
from .factories import OrderFactory, PaymentFactory, UserFactory

faker = Factory.create()


class Payment_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        PaymentFactory.create_batch(size=3)
        self.customer = UserFactory.create()
        self.order = OrderFactory.create()

    def test_create_payment(self):
        """
        Ensure we can create a new payment object.
        """
        client = self.api_client
        payment_count = Payment.objects.count()
        payment_dict = factory.build(dict, FACTORY_CLASS=PaymentFactory,
                                     customer=self.customer.id, order=self.order.id)
        response = client.post(reverse('payment-list'), payment_dict)
        created_payment_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Payment.objects.count() == payment_count + 1
        payment = Payment.objects.get(pk=created_payment_pk)

        assert payment_dict['created_at'] == payment.created_at.isoformat()
        assert payment_dict['paid_at'] == payment.paid_at.isoformat()
        assert payment_dict['amount'] == payment.amount
        assert payment_dict['status'] == payment.status

    def test_get_one(self):
        client = self.api_client
        payment_pk = Payment.objects.first().pk
        payment_detail_url = reverse('payment-detail', kwargs={'pk': payment_pk})
        response = client.get(payment_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('payment-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Payment.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        payment_qs = Payment.objects.all()
        payment_count = Payment.objects.count()

        for i, payment in enumerate(payment_qs, start=1):
            response = client.delete(reverse('payment-detail', kwargs={'pk': payment.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert payment_count - i == Payment.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        payment_pk = Payment.objects.first().pk
        payment_detail_url = reverse('payment-detail', kwargs={'pk': payment_pk})
        payment_dict = factory.build(dict, FACTORY_CLASS=PaymentFactory,
                                     customer=self.customer.id, order=self.order.id)
        response = client.patch(payment_detail_url, data=payment_dict)
        assert response.status_code == status.HTTP_200_OK

        assert payment_dict['created_at'] == response.data['created_at'].replace('Z', '+00:00')
        assert payment_dict['paid_at'] == response.data['paid_at'].replace('Z', '+00:00')
        assert payment_dict['amount'] == response.data['amount']
        assert payment_dict['status'] == response.data['status']

    def test_update_created_at_with_incorrect_value_data_type(self):
        client = self.api_client
        payment = Payment.objects.first()
        payment_detail_url = reverse('payment-detail', kwargs={'pk': payment.pk})
        payment_created_at = payment.created_at
        data = {
            'created_at': faker.pystr(),
        }
        response = client.patch(payment_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert payment_created_at == Payment.objects.first().created_at

    def test_update_paid_at_with_incorrect_value_data_type(self):
        client = self.api_client
        payment = Payment.objects.first()
        payment_detail_url = reverse('payment-detail', kwargs={'pk': payment.pk})
        payment_paid_at = payment.paid_at
        data = {
            'paid_at': faker.pystr(),
        }
        response = client.patch(payment_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert payment_paid_at == Payment.objects.first().paid_at

    def test_update_amount_with_incorrect_value_data_type(self):
        client = self.api_client
        payment = Payment.objects.first()
        payment_detail_url = reverse('payment-detail', kwargs={'pk': payment.pk})
        payment_amount = payment.amount
        data = {
            'amount': faker.pystr(),
        }
        response = client.patch(payment_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert payment_amount == Payment.objects.first().amount

    def test_update_status_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        payment = Payment.objects.first()
        payment_detail_url = reverse('payment-detail', kwargs={'pk': payment.pk})
        payment_status = payment.status
        data = {
            'status': faker.pystr(min_chars=51, max_chars=51),
        }
        response = client.patch(payment_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert payment_status == Payment.objects.first().status
