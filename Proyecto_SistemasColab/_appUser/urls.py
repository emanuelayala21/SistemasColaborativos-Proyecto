from django.urls import path
from .views import crear_usuario, listar_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario, login_usuario,vista_login, vista_registro, enviar_correo_recuperacion, restablecer_contrasena, vista_recuperar, vista_restablecer
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('crear_usuario/', crear_usuario, name='crear_usuario'),  # POST
    path('listar_usuarios/', listar_usuarios, name='listar_usuarios'),  # GET - findAll
    path('obtener_usuario/<int:pk>/', obtener_usuario, name='obtener_usuario'),  # GET - findPK
    path('actualizar_usuario/<int:pk>/', actualizar_usuario, name='actualizar_usuario'),  # PUT
    path('eliminar_usuario/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),  # DELETE
    path('login/', login_usuario, name='login_usuario'),  # <-- Nueva ruta para login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar Token
    path('enviar_correo_recuperacion/', enviar_correo_recuperacion, name='enviar_correo_recuperacion'),
    path('restablecer_contrasena/', restablecer_contrasena, name='restablecer_contrasena'),

    # Rutas HTML
    path('login_page/', vista_login, name='vista_login'),
    path('registro_page/', vista_registro, name='vista_registro'),
    path('recuperar_page/', vista_recuperar, name='vista_recuperar'),
    path('restablecer_page/', vista_restablecer, name='vista_restablecer'),
]

