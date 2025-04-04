from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib import messages
from .models import RegistroCambioContrasena


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
                usuario=user.username,
                nueva_contrasena=nueva,
                fecha_cambio=timezone.now()
            )

            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('login')

    return render(request, 'cambiar_contrasena.html')


def recuperar_contrasena(request):
    mensaje = None  # ✅ Se define al principio para evitar error

    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            usuario = User.objects.get(email=correo)
            contrasena_temporal = get_random_string(length=10)
            usuario.set_password(contrasena_temporal)
            usuario.save()

            RegistroCambioContrasena.objects.create(
                usuario=usuario.username,
                nueva_contrasena=contrasena_temporal,
                fecha_cambio=timezone.now()
            )

            send_mail(
                'Recuperación de Contraseña',
                f'Hola {usuario.username}, tu nueva contraseña temporal es: {contrasena_temporal}',
                'halomasterchiefcollection112@gmail.com',
                [correo],
                fail_silently=False,
            )

            mensaje = 'Se envió una contraseña temporal a tu correo.'
            messages.success(request, mensaje)
            return redirect('login')
        except User.DoesNotExist:
            mensaje = 'El correo ingresado no está registrado.'
            messages.error(request, mensaje)

    return render(request, 'users/recuperar_contrasena.html', {"mensaje": mensaje})


