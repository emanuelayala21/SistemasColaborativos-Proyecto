from django.urls import path
from .views import ViajeViewSet, ListarViajesView


urlpatterns = [
    path('crear_viaje/', ViajeViewSet.as_view({'post': 'create'}), name='crear_viaje'),
    path('mis_viajes/', ListarViajesView.as_view(), name='mis_viajes'),
    path('<int:pk>/', ViajeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy', 'put': 'update'}), name='detalle_viaje'),
]


