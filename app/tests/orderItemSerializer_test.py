from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import OrderItemSerializer

from .factories import OrderItemFactory


class OrderItemSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.orderItem = OrderItemFactory.create()

    def test_that_a_orderItem_is_correctly_serialized(self):
        orderItem = self.orderItem
        serializer = OrderItemSerializer
        serialized_orderItem = serializer(orderItem).data

        assert serialized_orderItem['id'] == orderItem.id
        assert serialized_orderItem['units'] == orderItem.units
        assert serialized_orderItem['valid'] == orderItem.valid
