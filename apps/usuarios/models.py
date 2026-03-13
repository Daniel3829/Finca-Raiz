from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.inmuebles.models import Inmueble


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    es_agente = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=True)
    estado = models.CharField(
        max_length=20,
        default="disponible"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email