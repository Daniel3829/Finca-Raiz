from rest_framework import serializers
from .models import Inmueble


class InmuebleSerializer(serializers.ModelSerializer):
    propietario_nombre = serializers.CharField(
        source="propietario.username",
        read_only=True,
    )

    class Meta:
        model = Inmueble
        fields = "__all__"
        read_only_fields = ["propietario", "creado_en"]