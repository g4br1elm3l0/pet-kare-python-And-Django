from django.db import models


class Escolhas(models.TextChoices):
    Female = "Female"
    Male = "Male"
    Default = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices=Escolhas.choices,
        default=Escolhas.Default,
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets", null=True
    )

    traits = models.ManyToManyField("traits.Trait", related_name="pets")


# Create your models here.
