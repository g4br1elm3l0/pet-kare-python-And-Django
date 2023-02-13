# Generated by Django 4.1.6 on 2023-02-08 23:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0003_pet_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                choices=[("F", "Female"), ("M", "Male"), ("N", "Not informed")],
                default="Not informed",
                max_length=20,
            ),
        ),
    ]