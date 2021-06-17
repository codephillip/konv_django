from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import ProductSerializer

from .factories import (
    CategoryFactory,
    OrderItemFactory,
    ProductFactory,
    ProductWithForeignFactory,
    ShopFactory,
    StockFactory,
)


class ProductSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.product = ProductWithForeignFactory.create()

    def test_that_a_product_is_correctly_serialized(self):
        product = self.product
        serializer = ProductSerializer
        serialized_product = serializer(product).data

        assert serialized_product['id'] == product.id
        assert serialized_product['name'] == product.name
        assert serialized_product['expiry_date'] == product.expiry_date
        assert serialized_product['weight'] == product.weight
        assert serialized_product['image'] == product.image
        assert serialized_product['discount'] == product.discount
        assert serialized_product['description'] == product.description
        assert serialized_product['color'] == product.color
        assert serialized_product['price'] == product.price

        assert len(serialized_product['stocks']) == product.stocks.count()

        assert len(serialized_product['orderitems']) == product.orderitems.count()
