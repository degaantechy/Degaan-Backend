from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Insight


class InsightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.published = Insight.objects.create(
            title_en='Hargeisa market update',
            title_so='Warbixinta suuqa Hargeysa',
            excerpt_en='A short market summary.',
            excerpt_so='Soo koobid kooban oo suuqa ah.',
            content_en='English article content.',
            content_so='Nuxurka maqaalka Soomaaliga.',
            is_published=True,
            published_at=timezone.now() - timedelta(hours=1),
        )
        Insight.objects.create(
            title_en='Draft insight',
            title_so='Maqaal qabyo ah',
            excerpt_en='Draft summary.',
            excerpt_so='Soo koobid qabyo ah.',
            content_en='Draft content.',
            content_so='Nuxur qabyo ah.',
            is_published=False,
        )

    def test_public_list_only_returns_published_insights(self):
        response = self.client.get('/api/insights/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['slug'], self.published.slug)

    def test_public_can_retrieve_an_insight_by_slug(self):
        response = self.client.get(f'/api/insights/{self.published.slug}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title_en'], self.published.title_en)

    def test_unpublished_insight_is_not_public(self):
        response = self.client.get('/api/insights/draft-insight/')

        self.assertEqual(response.status_code, 404)
