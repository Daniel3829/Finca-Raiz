from django.urls import path
from .views import (
    InmuebleListCreateView,
    InmuebleDetailView,
    inmuebles_lista_view,
    inmueble_detalle_view,
    agregar_favorito,
    quitar_favorito,
    favoritos_view,
    contactar_inmueble,
    agregar_inmueble_view,
    subir_imagen_galeria,
    guardar_datos_contacto,
)

urlpatterns = [
    # API
    path("api/", InmuebleListCreateView.as_view(), name="api_inmuebles"),
    path("api/<int:pk>/", InmuebleDetailView.as_view(), name="api_inmueble_detalle"),

    # WEB
    path("lista/", inmuebles_lista_view, name="lista_inmuebles"),
    path("<int:pk>/", inmueble_detalle_view, name="detalle_inmueble"),

    path("favorito/agregar/<int:inmueble_id>/", agregar_favorito, name="agregar_favorito"),
    path("favorito/quitar/<int:inmueble_id>/", quitar_favorito, name="quitar_favorito"),
    path("mis-favoritos/", favoritos_view, name="mis_favoritos"),
    path("contactar/<int:inmueble_id>/", contactar_inmueble, name="contactar_inmueble"),
    path("agregar/", agregar_inmueble_view, name="agregar_inmueble"),
    path("subir-imagen/", subir_imagen_galeria, name="subir_imagen_galeria"),
    path("guardar-datos-contacto/", guardar_datos_contacto, name="guardar_datos_contacto"),
]