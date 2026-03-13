from django.db import models
from django.conf import settings
Usuario = settings.AUTH_USER_MODEL


class Inmueble(models.Model):
    TIPOS_INMUEBLE = [
        ("apartamento", "Apartamento"),
        ("casa", "Casa"),
        ("finca", "Finca")
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_INMUEBLE
    )

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_INMUEBLE)
    precio = models.DecimalField(max_digits=13, decimal_places=2)
    ciudad = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="inmuebles/", null=True, blank=True)
    estado = models.CharField(max_length=20, default="disponible")

    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="inmuebles",
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.ciudad}"
    
class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("usuario", "inmueble")
        

class InmuebleImagen(models.Model):

    inmueble = models.ForeignKey(
        Inmueble,
        on_delete=models.CASCADE,
        related_name="imagenes"
    )

    imagen = models.ImageField(upload_to="galeria/")

    def __str__(self):
        return f"Imagen de {self.inmueble.titulo}"
    
class Contacto(models.Model):

    usuario = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    inmueble = models.ForeignKey(
        "inmuebles.Inmueble",
        on_delete=models.CASCADE
    )

    # Contact info (works for both anonymous and logged-in users)
    nombre = models.CharField(max_length=100, blank=True)
    email_contacto = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    mensaje = models.TextField(blank=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nombre_display = self.nombre or (self.usuario.email if self.usuario else "Anónimo")
        return f"{nombre_display} → {self.inmueble}"
    

