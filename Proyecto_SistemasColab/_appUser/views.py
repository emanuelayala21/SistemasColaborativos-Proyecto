from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario, RegistroCambioContrasena
from .serializers import UsuarioSerializer

import random
import string
from django.shortcuts import render


User = get_user_model()


# Crear usuario (POST)
@api_view(['POST'])
def crear_usuario(request):
    correo = request.data.get("correo")
    if Usuario.objects.filter(correo=correo).exists():
        return Response({"message": "El correo ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Error en los datos", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Listar todos los usuarios (GET)
@api_view(['GET'])
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Obtener usuario por ID (GET)
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

    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
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


# Login de usuario con JWT
@api_view(['POST'])
def login_usuario(request):
    correo = request.data.get("correo")
    contrasena = request.data.get("contrasena")
    try:
        usuario = Usuario.objects.get(correo=correo)

        if usuario.check_password(contrasena):
            refresh = RefreshToken.for_user(usuario)
            return Response({
                "message": "Inicio de sesión exitoso",
                "usuario": UsuarioSerializer(usuario).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

    except Usuario.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
def mostrar_login(request):
    return render(request, 'users/login.html')

# Recuperar contraseña por correo
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, RegistroCambioContrasena
from django.core.mail import send_mail
import random
import string

@csrf_exempt
def recuperar_contrasena(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            usuario = Usuario.objects.get(correo=correo)

            nueva_contrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            usuario.set_password(nueva_contrasena)
            usuario.save()

            RegistroCambioContrasena.objects.create(
                usuario=usuario.correo,
                nueva_contrasena=nueva_contrasena
            )

            send_mail(
                subject='Recuperación de contraseña',
                message=f'Tu nueva contraseña temporal es: {nueva_contrasena}',
                from_email='halomasterchiefcollection112@gmail.com',
                recipient_list=[correo],
                fail_silently=False,
            )

            from django.contrib import messages
            messages.success(request, 'Se ha enviado una nueva contraseña al correo electrónico.')
            return render(request, 'users/recuperar_contrasena.html')

        except Usuario.DoesNotExist:
            from django.contrib import messages
            messages.error(request, 'El correo no está registrado.')
            return render(request, 'users/recuperar_contrasena.html')

    # Si es GET o si el POST falla, renderiza el formulario
    return render(request, 'users/recuperar_contrasena.html')




# Cambio de contraseña autenticado
@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        nueva = request.POST.get('nueva')
        confirmar = request.POST.get('confirmar')

        if nueva != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            user = request.user
            user.set_password(nueva)
            user.save()
            update_session_auth_hash(request, user)

            RegistroCambioContrasena.objects.create(
                usuario=user.correo,
                nueva_contrasena=nueva,
                fecha_cambio=timezone.now()
            )

            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('login')

    return render(request, 'cambiar_contrasena.html')


# Login clásico (para plantilla HTML)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        try:
            user = Usuario.objects.get(correo=correo)
            user_auth = authenticate(username=user.correo, password=contrasena)

            if user_auth is not None:
                login(request, user_auth)
                return redirect('cambiar_contrasena')
            else:
                messages.error(request, 'Credenciales incorrectas.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario no existe.')

    return render(request, 'users/login.html')

def mostrar_login_html(request):
    return render(request, 'users/login.html')

def mostrar_custom_design(request):
    return render(request, 'users/Custom_Design.html')

def custom_design_view(request):
    return render(request, 'users/Custom_Design.html')

def mostrar_registro_html(request):
    return render(request, 'users/registro.html')