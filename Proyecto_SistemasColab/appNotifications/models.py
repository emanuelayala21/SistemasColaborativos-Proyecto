from django.db import models
from _appUser.models import Usuario  # Ajusta si tu app se llama distinto
from _appTrip.models import Viaje     # Ajusta si tu app se llama distinto

class Notificacion(models.Model):
    TIPO_CHOICES = (
        ('recordatorio', 'Recordatorio de viaje'),
        ('votacion', 'Votación creada'),
    )

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, null=True, blank=True)
    leida = models.BooleanField(default=False)
    fecha_creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre_usuario} - {self.tipo}"

