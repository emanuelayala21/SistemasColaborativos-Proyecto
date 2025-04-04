from .models import Usuario
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    # Usamos contrasena en el formulario, pero internamente se asigna a password
    contrasena = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre_usuario', 'correo', 'contrasena']  # no incluyas 'password'

    def create(self, validated_data):
        password = validated_data.pop('contrasena')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)  # encripta correctamente
        usuario.save()
        return usuario
