from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import DeliverySpeedSerializer

from .factories import (
    DeliverySpeedFactory,
    DeliverySpeedWithForeignFactory,
    LocationFactory,
    OrderFactory,
    UserFactory,
)


class DeliverySpeedSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.deliverySpeed = DeliverySpeedWithForeignFactory.create()

    def test_that_a_deliverySpeed_is_correctly_serialized(self):
        deliverySpeed = self.deliverySpeed
        serializer = DeliverySpeedSerializer
        serialized_deliverySpeed = serializer(deliverySpeed).data

        assert serialized_deliverySpeed['id'] == deliverySpeed.id
        assert serialized_deliverySpeed['type'] == deliverySpeed.type
        assert serialized_deliverySpeed['description'] == deliverySpeed.description

        assert len(serialized_deliverySpeed['orders']) == deliverySpeed.orders.count()
