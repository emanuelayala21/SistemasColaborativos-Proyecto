from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Usuario'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.nombre_usuario
