# eventos/management/commands/recordatorio_diario.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from eventos.models import Evento, Participante # Tus modelos
from tu_proyecto.utils import enviar_correo_asincrono # Reusamos lo de arriba

class Command(BaseCommand):
    help = 'Envía recordatorios a participantes no confirmados'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()
        print("--- Iniciando tarea de recordatorios ---")

        # Lógica de ejemplo (áptala a tus modelos):
        participantes_pendientes = Participante.objects.filter(
            confirmado=False,
            evento__fecha=hoy # O fecha futura
        )

        for p in participantes_pendientes:
            mensaje = f"Hola {p.nombre}, recuerda confirmar tu asistencia."
            # Usamos el envío asíncrono para que el script no tarde años si son muchos
            enviar_correo_asincrono(
                "Recordatorio de Evento",
                mensaje,
                [p.email]
            )
            
        self.stdout.write(self.style.SUCCESS('Recordatorios enviados correctamente'))