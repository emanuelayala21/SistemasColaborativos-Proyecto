from django.shortcuts import render, get_object_or_404
from django.db import models
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Viaje, Participante_Viaje, Nota_Importante
from .serializers import ViajeSerializer, ParticipanteSerializer, NotaImportanteSerializer

# ---------------- VISTAS HTML ----------------

def vista_dashboard(request):
    return render(request, 'trips/index.html')

def vista_viajes(request):
    return render(request, 'trips/Gestion_viajes.html')

def viaje_muro(request):
    return render(request, 'trips/viaje.html')

# --------------- VISTAS API: VIAJES ----------------

class ViajeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ViajeSerializer

    def get_queryset(self):
        return Viaje.objects.filter(
            models.Q(cedula_creador=self.request.user) | 
            models.Q(participante_viaje__usuario=self.request.user)
        ).distinct().order_by('id')

    def get_object(self):
        viaje_id = self.kwargs['pk']
        user = self.request.user
        try:
            return Viaje.objects.get(
                models.Q(id=viaje_id) & (
                    models.Q(cedula_creador=user) | 
                    models.Q(participante_viaje__usuario=user)
                )
            )
        except Viaje.DoesNotExist:
            raise NotFound("No tienes acceso a este viaje.")

    def perform_create(self, serializer):
        user = self.request.user
        if not user:
            raise serializers.ValidationError({"detail": "No se pudo determinar el usuario actual."})
        serializer.save(cedula_creador=user)

    def perform_update(self, serializer):
        viaje = self.get_object()
        if viaje.cedula_creador != self.request.user:
            raise PermissionDenied("No tienes permiso para modificar este viaje.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.cedula_creador != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este viaje.")
        instance.delete()

class ListarViajesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViajeSerializer

    def get_queryset(self):
        return Viaje.objects.filter(cedula_creador=self.request.user).order_by('id')

class ListarViajesParticipanteView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViajeSerializer

    def get_queryset(self):
        return Viaje.objects.filter(participante_viaje__usuario=self.request.user).distinct().order_by('id')

# ------------- VISTAS API: PARTICIPANTES ---------------

class ParticipantesViajeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, viaje_id):
        participantes = Participante_Viaje.objects.filter(viaje_id=viaje_id).select_related('usuario')
        serializer = ParticipanteSerializer(participantes, many=True)
        return Response(serializer.data)

# ------------- VISTAS API: NOTAS IMPORTANTES ------------

class NotasImportantesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, viaje_id):
        notas = Nota_Importante.objects.filter(viaje__id=viaje_id).order_by('fecha_creacion')
        serializer = NotaImportanteSerializer(notas, many=True)
        return Response(serializer.data)
    
# ------------- VISTA API: UNIRSE A UN VIAJE --------------

class UnirseAViajeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        codigo = request.data.get('codigo')
        usuario = request.user

        if not codigo:
            return Response({'detail': 'Código requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        viaje = get_object_or_404(Viaje, codigo_=codigo)

        if Participante_Viaje.objects.filter(usuario=usuario, viaje=viaje).exists():
            return Response({'detail': 'Ya estás unido a este viaje.'}, status=status.HTTP_400_BAD_REQUEST)

        Participante_Viaje.objects.create(usuario=usuario, viaje=viaje)
        return Response({'detail': 'Te has unido correctamente al viaje.'}, status=status.HTTP_200_OK)
