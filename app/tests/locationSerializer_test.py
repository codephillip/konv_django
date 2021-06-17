from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import LocationSerializer

from .factories import (
    DeliverySpeedFactory,
    DistrictFactory,
    LocationFactory,
    LocationWithForeignFactory,
    OrderFactory,
    UserFactory,
)


class LocationSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.location = LocationWithForeignFactory.create()

    def test_that_a_location_is_correctly_serialized(self):
        location = self.location
        serializer = LocationSerializer
        serialized_location = serializer(location).data

        assert serialized_location['id'] == location.id
        assert serialized_location['lat'] == location.lat
        assert serialized_location['lng'] == location.lng

        assert len(serialized_location['users']) == location.users.count()

        assert len(serialized_location['orders']) == location.orders.count()
