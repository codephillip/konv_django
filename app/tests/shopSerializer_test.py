from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import ShopSerializer

from .factories import (
    CategoryFactory,
    ProductFactory,
    ShopFactory,
    ShopWithForeignFactory,
)


class ShopSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.shop = ShopWithForeignFactory.create()

    def test_that_a_shop_is_correctly_serialized(self):
        shop = self.shop
        serializer = ShopSerializer
        serialized_shop = serializer(shop).data

        assert serialized_shop['id'] == shop.id
        assert serialized_shop['name'] == shop.name
        assert serialized_shop['is_special'] == shop.is_special

        assert len(serialized_shop['products']) == shop.products.count()
