from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .models import Viaje
from .serializers import ViajeSerializer
from django.shortcuts import render

def vista_dashboard(request):
    return render(request, 'trips/index.html')

def vista_viajes(request):
    return render(request, 'trips/Gestion_viajes.html')

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

    def perform_update(self, serializer):
        # Verificar que el usuario autenticado es el creador del viaje antes de permitir la actualización
        viaje = self.get_object()  # Obtener el objeto del viaje que se va a actualizar
        if viaje.cedula_creador != self.request.user:
            raise PermissionDenied("No tienes permiso para modificar este viaje.")
        serializer.save()

    def perform_destroy(self, instance):
        # Verificar que el usuario autenticado es el creador del viaje antes de permitir la eliminación
        if instance.cedula_creador != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este viaje.")
        instance.delete()

class ListarViajesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViajeSerializer

    def get_queryset(self):
        # Obtener solo los viajes creados por el usuario autenticado
        return Viaje.objects.filter(cedula_creador=self.request.user).order_by('id')