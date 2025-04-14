from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from _appTrip.models import Viaje, Participante_Viaje
from .models import Notificacion
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@shared_task
def enviar_recordatorios():
    print("Enviando recordatorios de viaje...")
    hoy = timezone.localtime(timezone.now()).date()
    mañana = hoy + timedelta(days=1)

    print(f"[Recordatorios] Hoy es: {hoy}, buscando viajes para mañana: {mañana}")
    viajes = Viaje.objects.filter(fecha_inicio=mañana)
    print(f"[Recordatorios] Viajes encontrados: {viajes.count()}")

    for viaje in viajes:
        print(f"[Recordatorios] Procesando viaje: {viaje.titulo} (ID: {viaje.id})")
        participantes = Participante_Viaje.objects.filter(viaje=viaje)
        print(f"[Recordatorios] Participantes encontrados: {participantes.count()}")
        for p in participantes:
            # Evitar crear notificaciones duplicadas
            ya_existe = Notificacion.objects.filter(
                tipo='recordatorio',
                usuario=p.usuario,
                viaje=viaje
            ).exists()

            if not ya_existe:
                Notificacion.objects.create(
                    tipo='recordatorio',
                    mensaje=f'El viaje "{viaje.titulo}" comienza mañana.',
                    usuario=p.usuario,
                    viaje=viaje
                )
                print(f"[Recordatorios] Notificación creada para {p.usuario}")
            else:
                print(f"[Recordatorios] Ya existe notificación para {p.usuario}")

def create_periodic_task():
    # Ejecutar cada minuto
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Recordatorio de Viajes - cada minuto',
        task='appNotifications.tasks.enviar_recordatorios',
    )