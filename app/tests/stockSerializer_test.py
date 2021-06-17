from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import StockSerializer

from .factories import StockFactory


class StockSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.stock = StockFactory.create()

    def test_that_a_stock_is_correctly_serialized(self):
        stock = self.stock
        serializer = StockSerializer
        serialized_stock = serializer(stock).data

        assert serialized_stock['id'] == stock.id
        assert serialized_stock['units_in_stock'] == stock.units_in_stock
        assert serialized_stock['units_on_order'] == stock.units_on_order
        assert serialized_stock['created_at'] == stock.created_at
        assert serialized_stock['name'] == stock.name
