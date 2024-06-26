# Generated by Django 5.0.6 on 2024-06-13 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voxapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('about_us', models.TextField()),
                ('terms_of_service', models.TextField()),
                ('privacy_policy', models.TextField()),
            ],
        ),
    ]
