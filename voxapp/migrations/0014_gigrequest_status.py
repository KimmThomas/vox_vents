# Generated by Django 5.0.6 on 2024-06-15 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voxapp', '0013_rename_pricing_price_alter_price_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='gigrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=20, null=True),
        ),
    ]