from django.db import models
from _appUser.models import Usuario

class Viaje(models.Model):
    cedula_creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.CharField(max_length=200)
    fecha_creacion = models.DateField()

    class Meta:
        db_table = 'Viaje'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.titulo

class Participante_Viaje(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_union = models.DateField()
    es_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'Participante_Viaje'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return f"{self.usuario.nombre_usuario} - {self.viaje.titulo}"

class Votacion(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Admin que crea la votación
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150)
    fecha_creacion = models.DateField()

    class Meta:
        db_table = 'Votacion'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.titulo

class Opcion_Votacion(models.Model):
    votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE)
    opcion = models.CharField(max_length=100)

    class Meta:
        db_table = 'Opcion_Votacion'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.opcion

class Respuesta_Votacion(models.Model):
    votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion_Votacion, on_delete=models.CASCADE)
    fecha_respuesta = models.DateField()

    class Meta:
        db_table = 'Respuesta_Votacion'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return f"{self.usuario.nombre_usuario} - {self.votacion.titulo}"

class Nota_Importante(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=25)
    contenido = models.CharField(max_length=255)
    fecha_creacion = models.DateField()

    class Meta:
        db_table = 'Nota_Importante'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.titulo
