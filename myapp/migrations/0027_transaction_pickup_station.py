# Generated by Django 5.1.2 on 2025-03-01 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_seller_followers_seller_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='pickup_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.pickupstation'),
        ),
    ]
