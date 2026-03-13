from django.db import models
from apps.usuarios.models import Usuario
from apps.inmuebles.models import Inmueble


class Venta(models.Model):

    comprador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="compras",
        null=True,
        blank=True
        
        )

    inmueble = models.ForeignKey(
        Inmueble,
        on_delete=models.CASCADE
    )

    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)

    comision = models.DecimalField(max_digits=12, decimal_places=2)
    
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def calcular_comision(self):

        if self.inmueble.tipo == "apartamento":
            return self.precio_venta * 0.02

        elif self.inmueble.tipo == "casa":
            return self.precio_venta * 0.03

        elif self.inmueble.tipo == "finca":
            return self.precio_venta * 0.04