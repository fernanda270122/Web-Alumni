from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import AdminFormaCreacionUsuario, AdminFormaActualizar

# Registramos el modelo de Usuario personalizado
# usando los formularios que definimos en forms.py

class UsuarioAdmin(UserAdmin):
    # Formularios para agregar y editar usuarios
    add_form = AdminFormaCreacionUsuario
    form = AdminFormaActualizar
    model = Usuario
    
    # Configuración de listas y filtros en el panel admin
    list_display = ['username', 'email', 'telefono', 'is_staff', 'is_active']
    list_filter = ('is_staff', 'is_active')
    
    # Organización de campos al editar
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'telefono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Organización de campos al crear
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2')}
        ),
    )
    
    search_fields = ('email', 'username')
    ordering = ('email',)

# Registrar en el admin
admin.site.register(Usuario, UsuarioAdmin)