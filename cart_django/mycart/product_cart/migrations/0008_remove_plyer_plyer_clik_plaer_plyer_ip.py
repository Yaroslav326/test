# Generated by Django 5.2 on 2025-05-05 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_cart', '0007_plyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plyer',
            name='plyer',
        ),
        migrations.AddField(
            model_name='clik',
            name='plaer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product_cart.plyer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plyer',
            name='ip',
            field=models.GenericIPAddressField(default='122.11.2'),
            preserve_default=False,
        ),
    ]
