import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import DeliverySpeed
from .factories import DeliverySpeedFactory, OrderFactory

faker = Factory.create()


class DeliverySpeed_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        DeliverySpeedFactory.create_batch(size=3)

    def test_create_deliverySpeed(self):
        """
        Ensure we can create a new deliverySpeed object.
        """
        client = self.api_client
        deliverySpeed_count = DeliverySpeed.objects.count()
        deliverySpeed_dict = factory.build(dict, FACTORY_CLASS=DeliverySpeedFactory)
        response = client.post(reverse('deliverySpeed-list'), deliverySpeed_dict)
        created_deliverySpeed_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert DeliverySpeed.objects.count() == deliverySpeed_count + 1
        deliverySpeed = DeliverySpeed.objects.get(pk=created_deliverySpeed_pk)

        assert deliverySpeed_dict['type'] == deliverySpeed.type
        assert deliverySpeed_dict['description'] == deliverySpeed.description

    def test_get_one(self):
        client = self.api_client
        deliverySpeed_pk = DeliverySpeed.objects.first().pk
        deliverySpeed_detail_url = reverse('deliverySpeed-detail', kwargs={'pk': deliverySpeed_pk})
        response = client.get(deliverySpeed_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('deliverySpeed-list'))
        assert response.status_code == status.HTTP_200_OK
        assert DeliverySpeed.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        deliverySpeed_qs = DeliverySpeed.objects.all()
        deliverySpeed_count = DeliverySpeed.objects.count()

        for i, deliverySpeed in enumerate(deliverySpeed_qs, start=1):
            response = client.delete(reverse('deliverySpeed-detail',
                                     kwargs={'pk': deliverySpeed.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert deliverySpeed_count - i == DeliverySpeed.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        deliverySpeed_pk = DeliverySpeed.objects.first().pk
        deliverySpeed_detail_url = reverse('deliverySpeed-detail', kwargs={'pk': deliverySpeed_pk})
        deliverySpeed_dict = factory.build(dict, FACTORY_CLASS=DeliverySpeedFactory)
        response = client.patch(deliverySpeed_detail_url, data=deliverySpeed_dict)
        assert response.status_code == status.HTTP_200_OK

        assert deliverySpeed_dict['type'] == response.data['type']
        assert deliverySpeed_dict['description'] == response.data['description']

    def test_update_type_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        deliverySpeed = DeliverySpeed.objects.first()
        deliverySpeed_detail_url = reverse('deliverySpeed-detail', kwargs={'pk': deliverySpeed.pk})
        deliverySpeed_type = deliverySpeed.type
        data = {
            'type': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(deliverySpeed_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert deliverySpeed_type == DeliverySpeed.objects.first().type

    def test_update_description_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        deliverySpeed = DeliverySpeed.objects.first()
        deliverySpeed_detail_url = reverse('deliverySpeed-detail', kwargs={'pk': deliverySpeed.pk})
        deliverySpeed_description = deliverySpeed.description
        data = {
            'description': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(deliverySpeed_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert deliverySpeed_description == DeliverySpeed.objects.first().description
