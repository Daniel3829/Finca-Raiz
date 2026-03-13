from django.contrib import admin
from .models import Inmueble, InmuebleImagen, Contacto

class ImagenInline(admin.TabularInline):
    model = InmuebleImagen
    extra = 3

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ("titulo", "precio", "ciudad")
    inlines = [ImagenInline]

@admin.register(InmuebleImagen)
class ImagenInmuebleAdmin(admin.ModelAdmin):
    list_display = ("inmueble", "imagen")

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = ("usuario", "inmueble", "fecha")
    search_fields = ("usuario__email", "inmueble__titulo")
