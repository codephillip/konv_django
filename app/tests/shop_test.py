import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Shop
from .factories import ProductFactory, ShopFactory

faker = Factory.create()


class Shop_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ShopFactory.create_batch(size=3)

    def test_create_shop(self):
        """
        Ensure we can create a new shop object.
        """
        client = self.api_client
        shop_count = Shop.objects.count()
        shop_dict = factory.build(dict, FACTORY_CLASS=ShopFactory)
        response = client.post(reverse('shop-list'), shop_dict)
        created_shop_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Shop.objects.count() == shop_count + 1
        shop = Shop.objects.get(pk=created_shop_pk)

        assert shop_dict['name'] == shop.name
        assert shop_dict['is_special'] == shop.is_special

    def test_get_one(self):
        client = self.api_client
        shop_pk = Shop.objects.first().pk
        shop_detail_url = reverse('shop-detail', kwargs={'pk': shop_pk})
        response = client.get(shop_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('shop-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Shop.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        shop_qs = Shop.objects.all()
        shop_count = Shop.objects.count()

        for i, shop in enumerate(shop_qs, start=1):
            response = client.delete(reverse('shop-detail', kwargs={'pk': shop.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert shop_count - i == Shop.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        shop_pk = Shop.objects.first().pk
        shop_detail_url = reverse('shop-detail', kwargs={'pk': shop_pk})
        shop_dict = factory.build(dict, FACTORY_CLASS=ShopFactory)
        response = client.patch(shop_detail_url, data=shop_dict)
        assert response.status_code == status.HTTP_200_OK

        assert shop_dict['name'] == response.data['name']
        assert shop_dict['is_special'] == response.data['is_special']

    def test_update_is_special_with_incorrect_value_data_type(self):
        client = self.api_client
        shop = Shop.objects.first()
        shop_detail_url = reverse('shop-detail', kwargs={'pk': shop.pk})
        shop_is_special = shop.is_special
        data = {
            'is_special': faker.pystr(),
        }
        response = client.patch(shop_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert shop_is_special == Shop.objects.first().is_special

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        shop = Shop.objects.first()
        shop_detail_url = reverse('shop-detail', kwargs={'pk': shop.pk})
        shop_name = shop.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(shop_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert shop_name == Shop.objects.first().name
