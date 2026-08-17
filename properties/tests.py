from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, Property


class PropertyApiTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description='A test development',
        )
        self.property = Property.objects.create(
            project=self.project,
            address='Road 1',
            location='Hargeisa',
            price='50000.00',
            size=1800,
            bedrooms=4,
            bathrooms=2,
            property_type='house',
            description='Test property',
        )

    def test_property_list_is_public(self):
        response = self.client.get('/api/properties/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_anonymous_user_cannot_create_property(self):
        response = self.client.post('/api/properties/', {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_property(self):
        admin = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_authenticate(admin)
        response = self.client.post(
            '/api/properties/',
            {
                'address': 'Road 2',
                'location': 'Hargeisa',
                'price': '65000.00',
                'size': 2200,
                'bedrooms': 5,
                'bathrooms': 3,
                'property_type': 'house',
                'description': 'Another property',
                'features': '',
                'images': [],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

