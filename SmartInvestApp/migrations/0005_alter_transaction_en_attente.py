# Generated by Django 5.0.3 on 2024-03-22 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartInvestApp', '0004_transaction_contrat_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='en_attente',
            field=models.BooleanField(default=True),
        ),
    ]
