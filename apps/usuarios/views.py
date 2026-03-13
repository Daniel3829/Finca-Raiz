from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework import generics, permissions
from .models import Usuario
from .serializers import UsuarioSerializer, RegistroSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from apps.inmuebles.models import Inmueble, Favorito, Contacto
from .forms import RegistroForm
from django.shortcuts import get_object_or_404
from apps.inmuebles.forms import InmuebleForm
from decimal import Decimal
from django.db.models import Sum


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.inmuebles.models import Inmueble, Favorito, Contacto
from apps.ventas.models import Venta

@login_required
def dashboard(request):

    if request.user.is_superuser:
        return redirect("admin_dashboard")

    usuario = request.user

    inmuebles_publicados = Inmueble.objects.filter(propietario=usuario, estado="disponible").order_by("-id")
    favoritos = Favorito.objects.filter(usuario=usuario).select_related("inmueble")
    contactos = Contacto.objects.filter(inmueble__propietario=usuario).select_related("inmueble", "usuario")

    contexto = {
        "inmuebles": inmuebles_publicados,
        "favoritos": favoritos,
        "contactos": contactos,
        "total_inmuebles": inmuebles_publicados.count(),
        "total_favoritos": favoritos.count(),
        "total_contactos": contactos.count(),
    }

    return render(request, "usuarios/dashboard.html", contexto)


@login_required
def editar_inmueble(request, id):

    inmueble = get_object_or_404(Inmueble, id=id, propietario=request.user)

    if request.method == "POST":

        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)

        if form.is_valid():
            form.save()
            messages.success(request, 'Inmueble actualizado correctamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            
    return redirect("dashboard")

@login_required
def eliminar_inmueble(request, id):

    inmueble = get_object_or_404(Inmueble, id=id, propietario=request.user)

    if request.method == "POST":
        inmueble.delete()
        return redirect("dashboard")

@login_required
def marcar_vendido(request, id):

    inmueble = get_object_or_404(Inmueble, id=id, propietario=request.user)

    porcentajes_comision = {
        "apartamento": Decimal("0.02"),
        "casa": Decimal("0.03"),
        "finca": Decimal("0.04"),
    }
    
    porcentaje = porcentajes_comision.get(inmueble.tipo, Decimal("0.05"))

    comision = inmueble.precio * porcentaje

    if request.method == "POST":

        metodo_pago = request.POST.get("metodo")

        # Save the transaction in the Venta model
        Venta.objects.create(
            inmueble=inmueble,
            precio_venta=inmueble.precio,
            comision=comision,
            metodo_pago=metodo_pago
        )

        inmueble.estado = "vendido"
        inmueble.save()

        messages.success(request, f'¡Pago realizado con éxito mediante {metodo_pago.capitalize()}! El inmueble se ha marcado como vendido.')
        return redirect("dashboard")

    return render(request, "usuarios/pago_comision.html", {
        "inmueble": inmueble,
        "comision": comision,
        "porcentaje": porcentaje * 100
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    todos_inmuebles = Inmueble.objects.all().select_related("propietario").order_by("-creado_en")
    todos_usuarios = Usuario.objects.filter(is_superuser=False).order_by("-date_joined")
    todas_ventas = Venta.objects.all().select_related("inmueble", "comprador").order_by("-fecha")
    total_comisiones = Venta.objects.aggregate(total=Sum("comision"))["total"] or 0

    return render(request, "usuarios/admin_dashboard.html", {
        "todos_inmuebles": todos_inmuebles,
        "todos_usuarios": todos_usuarios,
        "todas_ventas": todas_ventas,
        "total_comisiones": total_comisiones,
        "total_inmuebles": todos_inmuebles.count(),
        "total_usuarios": todos_usuarios.count(),
        "total_ventas": todas_ventas.count(),
    })

@login_required
def eliminar_inmueble_admin(request, id):
    if not request.user.is_superuser:
        return redirect("dashboard")

    inmueble = get_object_or_404(Inmueble, id=id)
    if request.method == "POST":
        inmueble.delete()
        messages.success(request, f'Inmueble "{inmueble.titulo}" eliminado exitosamente.')
    return redirect("admin_dashboard")

class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]




def register(request):

    if request.method == "POST":

        form = RegistroForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("/api/inmuebles/lista/")

    else:

        form = RegistroForm()

    return render(request, "usuarios/register.html", {"form": form})


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LoginSerializer(TokenObtainPairSerializer):
    username_field = Usuario.EMAIL_FIELD

class CustomLoginView(LoginView):

    template_name = "usuarios/login.html"

    def get_success_url(self):

        if self.request.user.is_superuser:
            return "/api/auth/admin-dashboard/"

        return "/api/inmuebles/lista/"