# Generated by Django 3.0.3 on 2020-03-27 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200327_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='title',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]