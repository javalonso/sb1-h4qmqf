from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Cliente, Medicamento, Receta, MedicamentoReceta, Frecuencia

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'imagen', 'telefono', 'is_active']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'imagen': 'Foto',
            'telefono': 'Teléfono',
            'is_active': 'Activo'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'edad']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Correo electrónico',
            'edad': 'Edad'
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'descripcion']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['cliente', 'notas']
        labels = {
            'cliente': 'Cliente',
            'notas': 'Notas adicionales'
        }

class MedicamentoRecetaForm(forms.ModelForm):
    class Meta:
        model = MedicamentoReceta
        fields = ['medicamento', 'cantidad', 'frecuencia', 'instrucciones']
        labels = {
            'medicamento': 'Medicamento',
            'cantidad': 'Cantidad',
            'frecuencia': 'Frecuencia',
            'instrucciones': 'Instrucciones'
        }

class FrecuenciaForm(forms.ModelForm):
    class Meta:
        model = Frecuencia
        fields = ['nombre', 'intervalo_horas', 'activo']
        labels = {
            'nombre': 'Nombre',
            'intervalo_horas': 'Intervalo en horas',
            'activo': 'Activo'
        }