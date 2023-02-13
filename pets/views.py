from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status

from groups.models import Group
from traits.models import Trait

from .models import Pet
from .serializers import PetSerializer


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        trait_param = req.query_params.get("trait")

        if trait_param:
            pets = Pet.objects.filter(traits__name__iexact=trait_param)
        else:
            pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, req)

        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")

        group_obj = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group_data)

        pet_obj = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for trait in traits_data:
            trait_obj = Trait.objects.filter(name__iexact=trait["name"]).first()
            if not trait_obj:
                trait_obj = Trait.objects.create(**trait)

            pet_obj.traits.add(trait_obj)

        serializer = PetSerializer(pet_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# iexact no filter para buscar o nome da model


class PetDetailView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def patch(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)

        if group_data:
            try:
                for key, value in group_data.items():
                    setattr(pet.group, key, value)
                pet.group.save()
            except Pet.group.RelatedObjectDoesNotExist:
                group_obj = Group.objects.create(**group_data, pets=pet)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
