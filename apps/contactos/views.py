from django.shortcuts import render, get_object_or_404, redirect
from apps.inmuebles.models import Inmueble
from apps.contactos.models import Contacto
from apps.contactos.forms import ContactoForm
from django.core.mail import send_mail
from django.conf import settings

def contactar_inmueble_view(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    if request.method == "POST":
        form = ContactoForm(request.POST)

        if form.is_valid():
            datos = form.cleaned_data
            user = request.user if request.user.is_authenticated else None

            if user:
                if not datos.get("nombre"):
                    datos["nombre"] = user.username
                if not datos.get("correo"):
                    datos["correo"] = user.email
                if not datos.get("telefono"):
                    datos["telefono"] = getattr(user, "telefono", "")

            contacto = Contacto.objects.create(
                inmueble=inmueble,
                nombre=datos["nombre"],
                correo=datos["correo"],
                telefono=datos["telefono"],
                mensaje=datos["mensaje"],
                user=user if user else None,
            )

            # Envío de correo al propietario
            propietario = inmueble.propietario
            asunto = f"Nuevo interesado en tu inmueble: {inmueble.titulo}"
            mensaje = f"""
Hola {propietario.username},

Tienes un nuevo interesado en tu inmueble.

📌 Inmueble: {inmueble.titulo}
👤 Nombre: {contacto.nombre}
📧 Correo: {contacto.correo}
📱 Teléfono: {contacto.telefono}
💬 Mensaje: {contacto.mensaje}
"""
            if propietario.email:
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [propietario.email],
                    fail_silently=False,
                )

            return redirect("detalle_inmueble", pk=inmueble.id)

    else:
        form = ContactoForm()

    return render(request, "contactos/contactar.html", {"form": form, "inmueble": inmueble})