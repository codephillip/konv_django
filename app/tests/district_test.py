import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import District
from .factories import DistrictFactory, LocationFactory

faker = Factory.create()


class District_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        DistrictFactory.create_batch(size=3)

    def test_create_district(self):
        """
        Ensure we can create a new district object.
        """
        client = self.api_client
        district_count = District.objects.count()
        district_dict = factory.build(dict, FACTORY_CLASS=DistrictFactory)
        response = client.post(reverse('district-list'), district_dict)
        created_district_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert District.objects.count() == district_count + 1
        district = District.objects.get(pk=created_district_pk)

        assert district_dict['name'] == district.name

    def test_get_one(self):
        client = self.api_client
        district_pk = District.objects.first().pk
        district_detail_url = reverse('district-detail', kwargs={'pk': district_pk})
        response = client.get(district_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('district-list'))
        assert response.status_code == status.HTTP_200_OK
        assert District.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        district_qs = District.objects.all()
        district_count = District.objects.count()

        for i, district in enumerate(district_qs, start=1):
            response = client.delete(reverse('district-detail', kwargs={'pk': district.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert district_count - i == District.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        district_pk = District.objects.first().pk
        district_detail_url = reverse('district-detail', kwargs={'pk': district_pk})
        district_dict = factory.build(dict, FACTORY_CLASS=DistrictFactory)
        response = client.patch(district_detail_url, data=district_dict)
        assert response.status_code == status.HTTP_200_OK

        assert district_dict['name'] == response.data['name']

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        district = District.objects.first()
        district_detail_url = reverse('district-detail', kwargs={'pk': district.pk})
        district_name = district.name
        data = {
            'name': faker.pystr(min_chars=51, max_chars=51),
        }
        response = client.patch(district_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert district_name == District.objects.first().name
