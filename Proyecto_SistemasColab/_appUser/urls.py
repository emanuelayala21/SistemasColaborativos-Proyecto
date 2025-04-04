from django.urls import path
from django.shortcuts import render

from . import views

from .views import (
    crear_usuario, listar_usuarios, obtener_usuario,
    actualizar_usuario, eliminar_usuario,
    login_usuario, login_view,
    recuperar_contrasena, cambiar_contrasena,
    mostrar_login_html  # ← asegúrate de importar esta correctamente
)

urlpatterns = [
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('listar_usuarios/', listar_usuarios, name='listar_usuarios'),
    path('obtener_usuario/<int:pk>/', obtener_usuario, name='obtener_usuario'),
    path('actualizar_usuario/<int:pk>/', actualizar_usuario, name='actualizar_usuario'),
    path('eliminar_usuario/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),
    
    path('login/', login_usuario, name='login_usuario'),  # API login
    path('login_html/', mostrar_login_html, name='login_html'),  # HTML form

    path('recuperar/', recuperar_contrasena, name='recuperar_contrasena'),
    path('cambiar/', cambiar_contrasena, name='cambiar_contrasena'),
    path('login_form/', login_view, name='login_form'),
    path('custom_design/', views.mostrar_custom_design, name='custom_design'),
    path('custom_design/', views.mostrar_custom_design, name='custom_design'),
    path('custom_design/', views.custom_design_view, name='custom_design'),
    path('registro_html/', views.mostrar_registro_html, name='registro_html'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('registro_html/', views.mostrar_registro_html, name='registro_html'),
    path('custom_design/', views.custom_design_view, name='custom_design'),
    path('login_html/', views.mostrar_login_html, name='login_html'),


]
