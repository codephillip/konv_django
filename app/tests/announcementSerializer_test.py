from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from app.serializers import AnnouncementSerializer

from .factories import AnnouncementFactory


class AnnouncementSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.announcement = AnnouncementFactory.create()

    def test_that_a_announcement_is_correctly_serialized(self):
        announcement = self.announcement
        serializer = AnnouncementSerializer
        serialized_announcement = serializer(announcement).data

        assert serialized_announcement['id'] == announcement.id
        assert serialized_announcement['title'] == announcement.title
        assert serialized_announcement['body'] == announcement.body
        assert serialized_announcement['image'] == announcement.image
