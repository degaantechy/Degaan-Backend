from django.db import models
from django.core.validators import MinValueValidator

class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('construction', 'Under Construction'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_estimate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    timeline_start = models.DateField(null=True, blank=True)
    timeline_end = models.DateField(null=True, blank=True)
    units_total = models.IntegerField(default=0)
    units_sold = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    structural_specs = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    progress_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class Property(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('construction', 'Under Construction'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
        ('mixed-use', 'Mixed-Use'),
    ]

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    size = models.IntegerField(help_text="Size in square feet")
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=1)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='apartment')
    description = models.TextField()
    features = models.TextField(blank=True, help_text="Comma-separated features")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    images = models.JSONField(default=list, help_text="List of image URLs")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.address} - {self.property_type}"


class Lead(models.Model):
    INTEREST_CHOICES = [
        ('buy', 'Buy Property'),
        ('sell', 'Sell Property'),
        ('construction', 'Construction'),
        ('investment', 'Investment'),
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
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True, default='website')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.name} - {self.interest_type}"
