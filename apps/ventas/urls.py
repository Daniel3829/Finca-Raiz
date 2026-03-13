from django.urls import path
from .views import VentaListView, VentaCreateView

urlpatterns = [
    path("", VentaListView.as_view()),
    path("crear/", VentaCreateView.as_view()),
]