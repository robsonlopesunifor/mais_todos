# Generated by Django 3.2 on 2023-03-05 21:34

import django.core.validators
import django_cryptography.fields

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("credit_card", "0002_auto_20230305_1843"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creditcard",
            name="brand",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="creditcard",
            name="holder",
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name="creditcard",
            name="number",
            field=django_cryptography.fields.encrypt(models.CharField(max_length=20)),
        ),
    ]
