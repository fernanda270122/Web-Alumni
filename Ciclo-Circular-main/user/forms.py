from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from app.models import RegistroActividad, Universidad, Carrera
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# --- FORMULARIO DE REGISTRO DE USUARIO ---
class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Ingrese su nombre de usuario', 'id': 'username'}))
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Ingrese su nombre', 'id': 'first_name'}))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Ingrese su apellido', 'id': 'last_name'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Ingrese su correo electrónico', 'id': 'email'}))
    telefono = forms.IntegerField(label='Teléfono', required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Ingrese Telefono', 'id': 'telefono'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Ingrese Contraseña', 'id': 'password'}))

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# --- FORMULARIO DE PERFIL ACADÉMICO ---
class RegistroActividadForm(forms.ModelForm):
    descripcion = forms.CharField(label='Descripción / Rol', widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Ej: Estudiante 4to año',
        'id': 'descripcion'
    }))

    # Campo auxiliar para filtrar (NO se guarda en BD)
    universidad = forms.ModelChoiceField(
        queryset=Universidad.objects.all(),
        label="Seleccione Universidad",
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id': 'select_universidad'})
    )

    # Campo real que se guarda
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.none(), # Inicialmente vacío
        label="Seleccione Carrera",
        widget=forms.Select(attrs={'class': 'form-control mb-3', 'id': 'select_carrera'})
    )

    class Meta:
        model = RegistroActividad
        fields = ['descripcion', 'carrera']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'universidad' in self.data:
            try:
                universidad_id = int(self.data.get('universidad'))
                self.fields['carrera'].queryset = Carrera.objects.filter(
                    departamento__facultad__universidad_id=universidad_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['carrera'].queryset = self.instance.carrera.departamento.facultad.universidad.carrera_set.order_by('nombre')


# --- FORMULARIO PARA ADMIN (CREACIÓN) ---
class AdminFormaCreacionUsuario(UserCreationForm):
    class Meta:
        model = Usuario
        # IMPORTANTE: No incluyas 'password' aquí. 
        # UserCreationForm agrega automáticamente los campos de contraseña segura.
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono')


# --- FORMULARIO PARA ADMIN (ACTUALIZAR) ---
# ESTA ERA LA CLASE QUE FALTABA
class AdminFormaActualizar(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Contraseña",
        help_text="Las contraseñas raw no se guardan en la base de datos, por lo que no puede ver la contraseña de este usuario, pero puede cambiarla usando <a href=\"../password/\">este formulario</a>."
    )

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'telefono', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


# --- TELEGRAM ---
class TelegramForm(forms.ModelForm):
    id_telegram = forms.CharField(label='ID Telegram', widget=forms.TextInput(
        attrs={'placeholder': 'Ingrese su ID de telegram', 'id': 'id_telegram', 'class': 'form-control'}))
    class Meta:
        model = Usuario
        fields = ('id_telegram', )