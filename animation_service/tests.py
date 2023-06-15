import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Animation


class AnimationTests(TestCase):
    def test_upload_animation(self):
        csv_file_path = os.path.join('animation_service', 'test_data', 'test.csv')
        json_file_path = os.path.join('animation_service', 'test_data', 'test.json')
        with open(csv_file_path, 'rb') as csv_file, open(json_file_path, 'rb') as json_file:
            response = self.client.post(reverse('upload'), {
                'csv_file': SimpleUploadedFile(csv_file.name, csv_file.read()),
                'json_description': SimpleUploadedFile(json_file.name, json_file.read()),
            })
        self.assertEqual(response.status_code, 200)

    def test_view_animation(self):
        animation = Animation.objects.create(animation_id='bb97c684-ad0f-4039-8b82-9c129ea0e257',
                                             animation_path='animation_service/test_data/',
                                             duration=2)
        response = self.client.get(reverse('view', args=[animation.animation_id]))
        self.assertEqual(response.status_code, 200)
