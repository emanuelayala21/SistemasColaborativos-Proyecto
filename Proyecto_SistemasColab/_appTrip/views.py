from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .models import Viaje
from .serializers import ViajeSerializer
from django.core.exceptions import PermissionDenied
from .models import Participante_Viaje 
from django.shortcuts import render
from .models import Participante_Viaje
from .serializers import ParticipanteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Nota_Importante
from .serializers import NotaImportanteSerializer 

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
    
class ListarViajesParticipanteView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViajeSerializer

    def get_queryset(self):
        usuario = self.request.user
        # Obtener los viajes donde el usuario participa
        return Viaje.objects.filter(participante_viaje__usuario=usuario).distinct().order_by('id')

def viaje_muro(request):
    return render(request, 'trips/viaje.html')

class ParticipantesViajeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, viaje_id):
        # Usamos select_related para traer el usuario relacionado en una sola consulta
        participantes = Participante_Viaje.objects.filter(viaje_id=viaje_id).select_related('usuario')
        serializer = ParticipanteSerializer(participantes, many=True)
        return Response(serializer.data)
    
    
class NotasImportantesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, viaje_id):
        notas = Nota_Importante.objects.filter(viaje__id=viaje_id).order_by('-fecha_creacion')
        serializer = NotaImportanteSerializer(notas, many=True)
        return Response(serializer.data)