from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.conf import settings
from app.models import Evento, Invitacion
from datetime import timedelta

class Command(BaseCommand):
    help = 'Envía recordatorios para eventos de mañana a usuarios en estado ENVIADO'

    def handle(self, *args, **kwargs):
        # 1. Calcular "Mañana"
        ahora = timezone.now()
        manana = ahora.date() + timedelta(days=1)
        
        self.stdout.write(f"--- Buscando eventos para: {manana} ---")

        # 2. Filtramos eventos de mañana que NO hayan sido enviados (False)
        eventos_manana = Evento.objects.filter(
            inicio__date=manana, 
            recordatorio_24h_enviado=False
        )

        if not eventos_manana.exists():
            self.stdout.write(self.style.WARNING(f"No hay eventos pendientes para mañana."))
            return

        mensajes_a_enviar = []
        eventos_procesados = 0

        # 3. Recorrer eventos
        for evento in eventos_manana:
            self.stdout.write(f"Procesando: {evento.titulo}")

            # Buscamos usuarios en estado 'ENVIADO'
            pendientes = Invitacion.objects.filter(evento=evento, estado='ENVIADO')
            
            if not pendientes.exists():
                self.stdout.write(f" > '{evento.titulo}' no tiene invitados pendientes.")
                # Marcamos como procesado igual para no volver a revisar mañana
                evento.recordatorio_24h_enviado = True
                evento.save()
                continue

            count_usuarios = 0
            for invitacion in pendientes:
                usuario = invitacion.usuario
                
                asunto = f"🔔 Recordatorio: Mañana es el evento {evento.titulo}"
                cuerpo = (
                    f"Hola {usuario.first_name},\n\n"
                    f"Te recordamos que tienes una invitación pendiente por confirmar:\n\n"
                    f"📌 Evento: {evento.titulo}\n"
                    f"📅 Inicio: {evento.inicio.strftime('%H:%M')}\n"
                    f"📍 Lugar: {evento.lugar}\n\n"
                    f"Por favor ingresa a la plataforma para confirmar o rechazar tu asistencia.\n\n"
                    f"Saludos,\nEquipo Alumni."
                )
                
                mensajes_a_enviar.append((asunto, cuerpo, settings.EMAIL_HOST_USER, [usuario.email]))
                count_usuarios += 1
            
            # ¡IMPORTANTE! Marcamos el evento como enviado aquí
            evento.recordatorio_24h_enviado = True
            evento.save()
            eventos_procesados += 1
            self.stdout.write(f" > Se prepararon {count_usuarios} correos.")

        # 4. Enviar correos
        if mensajes_a_enviar:
            self.stdout.write("Enviando correos masivos...")
            try:
                send_mass_mail(tuple(mensajes_a_enviar), fail_silently=False)
                self.stdout.write(self.style.SUCCESS(f"✅ ÉXITO: Se enviaron {len(mensajes_a_enviar)} correos."))
            except Exception as e:
                # Si falla el SMTP, lo imprimimos. El evento ya quedó marcado como True arriba
                # para evitar bucles infinitos de intentos fallidos.
                self.stdout.write(self.style.ERROR(f"❌ ERROR SMTP: {e}"))
        else:
            self.stdout.write("Proceso terminado. No hubo correos para enviar.")