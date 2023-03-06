# Generated by Django 3.2 on 2023-03-05 18:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("credit_card", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creditcard",
            name="cvv",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="creditcard",
            name="holder",
            field=models.CharField(
                max_length=200,
                validators=[django.core.validators.MinLengthValidator(2)],
            ),
        ),
    ]
