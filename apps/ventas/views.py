from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Venta
from .serializers import VentaSerializer


class VentaListView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAdminUser]


class VentaCreateView(generics.CreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAdminUser]