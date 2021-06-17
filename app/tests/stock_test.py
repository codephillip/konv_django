import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Stock
from .factories import ProductFactory, StockFactory

faker = Factory.create()


class Stock_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        StockFactory.create_batch(size=3)
        self.product = ProductFactory.create()

    def test_create_stock(self):
        """
        Ensure we can create a new stock object.
        """
        client = self.api_client
        stock_count = Stock.objects.count()
        stock_dict = factory.build(dict, FACTORY_CLASS=StockFactory, product=self.product.id)
        response = client.post(reverse('stock-list'), stock_dict)
        created_stock_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Stock.objects.count() == stock_count + 1
        stock = Stock.objects.get(pk=created_stock_pk)

        assert stock_dict['units_in_stock'] == stock.units_in_stock
        assert stock_dict['units_on_order'] == stock.units_on_order
        assert stock_dict['created_at'] == stock.created_at.isoformat()
        assert stock_dict['name'] == stock.name

    def test_get_one(self):
        client = self.api_client
        stock_pk = Stock.objects.first().pk
        stock_detail_url = reverse('stock-detail', kwargs={'pk': stock_pk})
        response = client.get(stock_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('stock-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Stock.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        stock_qs = Stock.objects.all()
        stock_count = Stock.objects.count()

        for i, stock in enumerate(stock_qs, start=1):
            response = client.delete(reverse('stock-detail', kwargs={'pk': stock.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert stock_count - i == Stock.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        stock_pk = Stock.objects.first().pk
        stock_detail_url = reverse('stock-detail', kwargs={'pk': stock_pk})
        stock_dict = factory.build(dict, FACTORY_CLASS=StockFactory, product=self.product.id)
        response = client.patch(stock_detail_url, data=stock_dict)
        assert response.status_code == status.HTTP_200_OK

        assert stock_dict['units_in_stock'] == response.data['units_in_stock']
        assert stock_dict['units_on_order'] == response.data['units_on_order']
        assert stock_dict['created_at'] == response.data['created_at'].replace('Z', '+00:00')
        assert stock_dict['name'] == response.data['name']

    def test_update_units_in_stock_with_incorrect_value_data_type(self):
        client = self.api_client
        stock = Stock.objects.first()
        stock_detail_url = reverse('stock-detail', kwargs={'pk': stock.pk})
        stock_units_in_stock = stock.units_in_stock
        data = {
            'units_in_stock': faker.pystr(),
        }
        response = client.patch(stock_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert stock_units_in_stock == Stock.objects.first().units_in_stock

    def test_update_units_on_order_with_incorrect_value_data_type(self):
        client = self.api_client
        stock = Stock.objects.first()
        stock_detail_url = reverse('stock-detail', kwargs={'pk': stock.pk})
        stock_units_on_order = stock.units_on_order
        data = {
            'units_on_order': faker.pystr(),
        }
        response = client.patch(stock_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert stock_units_on_order == Stock.objects.first().units_on_order

    def test_update_created_at_with_incorrect_value_data_type(self):
        client = self.api_client
        stock = Stock.objects.first()
        stock_detail_url = reverse('stock-detail', kwargs={'pk': stock.pk})
        stock_created_at = stock.created_at
        data = {
            'created_at': faker.pystr(),
        }
        response = client.patch(stock_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert stock_created_at == Stock.objects.first().created_at

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        stock = Stock.objects.first()
        stock_detail_url = reverse('stock-detail', kwargs={'pk': stock.pk})
        stock_name = stock.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(stock_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert stock_name == Stock.objects.first().name
