from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notificacion
from .serializers import NotificacionSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

# Notificaciones no leídas
class NotificacionesNoLeidasView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user, leida=False).order_by('-fecha_creada')

# Marcar como leída
class MarcarNotificacionComoLeidaView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            notificacion = Notificacion.objects.get(pk=pk, usuario=request.user)
            notificacion.leida = True
            notificacion.save()
            return Response({"mensaje": "Notificación marcada como leída"})
        except Notificacion.DoesNotExist:
            raise NotFound("No se encontró la notificación")

class VerificarNuevasNotificacionesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tiene_nuevas = Notificacion.objects.filter(usuario=request.user, leida=False).exists()
        return Response({"tiene_nuevas": tiene_nuevas})