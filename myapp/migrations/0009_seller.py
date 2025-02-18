# Generated by Django 5.1.2 on 2025-02-18 11:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_product_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='sellers/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
