import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Location
from .factories import (
    DistrictFactory,
    LocationFactory,
    OrderFactory,
    UserFactory,
)

faker = Factory.create()


class Location_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        LocationFactory.create_batch(size=3)
        self.district = DistrictFactory.create()

    def test_create_location(self):
        """
        Ensure we can create a new location object.
        """
        client = self.api_client
        location_count = Location.objects.count()
        location_dict = factory.build(
            dict, FACTORY_CLASS=LocationFactory, district=self.district.id)
        response = client.post(reverse('location-list'), location_dict)
        created_location_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Location.objects.count() == location_count + 1
        location = Location.objects.get(pk=created_location_pk)

        assert location_dict['lat'] == location.lat
        assert location_dict['lng'] == location.lng

    def test_get_one(self):
        client = self.api_client
        location_pk = Location.objects.first().pk
        location_detail_url = reverse('location-detail', kwargs={'pk': location_pk})
        response = client.get(location_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('location-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Location.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        location_qs = Location.objects.all()
        location_count = Location.objects.count()

        for i, location in enumerate(location_qs, start=1):
            response = client.delete(reverse('location-detail', kwargs={'pk': location.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert location_count - i == Location.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        location_pk = Location.objects.first().pk
        location_detail_url = reverse('location-detail', kwargs={'pk': location_pk})
        location_dict = factory.build(
            dict, FACTORY_CLASS=LocationFactory, district=self.district.id)
        response = client.patch(location_detail_url, data=location_dict)
        assert response.status_code == status.HTTP_200_OK

        assert location_dict['lat'] == response.data['lat']
        assert location_dict['lng'] == response.data['lng']

    def test_update_lat_with_incorrect_value_data_type(self):
        client = self.api_client
        location = Location.objects.first()
        location_detail_url = reverse('location-detail', kwargs={'pk': location.pk})
        location_lat = location.lat
        data = {
            'lat': faker.pystr(),
        }
        response = client.patch(location_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert location_lat == Location.objects.first().lat

    def test_update_lng_with_incorrect_value_data_type(self):
        client = self.api_client
        location = Location.objects.first()
        location_detail_url = reverse('location-detail', kwargs={'pk': location.pk})
        location_lng = location.lng
        data = {
            'lng': faker.pystr(),
        }
        response = client.patch(location_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert location_lng == Location.objects.first().lng
