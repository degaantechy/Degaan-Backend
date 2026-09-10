from django.db import models

from properties.models import Property


class Lead(models.Model):
    INTEREST_CHOICES = [
        ('buy', 'Buy Property'),
        ('sell', 'Sell Property'),
        ('construction', 'Construction'),
        ('investment', 'Investment'),
        ('development', 'Development / Project Interest'),
        ('valuation', 'Property Valuation'),
        ('landowner', 'Landowner / Joint Development'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interest_type = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True, default='website')

    # Website attribution and qualification fields.
    project_slug = models.CharField(max_length=120, blank=True)
    service = models.CharField(max_length=120, blank=True)
    source_page = models.CharField(max_length=255, blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)
    budget_range = models.CharField(max_length=100, blank=True)
    preferred_contact = models.CharField(max_length=100, blank=True)
    unit_type = models.CharField(max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.name} - {self.interest_type}'
