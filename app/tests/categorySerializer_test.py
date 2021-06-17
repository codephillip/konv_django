from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import CategorySerializer

from .factories import (
    CategoryFactory,
    CategoryWithForeignFactory,
    ProductFactory,
    ShopFactory,
)


class CategorySerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = CategoryWithForeignFactory.create()

    def test_that_a_category_is_correctly_serialized(self):
        category = self.category
        serializer = CategorySerializer
        serialized_category = serializer(category).data

        assert serialized_category['id'] == category.id
        assert serialized_category['name'] == category.name
        assert serialized_category['description'] == category.description
        assert serialized_category['image'] == category.image

        assert len(serialized_category['products']) == category.products.count()
