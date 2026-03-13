import django_filters
from .models import Inmueble

class InmuebleFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name="precio", lookup_expr="gte")
    precio_max = django_filters.NumberFilter(field_name="precio", lookup_expr="lte")
    ciudad = django_filters.CharFilter(lookup_expr="icontains")
    tipo = django_filters.CharFilter(lookup_expr="iexact")
    habitaciones = django_filters.NumberFilter()

    class Meta:
        model = Inmueble
        fields = ["ciudad", "tipo", "habitaciones"]