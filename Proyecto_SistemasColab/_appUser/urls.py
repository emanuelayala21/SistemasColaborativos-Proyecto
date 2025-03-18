from django.urls import path
from .views import crear_usuario, listar_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario, login_usuario
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('crear_usuario/', crear_usuario, name='crear_usuario'),  # POST
    path('listar_usuarios/', listar_usuarios, name='listar_usuarios'),  # GET - findAll
    path('obtener_usuario/<int:pk>/', obtener_usuario, name='obtener_usuario'),  # GET - findPK
    path('actualizar_usuario/<int:pk>/', actualizar_usuario, name='actualizar_usuario'),  # PUT
    path('eliminar_usuario/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),  # DELETE
    path('login/', login_usuario, name='login_usuario'),  # <-- Nueva ruta para login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar Token
]

