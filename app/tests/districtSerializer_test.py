from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import DistrictSerializer

from .factories import (
    DistrictFactory,
    DistrictWithForeignFactory,
    LocationFactory,
)


class DistrictSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.district = DistrictWithForeignFactory.create()

    def test_that_a_district_is_correctly_serialized(self):
        district = self.district
        serializer = DistrictSerializer
        serialized_district = serializer(district).data

        assert serialized_district['id'] == district.id
        assert serialized_district['name'] == district.name

        assert len(serialized_district['locations']) == district.locations.count()
