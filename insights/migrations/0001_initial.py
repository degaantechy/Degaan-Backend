from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Insight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=255, verbose_name='English title')),
                ('title_so', models.CharField(max_length=255, verbose_name='Somali title')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('excerpt_en', models.TextField(max_length=500, verbose_name='English summary')),
                ('excerpt_so', models.TextField(max_length=500, verbose_name='Somali summary')),
                ('content_en', models.TextField(help_text='Separate paragraphs with a blank line.', verbose_name='English article')),
                ('content_so', models.TextField(help_text='Separate paragraphs with a blank line.', verbose_name='Somali article')),
                ('category', models.CharField(choices=[('market', 'Market Insight'), ('investment', 'Investment'), ('construction', 'Construction'), ('guides', 'Property Guide'), ('company', 'Company News')], default='market', max_length=20)),
                ('author', models.CharField(default='Degaan Real Estate', max_length=120)),
                ('cover_image_url', models.URLField(blank=True, help_text='Paste a public HTTPS image URL. Recommended ratio: 16:9.')),
                ('is_featured', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-published_at', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='insight',
            index=models.Index(fields=['is_published', '-published_at'], name='insights_in_is_publ_7098b0_idx'),
        ),
        migrations.AddIndex(
            model_name='insight',
            index=models.Index(fields=['category', '-published_at'], name='insights_in_categor_cf1529_idx'),
        ),
    ]
