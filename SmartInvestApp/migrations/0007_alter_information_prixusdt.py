# Generated by Django 5.0.3 on 2024-03-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartInvestApp', '0006_information_prixusdt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='prixUSDT',
            field=models.FloatField(default=606.37),
        ),
    ]