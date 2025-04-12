from rest_framework import serializers
from .models import Viaje
from .models import Participante_Viaje
from _appUser.models import Usuario
from .models import Nota_Importante

class ViajeSerializer(serializers.ModelSerializer):
    creador_nombre = serializers.CharField(source='cedula_creador.nombre_usuario', read_only=True)

    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'fecha_inicio', 'fecha_fin', 'descripcion', 'fecha_creacion', 'creador_nombre']
        read_only_fields = ['id', 'fecha_creacion']

class ParticipanteSerializer(serializers.ModelSerializer):
    # Accedemos al nombre del usuario directamente, sin hacer una consulta adicional
    usuario_nombre = serializers.CharField(source='usuario.nombre_usuario', read_only=True)

    class Meta:
        model = Participante_Viaje
        fields = ['usuario_nombre']

class NotaImportanteSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre_usuario', read_only=True)

    class Meta:
        model = Nota_Importante
        fields = ['id', 'titulo', 'contenido', 'fecha_creacion', 'usuario_nombre']