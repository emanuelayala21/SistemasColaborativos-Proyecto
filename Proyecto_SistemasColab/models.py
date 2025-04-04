from django.db import models

class RegistroCambioContrasena(models.Model):
    usuario = models.CharField(max_length=150)
    nueva_contrasena = models.CharField(max_length=128)  # Hasheada o temporal
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha_cambio.strftime('%Y-%m-%d %H:%M:%S')}"
