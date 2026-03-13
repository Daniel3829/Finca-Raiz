from django.db import models
from apps.inmuebles.models import Inmueble


class Contacto(models.Model):
    inmueble = models.ForeignKey(
        Inmueble,
        on_delete=models.CASCADE,
        related_name="contactos",
    )

    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    mensaje = models.TextField(blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interesado en {self.inmueble_id}"