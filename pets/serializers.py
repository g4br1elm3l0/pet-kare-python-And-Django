from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

from .models import Escolhas


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Escolhas.choices, default=Escolhas.Default)

    traits = TraitSerializer(many=True)
    group = GroupSerializer()
