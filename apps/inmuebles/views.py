from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render
from .models import Inmueble, Contacto
from .serializers import InmuebleSerializer
from django.shortcuts import get_object_or_404
from .filters import InmuebleFilter
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Favorito
from .forms import InmuebleForm
from django.contrib import messages
from .models import InmuebleImagen
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import json


class InmuebleListCreateView(generics.ListCreateAPIView):
    queryset = Inmueble.objects.all().order_by("-id")
    serializer_class = InmuebleSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = InmuebleFilter
    search_fields = ["titulo", "descripcion", "ciudad"]
    ordering_fields = ["precio", "id"]

    def perform_create(self, serializer):
        serializer.save(propietario=self.request.user)
        


class InmuebleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer

def inmuebles_lista_view(request):

    # Base query: Only show available properties
    inmuebles = (
        Inmueble.objects
        .filter(estado="disponible")
        .select_related("propietario")
        .order_by("-id")
    )

    ciudad = request.GET.get("ciudad")
    precio_min = request.GET.get("precio_min")
    precio_max = request.GET.get("precio_max")
    orden = request.GET.get("orden")
    tipo = request.GET.get("tipo")  # NUEVO: Filtro por tipo

    if ciudad:
        inmuebles = inmuebles.filter(ciudad__icontains=ciudad)

    if tipo:
        inmuebles = inmuebles.filter(tipo=tipo)

    if precio_min:
        inmuebles = inmuebles.filter(precio__gte=precio_min)

    if precio_max:
        inmuebles = inmuebles.filter(precio__lte=precio_max)

    if orden == "precio_asc":
        inmuebles = inmuebles.order_by("precio")

    elif orden == "precio_desc":
        inmuebles = inmuebles.order_by("-precio")

    elif orden == "recientes":
        inmuebles = inmuebles.order_by("-id")

    # Obtenemos las ciudades únicas de los inmuebles disponibles
    ciudades_disponibles = (
        Inmueble.objects
        .filter(estado="disponible")
        .values_list("ciudad", flat=True)
        .distinct()
        .order_by("ciudad")
    )

    paginator = Paginator(inmuebles, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "inmuebles/lista.html", {
        "page_obj": page_obj,
        "ciudades_disponibles": ciudades_disponibles
    })

def inmueble_detalle_view(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    return render(request, "inmuebles/detalle.html", {
        "inmueble": inmueble
    })

@login_required
def agregar_favorito(request, inmueble_id):

    inmueble = get_object_or_404(Inmueble, id=inmueble_id)

    Favorito.objects.get_or_create(
        usuario=request.user,
        inmueble=inmueble
    )

    return redirect("detalle_inmueble", pk=inmueble_id)

@login_required
def quitar_favorito(request, inmueble_id):

    Favorito.objects.filter(
        usuario=request.user,
        inmueble_id=inmueble_id
    ).delete()

    return redirect("detalle_inmueble", pk=inmueble_id)

@login_required
def favoritos_view(request):

    favoritos = Favorito.objects.filter(usuario=request.user)

    return render(request, "inmuebles/favoritos.html", {
        "favoritos": favoritos
    })

def contactar_inmueble(request, inmueble_id):

    inmueble = get_object_or_404(Inmueble, id=inmueble_id)

    # Pre-load profile data for logged-in users (for autocomplete)
    datos_perfil = None
    if request.user.is_authenticated:
        u = request.user
        if u.first_name or u.telefono:
            datos_perfil = {
                "nombre": f"{u.first_name} {u.last_name}".strip(),
                "email": u.email,
                "telefono": u.telefono or "",
            }

    if request.method == "POST":
        nombre      = request.POST.get("nombre", "").strip()
        email_c     = request.POST.get("email_contacto", "").strip()
        telefono    = request.POST.get("telefono", "").strip()
        mensaje_txt = request.POST.get("mensaje", "").strip()

        # Save contact record
        Contacto.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            inmueble=inmueble,
            nombre=nombre,
            email_contacto=email_c,
            telefono=telefono,
            mensaje=mensaje_txt,
        )

        # Email notification to the property owner
        propietario = inmueble.propietario
        if propietario.email:
            asunto = f"🏡 Tienes un nuevo interesado: {inmueble.titulo}"
            cuerpo = f"""
Hola {propietario.username},

Tienes un nuevo mensaje de un posible comprador en Tierras no Expropiadas.

📌 Inmueble: {inmueble.titulo} ({inmueble.ciudad})
👤 Nombre: {nombre or 'No especificado'}
📧 Email: {email_c or 'No especificado'}
📱 Teléfono: {telefono or 'No especificado'}
💬 Mensaje:
"{mensaje_txt}"

Ingresa a tu Dashboard para responder directamente.

Saludos,
Equipo de Tierras no Expropiadas
"""
            send_mail(asunto, cuerpo, settings.DEFAULT_FROM_EMAIL, [propietario.email], fail_silently=True)

        messages.success(request, f'¡Tu mensaje ha sido enviado al dueño de {inmueble.titulo}!')
        return redirect("detalle_inmueble", pk=inmueble.id)

    return render(request, "inmuebles/contacto.html", {
        "inmueble": inmueble,
        "datos_perfil": datos_perfil,
    })


def guardar_datos_contacto(request):
    """AJAX endpoint: save/retrieve autocomplete profile data for logged-in users."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "No autenticado"}, status=401)

    if request.method == "POST":
        data = json.loads(request.body)
        u = request.user
        nombre_completo = data.get("nombre", "").strip()
        partes = nombre_completo.split(" ", 1)
        u.first_name = partes[0]
        u.last_name  = partes[1] if len(partes) > 1 else ""
        u.telefono   = data.get("telefono", "").strip()
        u.save(update_fields=["first_name", "last_name", "telefono"])
        return JsonResponse({
            "nombre":   f"{u.first_name} {u.last_name}".strip(),
            "email":    u.email,
            "telefono": u.telefono or "",
        })

    # GET: return current saved profile data
    u = request.user
    tiene_datos = bool(u.first_name or u.telefono)
    return JsonResponse({
        "tiene_datos": tiene_datos,
        "nombre":   f"{u.first_name} {u.last_name}".strip() if tiene_datos else "",
        "email":    u.email,
        "telefono": u.telefono or "",
    })

@login_required
def agregar_inmueble_view(request):

    if request.method == "POST":

        form = InmuebleForm(request.POST, request.FILES)

        if form.is_valid():

            inmueble = form.save(commit=False)
            inmueble.propietario = request.user
            inmueble.save()

            return redirect("detalle_inmueble", pk=inmueble.id)

    else:
        form = InmuebleForm()

    return render(request, "inmuebles/agregar.html", {
        "form": form
    })

@login_required
def subir_imagen_galeria(request):

    if request.method == "POST":

        inmueble_id = request.POST.get("inmueble_id")
        imagenes = request.FILES.getlist("imagenes[]")

        for imagen in imagenes:
            InmuebleImagen.objects.create(
                inmueble_id=inmueble_id,
                imagen=imagen
            )

        return JsonResponse({"mensaje": "imagenes guardadas"})