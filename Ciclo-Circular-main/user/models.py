from django.db import models

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import BaseUserManager, AbstractUser
class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        email = self.normalize_email(email)
        usuario = self.model(username=username, email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Preferencia(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Mascotas, Viajes, Tecnología
    pregunta = models.CharField(max_length=200) # Ej: ¿Me interesan promociones en viajes?
    icono = models.CharField(max_length=50, default='fa-tag') # Para FontAwesome (Opcional pero recomendado)


    universidad = models.ForeignKey(
            'app.Universidad', # Asegúrate de que apunte a la app correcta
            on_delete=models.CASCADE, 
            related_name='preferencias',
            null=True, # Lo dejamos nulo por ahora para no romper datos viejos
            blank=True
        )
    def __str__(self):
        return self.nombre     


class DescuentoBanco(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Banco Santander, Banco de Chile
    icono = models.CharField(max_length=50, default='fa-building-columns') 
    
    # Lo atamos a la universidad igual que las preferencias
    universidad = models.ForeignKey(
        'app.Universidad', 
        on_delete=models.CASCADE, 
        related_name='descuentos',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} ({self.universidad})"

class Usuario(AbstractUser):
    # Opciones de Género
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decir'),
    ]

    # Campos existentes
    telefono = models.IntegerField(null=True, blank=True)
    id_telegram = models.CharField(max_length=100, null=True, default=0)
    es_coordinador = models.BooleanField(default=False)
    preferencias = models.ManyToManyField(Preferencia, blank=True, related_name='usuarios')
    descuentos = models.ManyToManyField('DescuentoBanco', blank=True, related_name='usuarios_banco')
   
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    comuna = models.CharField(max_length=100, null=True, blank=True, verbose_name="Comuna")
    region = models.CharField(max_length=100,blank=True,verbose_name="Región")
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, null=True, blank=True, verbose_name="Género")
    # ---------------------------------

    universidad_coordinador = models.ForeignKey(
        'app.Universidad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coordinadores'
    )

    carrera = models.ForeignKey(
        'app.Carrera', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Carrera del Estudiante"
    )

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'telefono']

    def __str__(self):
        return self.username



class TrabajoEmpresa(models.Model):
    TIPO_CHOICES = [
        ('Socio', 'Socio / Dueño'),
        ('Trabajo', 'Empleado / Colaborador'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='trabajos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Relación")
    nombre_empresa = models.CharField(max_length=200, verbose_name="Nombre de la Empresa")
    url = models.URLField(max_length=300, blank=True, null=True, verbose_name="URL / Sitio Web")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Email de contacto")
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name="WhatsApp")
    descripcion_breve = models.TextField(max_length=500, verbose_name="Descripción breve")
    
    # Campo generado por la IA de Gemini
    categoria_ia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Categoría (Generada por IA)")

    def __str__(self):
        return f"{self.nombre_empresa} ({self.tipo}) - {self.usuario.username}"  




# 1. El Plan que configura el Administrador
class PlanMembresia(models.Model):
    universidad = models.OneToOneField('app.Universidad', on_delete=models.CASCADE, related_name='plan_membresia')
    valor_anual = models.IntegerField(default=0)
    descripcion = models.TextField(default="Acceso completo a la red de ex alumnos.")

    def __str__(self):
        return f"Plan de {self.universidad.nombre}"

# 2. El registro a prueba de balas para cada usuario
class SuscripcionUsuario(models.Model):
    usuario = models.OneToOneField('user.Usuario', on_delete=models.CASCADE, related_name='suscripcion')
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    @property
    def esta_activa(self):
        # Magia robusta: Comprueba si existe fecha de fin y si el momento actual es menor a esa fecha.
        if not self.fecha_fin:
            return False
        return timezone.now() <= self.fecha_fin

    def renovar_por_un_ano(self):
        self.fecha_inicio = timezone.now()
        # Suma 365 días exactos desde el momento del pago
        self.fecha_fin = self.fecha_inicio + timedelta(days=365)
        self.save()

    def __str__(self):
        return f"Suscripción de {self.usuario.username}"