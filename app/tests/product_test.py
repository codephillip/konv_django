import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Product
from .factories import (
    CategoryFactory,
    OrderItemFactory,
    ProductFactory,
    ShopFactory,
    StockFactory,
)

faker = Factory.create()


class Product_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ProductFactory.create_batch(size=3)
        self.category = CategoryFactory.create()
        self.shop = ShopFactory.create()

    def test_create_product(self):
        """
        Ensure we can create a new product object.
        """
        client = self.api_client
        product_count = Product.objects.count()
        product_dict = factory.build(dict, FACTORY_CLASS=ProductFactory,
                                     category=self.category.id, shop=self.shop.id)
        response = client.post(reverse('product-list'), product_dict)
        created_product_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == product_count + 1
        product = Product.objects.get(pk=created_product_pk)

        assert product_dict['name'] == product.name
        assert product_dict['expiry_date'] == product.expiry_date.isoformat()
        assert product_dict['weight'] == product.weight
        assert product_dict['image'] == product.image
        assert product_dict['discount'] == product.discount
        assert product_dict['description'] == product.description
        assert product_dict['color'] == product.color
        assert product_dict['price'] == product.price

    def test_get_one(self):
        client = self.api_client
        product_pk = Product.objects.first().pk
        product_detail_url = reverse('product-detail', kwargs={'pk': product_pk})
        response = client.get(product_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('product-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Product.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        product_qs = Product.objects.all()
        product_count = Product.objects.count()

        for i, product in enumerate(product_qs, start=1):
            response = client.delete(reverse('product-detail', kwargs={'pk': product.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert product_count - i == Product.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        product_pk = Product.objects.first().pk
        product_detail_url = reverse('product-detail', kwargs={'pk': product_pk})
        product_dict = factory.build(dict, FACTORY_CLASS=ProductFactory,
                                     category=self.category.id, shop=self.shop.id)
        response = client.patch(product_detail_url, data=product_dict)
        assert response.status_code == status.HTTP_200_OK

        assert product_dict['name'] == response.data['name']
        assert product_dict['expiry_date'] == response.data['expiry_date'].replace('Z', '+00:00')
        assert product_dict['weight'] == response.data['weight']
        assert product_dict['image'] == response.data['image']
        assert product_dict['discount'] == response.data['discount']
        assert product_dict['description'] == response.data['description']
        assert product_dict['color'] == response.data['color']
        assert product_dict['price'] == response.data['price']

    def test_update_expiry_date_with_incorrect_value_data_type(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_expiry_date = product.expiry_date
        data = {
            'expiry_date': faker.pystr(),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_expiry_date == Product.objects.first().expiry_date

    def test_update_weight_with_incorrect_value_data_type(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_weight = product.weight
        data = {
            'weight': faker.pystr(),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_weight == Product.objects.first().weight

    def test_update_discount_with_incorrect_value_data_type(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_discount = product.discount
        data = {
            'discount': faker.pystr(),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_discount == Product.objects.first().discount

    def test_update_price_with_incorrect_value_data_type(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_price = product.price
        data = {
            'price': faker.pystr(),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_price == Product.objects.first().price

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_name = product.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_name == Product.objects.first().name

    def test_update_image_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_image = product.image
        data = {
            'image': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_image == Product.objects.first().image

    def test_update_description_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_description = product.description
        data = {
            'description': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_description == Product.objects.first().description

    def test_update_color_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        product = Product.objects.first()
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        product_color = product.color
        data = {
            'color': faker.pystr(min_chars=51, max_chars=51),
        }
        response = client.patch(product_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert product_color == Product.objects.first().color
