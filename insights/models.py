from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Insight(models.Model):
    CATEGORY_CHOICES = [
        ('market', 'Market Insight'),
        ('investment', 'Investment'),
        ('construction', 'Construction'),
        ('guides', 'Property Guide'),
        ('company', 'Company News'),
    ]

    title_en = models.CharField('English title', max_length=255)
    title_so = models.CharField('Somali title', max_length=255)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt_en = models.TextField('English summary', max_length=500)
    excerpt_so = models.TextField('Somali summary', max_length=500)
    content_en = models.TextField(
        'English article',
        help_text='Separate paragraphs with a blank line.',
    )
    content_so = models.TextField(
        'Somali article',
        help_text='Separate paragraphs with a blank line.',
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='market')
    author = models.CharField(max_length=120, default='Degaan Real Estate')
    cover_image_url = models.URLField(
        blank=True,
        help_text='Paste a public HTTPS image URL. Recommended ratio: 16:9.',
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['is_published', '-published_at']),
            models.Index(fields=['category', '-published_at']),
        ]

    def __str__(self):
        return self.title_en

    def _generate_unique_slug(self):
        base_slug = slugify(self.title_en)[:200] or 'insight'
        slug = base_slug
        counter = 2

        while Insight.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            suffix = f'-{counter}'
            slug = f'{base_slug[:220 - len(suffix)]}{suffix}'
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
