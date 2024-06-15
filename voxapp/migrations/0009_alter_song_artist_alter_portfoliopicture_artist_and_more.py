# Generated by Django 5.0.6 on 2024-06-15 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voxapp', '0008_alter_bookingrequest_artist_artistprofile_pricing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='voxapp.profile'),
        ),
        migrations.AlterField(
            model_name='portfoliopicture',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_pictures', to='voxapp.profile'),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voxapp.profile'),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='artist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_info', to='voxapp.profile'),
        ),
        migrations.AlterField(
            model_name='review',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='voxapp.profile'),
        ),
        migrations.AlterField(
            model_name='portfoliovideo',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_videos', to='voxapp.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='class_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='pricing',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Default Pricing'),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.DeleteModel(
            name='ArtistProfile',
        ),
    ]
