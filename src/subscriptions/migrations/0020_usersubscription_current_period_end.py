# Generated by Django 5.0.7 on 2024-07-27 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0019_usersubscription_current_period_start_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='current_period_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
