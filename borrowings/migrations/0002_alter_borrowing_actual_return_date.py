# Generated by Django 5.0.1 on 2024-02-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="actual_return_date",
            field=models.DateField(blank=True),
        ),
    ]
