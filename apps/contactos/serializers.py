from rest_framework import serializers
from .models import Contacto


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = "__all__"
        read_only_fields = ["creado_en"]