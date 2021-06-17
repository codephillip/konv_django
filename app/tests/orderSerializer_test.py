from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import OrderSerializer

from .factories import (
    DeliverySpeedFactory,
    LocationFactory,
    OrderFactory,
    OrderWithForeignFactory,
    PaymentFactory,
    UserFactory,
)


class OrderSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.order = OrderWithForeignFactory.create()

    def test_that_a_order_is_correctly_serialized(self):
        order = self.order
        serializer = OrderSerializer
        serialized_order = serializer(order).data

        assert serialized_order['id'] == order.id
        assert serialized_order['created_at'] == order.created_at
        assert serialized_order['status'] == order.status
        assert serialized_order['valid'] == order.valid
        assert serialized_order['delivery_method'] == order.delivery_method
        assert serialized_order['expected_delivery_date_time'] == order.expected_delivery_date_time
        assert serialized_order['delivery_date_time'] == order.delivery_date_time
        assert serialized_order['total_amount'] == order.total_amount

        assert len(serialized_order['payments']) == order.payments.count()
