# Generated by Django 4.1.6 on 2023-02-08 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0002_remove_group_pets"),
        ("pets", "0002_rename_weigth_pet_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pets",
                to="groups.group",
            ),
        ),
    ]
