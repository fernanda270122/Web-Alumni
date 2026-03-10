from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib import messages
import random
import string

# Tus modelos y forms
from app.models import Carrera, RegistroActividad, Universidad
from .models import Usuario
from .forms import RegistroActividadForm, UsuarioForm, TelegramForm

# Función auxiliar
def generar_clave(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# --- REGISTRO DE USUARIO ---
def registro(request):
    data = {'form': UsuarioForm()}
    if request.method == 'POST':
        formulario = UsuarioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data["username"], 
                password=formulario.cleaned_data["password"]
            )
            if user:
                login(request, user)
                # Redirige a completar perfil académico
                return redirect(to='agregar_Area', id=user.id)
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

# --- PERFIL ACADÉMICO (Antes AgregarArea) ---
def AgregarArea(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    # 1. BLOQUE AJAX: Responder con lista de carreras cuando el JS lo pida
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action = request.POST.get('action')
        if action == 'buscar_carreras':
            uni_id = request.POST.get('universidad_id')
            data = []
            if uni_id:
                carreras = Carrera.objects.filter(
                    departamento__facultad__universidad_id=uni_id
                ).values('id_carrera', 'nombre').order_by('nombre')
                for c in carreras:
                    data.append({'id': c['id_carrera'], 'nombre': c['nombre']})
            return JsonResponse(data, safe=False)

    # 2. GUARDADO NORMAL
    if request.method == "POST":
        form = RegistroActividadForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = usuario
            registro.save()
            return redirect('home') # O a donde quieras ir después
    else:
        form = RegistroActividadForm()

    return render(request, 'area/agregar_area.html', {'form': form, 'usuario': usuario})

# --- TELEGRAM ---
def agregraIDtelegram(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = TelegramForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TelegramForm(instance=usuario)
    return render(request, 'telegram/agregar_telegram.html', {'form': form})

# --- RESET PASSWORD ---
def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        usuario = Usuario.objects.filter(email=email).first()
        if not usuario:
            messages.error(request, "No existe usuario con ese correo.")
            return redirect('reset_password')

        nueva_clave = generar_clave()
        usuario.set_password(nueva_clave)
        usuario.save()

        try:
            # Nota: Asegúrate de tener configurado el EMAIL_BACKEND en settings
            send_mail(
                "Recuperación de contraseña",
                f"Tu nueva clave es: {nueva_clave}",
                "no-reply@sistema.com",
                [usuario.email],
                fail_silently=False,
            )
            messages.success(request, "Clave enviada al correo.")
            return redirect('login')
        except Exception:
            messages.error(request, "Error enviando correo.")

    return render(request, "registration/reset_password.html")

def registro_usuario(request):
    pass