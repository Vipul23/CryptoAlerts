# Generated by Django 5.0.7 on 2024-07-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertservice', '0005_remove_alert_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='status',
            field=models.CharField(default='N', max_length=100),
        ),
    ]
