from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import UserSerializer

from .factories import (
    DeliverySpeedFactory,
    LocationFactory,
    OrderFactory,
    PaymentFactory,
    UserFactory,
    UserWithForeignFactory,
)


class UserSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserWithForeignFactory.create()

    def test_that_a_user_is_correctly_serialized(self):
        user = self.user
        serializer = UserSerializer
        serialized_user = serializer(user).data

        assert serialized_user['id'] == user.id
        assert serialized_user['dob'] == user.dob
        assert serialized_user['verified'] == user.verified
        assert serialized_user['phone'] == user.phone
        assert serialized_user['role'] == user.role

        assert len(serialized_user['payments']) == user.payments.count()

        assert len(serialized_user['orders']) == user.orders.count()
