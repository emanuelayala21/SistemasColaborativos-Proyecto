from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Viaje
from .serializers import ViajeSerializer

class ViajeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ViajeSerializer

    def get_queryset(self):
        # Obtener solo los viajes creados por el usuario autenticado
        return Viaje.objects.filter(cedula_creador=self.request.user).order_by('id')

    def perform_create(self, serializer):
        print(f"Request recibido: {self.request}")
        # Obtener el usuario autenticado que realiza la acción
        user = self.request.user
        if not user:
            print(f"Error: No se encontró un usuario autenticado.")
            raise serializers.ValidationError({"detail": "No se pudo determinar el usuario actual."})
        # Asignar el usuario como creador del viaje
        print(f"Usuario asignado: {user}")
        serializer.save(cedula_creador=user)