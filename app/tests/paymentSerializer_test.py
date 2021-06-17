from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import PaymentSerializer

from .factories import PaymentFactory


class PaymentSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.payment = PaymentFactory.create()

    def test_that_a_payment_is_correctly_serialized(self):
        payment = self.payment
        serializer = PaymentSerializer
        serialized_payment = serializer(payment).data

        assert serialized_payment['id'] == payment.id
        assert serialized_payment['created_at'] == payment.created_at
        assert serialized_payment['paid_at'] == payment.paid_at
        assert serialized_payment['amount'] == payment.amount
        assert serialized_payment['status'] == payment.status
