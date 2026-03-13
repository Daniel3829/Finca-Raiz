from django import forms
from .models import Inmueble
from django import forms
from .models import Inmueble


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

class InmuebleForm(forms.ModelForm):

    class Meta:
        model = Inmueble
        fields = [
            "titulo",
            "descripcion",
            "tipo",
            "precio",
            "ciudad",
            "imagen",
        ]

        widgets = {

            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Apartamento moderno en el centro"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "tipo": forms.Select(attrs={
                "class": "form-select"
            }),

            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: 350000000"
            }),

            "ciudad": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Bogotá"
            }),

            "imagen": forms.FileInput(attrs={
                "class": "form-control"
            }),

        }