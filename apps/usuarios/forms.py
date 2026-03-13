from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Usuario


class RegistroForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = ["email", "first_name", "last_name"]

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado."
            )

        return email

    def clean_password1(self):

        password = self.cleaned_data.get("password1")

        validate_password(password)

        return password

    def clean(self):

        cleaned_data = super().clean()

        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()

        return user