import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Category
from .factories import CategoryFactory, ProductFactory

faker = Factory.create()


class Category_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        CategoryFactory.create_batch(size=3)

    def test_create_category(self):
        """
        Ensure we can create a new category object.
        """
        client = self.api_client
        category_count = Category.objects.count()
        category_dict = factory.build(dict, FACTORY_CLASS=CategoryFactory)
        response = client.post(reverse('category-list'), category_dict)
        created_category_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == category_count + 1
        category = Category.objects.get(pk=created_category_pk)

        assert category_dict['name'] == category.name
        assert category_dict['description'] == category.description
        assert category_dict['image'] == category.image

    def test_get_one(self):
        client = self.api_client
        category_pk = Category.objects.first().pk
        category_detail_url = reverse('category-detail', kwargs={'pk': category_pk})
        response = client.get(category_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('category-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Category.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        category_qs = Category.objects.all()
        category_count = Category.objects.count()

        for i, category in enumerate(category_qs, start=1):
            response = client.delete(reverse('category-detail', kwargs={'pk': category.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert category_count - i == Category.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        category_pk = Category.objects.first().pk
        category_detail_url = reverse('category-detail', kwargs={'pk': category_pk})
        category_dict = factory.build(dict, FACTORY_CLASS=CategoryFactory)
        response = client.patch(category_detail_url, data=category_dict)
        assert response.status_code == status.HTTP_200_OK

        assert category_dict['name'] == response.data['name']
        assert category_dict['description'] == response.data['description']
        assert category_dict['image'] == response.data['image']

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        category = Category.objects.first()
        category_detail_url = reverse('category-detail', kwargs={'pk': category.pk})
        category_name = category.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(category_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert category_name == Category.objects.first().name

    def test_update_description_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        category = Category.objects.first()
        category_detail_url = reverse('category-detail', kwargs={'pk': category.pk})
        category_description = category.description
        data = {
            'description': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(category_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert category_description == Category.objects.first().description

    def test_update_image_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        category = Category.objects.first()
        category_detail_url = reverse('category-detail', kwargs={'pk': category.pk})
        category_image = category.image
        data = {
            'image': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(category_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert category_image == Category.objects.first().image
