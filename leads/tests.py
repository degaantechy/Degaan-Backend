from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Lead


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class LeadApiTests(APITestCase):
    def test_public_contact_form_creates_lead_and_sends_emails(self):
        response = self.client.post(
            '/api/leads/',
            {
                'name': 'Test Client',
                'email': 'client@example.com',
                'phone': '+252630000000',
                'interest_type': 'construction',
                'message': 'Please contact me.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_anonymous_user_cannot_list_leads(self):
        response = self.client.get('/api/leads/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

