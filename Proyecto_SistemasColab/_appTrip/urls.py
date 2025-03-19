from django.urls import path
from .views import ViajeViewSet


urlpatterns = [
    path('crear_viaje/', ViajeViewSet.as_view({'post': 'create'}), name='crear_viaje'),
]


