from django.urls import path
from .views import CrearViajeView

urlpatterns = [
    path('crear/', CrearViajeView.as_view(), name='crear_viaje'),
]
