from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Sobrescribimos el campo contrasena para encriptarla antes de guardarla
    contrasena = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'correo', 'contrasena']  # Especificamos los campos que queremos manejar

    def create(self, validated_data):
        # Encriptar la contraseña antes de guardar
        contrasena = validated_data.pop('contrasena')  # Eliminar la contraseña de los datos validados
        usuario = Usuario.objects.create(
            **validated_data, 
            contrasena=make_password(contrasena)  # Encriptamos la contraseña antes de guardarla
        )
        return usuario

    def update(self, instance, validated_data):
        # Si se proporciona una nueva contraseña, la encriptamos antes de actualizar
        contrasena = validated_data.pop('contrasena', None)
        if contrasena:
            instance.contrasena = make_password(contrasena)

        # Actualizar otros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance