from rest_framework import serializers
from .models import Viaje

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = ['id', 'titulo', 'fecha_inicio', 'fecha_fin', 'descripcion', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']  # Estos campos no se deben modificar manualmente
