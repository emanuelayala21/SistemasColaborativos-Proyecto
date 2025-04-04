from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager personalizado para el modelo de usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        correo = self.normalize_email(correo)
        usuario = self.model(nombre_usuario=nombre_usuario, correo=correo, **extra_fields)
        usuario.set_password(password)  # Hashea la contraseña
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre_usuario, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nombre_usuario, correo, password, **extra_fields)

# Modelo personalizado de Usuario
class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100, unique=True)
    fecha_creacion = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre_usuario']

    class Meta:
        db_table = 'usuario'  # Nombre exacto de la tabla en MySQL

    def __str__(self):
        return self.nombre_usuario

# Registro de cambios de contraseña
class RegistroCambioContrasena(models.Model):
    usuario = models.CharField(max_length=150)
    nueva_contrasena = models.CharField(max_length=128)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha_cambio.strftime('%Y-%m-%d %H:%M:%S')}"
