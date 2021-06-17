import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import OrderItem
from .factories import OrderItemFactory, ProductFactory

faker = Factory.create()


class OrderItem_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        OrderItemFactory.create_batch(size=3)
        self.product = ProductFactory.create()

    def test_create_orderItem(self):
        """
        Ensure we can create a new orderItem object.
        """
        client = self.api_client
        orderItem_count = OrderItem.objects.count()
        orderItem_dict = factory.build(
            dict, FACTORY_CLASS=OrderItemFactory, product=self.product.id)
        response = client.post(reverse('orderItem-list'), orderItem_dict)
        created_orderItem_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert OrderItem.objects.count() == orderItem_count + 1
        orderItem = OrderItem.objects.get(pk=created_orderItem_pk)

        assert orderItem_dict['units'] == orderItem.units
        assert orderItem_dict['valid'] == orderItem.valid

    def test_get_one(self):
        client = self.api_client
        orderItem_pk = OrderItem.objects.first().pk
        orderItem_detail_url = reverse('orderItem-detail', kwargs={'pk': orderItem_pk})
        response = client.get(orderItem_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('orderItem-list'))
        assert response.status_code == status.HTTP_200_OK
        assert OrderItem.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        orderItem_qs = OrderItem.objects.all()
        orderItem_count = OrderItem.objects.count()

        for i, orderItem in enumerate(orderItem_qs, start=1):
            response = client.delete(reverse('orderItem-detail', kwargs={'pk': orderItem.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert orderItem_count - i == OrderItem.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        orderItem_pk = OrderItem.objects.first().pk
        orderItem_detail_url = reverse('orderItem-detail', kwargs={'pk': orderItem_pk})
        orderItem_dict = factory.build(
            dict, FACTORY_CLASS=OrderItemFactory, product=self.product.id)
        response = client.patch(orderItem_detail_url, data=orderItem_dict)
        assert response.status_code == status.HTTP_200_OK

        assert orderItem_dict['units'] == response.data['units']
        assert orderItem_dict['valid'] == response.data['valid']

    def test_update_units_with_incorrect_value_data_type(self):
        client = self.api_client
        orderItem = OrderItem.objects.first()
        orderItem_detail_url = reverse('orderItem-detail', kwargs={'pk': orderItem.pk})
        orderItem_units = orderItem.units
        data = {
            'units': faker.pystr(),
        }
        response = client.patch(orderItem_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert orderItem_units == OrderItem.objects.first().units

    def test_update_valid_with_incorrect_value_data_type(self):
        client = self.api_client
        orderItem = OrderItem.objects.first()
        orderItem_detail_url = reverse('orderItem-detail', kwargs={'pk': orderItem.pk})
        orderItem_valid = orderItem.valid
        data = {
            'valid': faker.pystr(),
        }
        response = client.patch(orderItem_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert orderItem_valid == OrderItem.objects.first().valid
