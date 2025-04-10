from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer
from .models import Usuario
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

def vista_login(request):
    return render(request, 'users/login.html')

def vista_registro(request):
    return render(request, 'users/registro.html')

# Crear usuario (POST) - Ya lo tienes
@api_view(['POST'])
def crear_usuario(request):
    correo = request.data.get("correo")
        
    # Verificar si el correo ya existe
    if Usuario.objects.filter(correo=correo).exists():
        return Response({"message": "El correo ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)


    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Error en los datos", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Listar todos los usuarios (GET) - findAll
@api_view(['GET'])
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Obtener usuario por ID (GET) - findPK
@api_view(['GET'])
def obtener_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(id=pk)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Actualizar usuario (PUT)
@api_view(['PUT'])
def actualizar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(id=pk)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)  # `partial=True` permite actualizar solo algunos campos
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Usuario actualizado correctamente"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Eliminar usuario (DELETE)
@api_view(['DELETE'])
def eliminar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(id=pk)
        usuario.delete()
        return Response({"mensaje": "Usuario eliminado correctamente"}, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login_usuario(request):
    correo = request.data.get("correo")
    contrasena = request.data.get("contrasena")
    try:
        usuario = Usuario.objects.get(correo=correo)

        # Verificar si la contraseña es correcta
        if check_password(contrasena, usuario.contrasena):
            # Generar Token JWT
            refresh = RefreshToken.for_user(usuario)
            return Response({
                "message": "Inicio de sesión exitoso",
                "usuario": UsuarioSerializer(usuario).data,  # Enviar datos del usuario si es necesario
                "access": str(refresh.access_token),  # Token de acceso
                "refresh": str(refresh)  # Token de refresco
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)
    
    except Usuario.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)