# Generated by Django 5.0.1 on 2024-01-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insight',
            name='title',
            field=models.CharField(default=' ', max_length=255),
        ),
    ]
