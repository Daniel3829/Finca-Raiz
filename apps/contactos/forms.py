from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=120, required=True)
    correo = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=30, required=False)
    mensaje = forms.CharField(widget=forms.Textarea, required=True)