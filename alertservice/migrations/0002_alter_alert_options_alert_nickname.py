# Generated by Django 5.0.7 on 2024-07-27 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alert',
            options={'ordering': ['updated_at']},
        ),
        migrations.AddField(
            model_name='alert',
            name='nickname',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
