import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Order
from .factories import (
    DeliverySpeedFactory,
    LocationFactory,
    OrderFactory,
    PaymentFactory,
    UserFactory,
)

faker = Factory.create()


class Order_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        OrderFactory.create_batch(size=3)
        self.driver = UserFactory.create()
        self.location = LocationFactory.create()
        self.deliveryspeed = DeliverySpeedFactory.create()

    def test_create_order(self):
        """
        Ensure we can create a new order object.
        """
        client = self.api_client
        order_count = Order.objects.count()
        order_dict = factory.build(dict, FACTORY_CLASS=OrderFactory, driver=self.driver.id,
                                   location=self.location.id, deliveryspeed=self.deliveryspeed.id)
        response = client.post(reverse('order-list'), order_dict)
        created_order_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == order_count + 1
        order = Order.objects.get(pk=created_order_pk)

        assert order_dict['created_at'] == order.created_at.isoformat()
        assert order_dict['status'] == order.status
        assert order_dict['valid'] == order.valid
        assert order_dict['delivery_method'] == order.delivery_method
        assert order_dict['expected_delivery_date_time'] == order.expected_delivery_date_time.isoformat()
        assert order_dict['delivery_date_time'] == order.delivery_date_time.isoformat()
        assert order_dict['total_amount'] == order.total_amount

    def test_get_one(self):
        client = self.api_client
        order_pk = Order.objects.first().pk
        order_detail_url = reverse('order-detail', kwargs={'pk': order_pk})
        response = client.get(order_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('order-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Order.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        order_qs = Order.objects.all()
        order_count = Order.objects.count()

        for i, order in enumerate(order_qs, start=1):
            response = client.delete(reverse('order-detail', kwargs={'pk': order.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert order_count - i == Order.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        order_pk = Order.objects.first().pk
        order_detail_url = reverse('order-detail', kwargs={'pk': order_pk})
        order_dict = factory.build(dict, FACTORY_CLASS=OrderFactory, driver=self.driver.id,
                                   location=self.location.id, deliveryspeed=self.deliveryspeed.id)
        response = client.patch(order_detail_url, data=order_dict)
        assert response.status_code == status.HTTP_200_OK

        assert order_dict['created_at'] == response.data['created_at'].replace('Z', '+00:00')
        assert order_dict['status'] == response.data['status']
        assert order_dict['valid'] == response.data['valid']
        assert order_dict['delivery_method'] == response.data['delivery_method']
        assert order_dict['expected_delivery_date_time'] == response.data['expected_delivery_date_time'].replace(
            'Z', '+00:00')
        assert order_dict['delivery_date_time'] == response.data['delivery_date_time'].replace(
            'Z', '+00:00')
        assert order_dict['total_amount'] == response.data['total_amount']

    def test_update_created_at_with_incorrect_value_data_type(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_created_at = order.created_at
        data = {
            'created_at': faker.pystr(),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_created_at == Order.objects.first().created_at

    def test_update_valid_with_incorrect_value_data_type(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_valid = order.valid
        data = {
            'valid': faker.pystr(),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_valid == Order.objects.first().valid

    def test_update_expected_delivery_date_time_with_incorrect_value_data_type(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_expected_delivery_date_time = order.expected_delivery_date_time
        data = {
            'expected_delivery_date_time': faker.pystr(),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_expected_delivery_date_time == Order.objects.first().expected_delivery_date_time

    def test_update_delivery_date_time_with_incorrect_value_data_type(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_delivery_date_time = order.delivery_date_time
        data = {
            'delivery_date_time': faker.pystr(),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_delivery_date_time == Order.objects.first().delivery_date_time

    def test_update_total_amount_with_incorrect_value_data_type(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_total_amount = order.total_amount
        data = {
            'total_amount': faker.pystr(),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_total_amount == Order.objects.first().total_amount

    def test_update_status_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_status = order.status
        data = {
            'status': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_status == Order.objects.first().status

    def test_update_delivery_method_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        order = Order.objects.first()
        order_detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        order_delivery_method = order.delivery_method
        data = {
            'delivery_method': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(order_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert order_delivery_method == Order.objects.first().delivery_method
