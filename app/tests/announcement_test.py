import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Announcement
from .factories import AnnouncementFactory

faker = Factory.create()


class Announcement_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        AnnouncementFactory.create_batch(size=3)

    def test_create_announcement(self):
        """
        Ensure we can create a new announcement object.
        """
        client = self.api_client
        announcement_count = Announcement.objects.count()
        announcement_dict = factory.build(dict, FACTORY_CLASS=AnnouncementFactory)
        response = client.post(reverse('announcement-list'), announcement_dict)
        created_announcement_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Announcement.objects.count() == announcement_count + 1
        announcement = Announcement.objects.get(pk=created_announcement_pk)

        assert announcement_dict['title'] == announcement.title
        assert announcement_dict['body'] == announcement.body
        assert announcement_dict['image'] == announcement.image

    def test_get_one(self):
        client = self.api_client
        announcement_pk = Announcement.objects.first().pk
        announcement_detail_url = reverse('announcement-detail', kwargs={'pk': announcement_pk})
        response = client.get(announcement_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('announcement-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Announcement.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        announcement_qs = Announcement.objects.all()
        announcement_count = Announcement.objects.count()

        for i, announcement in enumerate(announcement_qs, start=1):
            response = client.delete(reverse('announcement-detail', kwargs={'pk': announcement.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert announcement_count - i == Announcement.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        announcement_pk = Announcement.objects.first().pk
        announcement_detail_url = reverse('announcement-detail', kwargs={'pk': announcement_pk})
        announcement_dict = factory.build(dict, FACTORY_CLASS=AnnouncementFactory)
        response = client.patch(announcement_detail_url, data=announcement_dict)
        assert response.status_code == status.HTTP_200_OK

        assert announcement_dict['title'] == response.data['title']
        assert announcement_dict['body'] == response.data['body']
        assert announcement_dict['image'] == response.data['image']

    def test_update_title_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        announcement = Announcement.objects.first()
        announcement_detail_url = reverse('announcement-detail', kwargs={'pk': announcement.pk})
        announcement_title = announcement.title
        data = {
            'title': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(announcement_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert announcement_title == Announcement.objects.first().title

    def test_update_body_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        announcement = Announcement.objects.first()
        announcement_detail_url = reverse('announcement-detail', kwargs={'pk': announcement.pk})
        announcement_body = announcement.body
        data = {
            'body': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(announcement_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert announcement_body == Announcement.objects.first().body

    def test_update_image_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        announcement = Announcement.objects.first()
        announcement_detail_url = reverse('announcement-detail', kwargs={'pk': announcement.pk})
        announcement_image = announcement.image
        data = {
            'image': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(announcement_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert announcement_image == Announcement.objects.first().image
