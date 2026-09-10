from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='interest_type',
            field=models.CharField(
                choices=[
                    ('buy', 'Buy Property'),
                    ('sell', 'Sell Property'),
                    ('construction', 'Construction'),
                    ('investment', 'Investment'),
                    ('development', 'Development / Project Interest'),
                    ('valuation', 'Property Valuation'),
                    ('landowner', 'Landowner / Joint Development'),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(model_name='lead', name='project_slug', field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(model_name='lead', name='service', field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(model_name='lead', name='source_page', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='lead', name='utm_source', field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(model_name='lead', name='utm_medium', field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(model_name='lead', name='utm_campaign', field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(model_name='lead', name='budget_range', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='lead', name='preferred_contact', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='lead', name='unit_type', field=models.CharField(blank=True, max_length=100)),
    ]
