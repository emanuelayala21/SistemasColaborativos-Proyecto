from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Viaje
from _appUser.models import Usuario
from .serializers import ViajeSerializer

class CrearViajeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Usuario autenticado:", request.user)  # 👈 Agregar esta línea
        print("ID del usuario:", request.user.id)  # 👈 Para ver si tiene un ID válido
        # Obtener el user_id desde el token del usuario autenticado
        user_id = request.user.id  

        # Buscar el Usuario en la base de datos
        try:
            usuario_creador = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Preparar los datos y asignar el creador
        data = request.data.copy()
        data['cedula_creador'] = usuario_creador.id  # Asignamos el usuario autenticado

        # Serializar y guardar el objeto
        serializer = ViajeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(cedula_creador=usuario_creador)  # Guardamos con el usuario asignado
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
