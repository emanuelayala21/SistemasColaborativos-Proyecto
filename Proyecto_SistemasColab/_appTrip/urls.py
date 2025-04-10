from django.urls import path
from .views import ViajeViewSet, ListarViajesView, vista_dashboard, vista_viajes


urlpatterns = [
    path('crear_viaje/', ViajeViewSet.as_view({'post': 'create'}), name='crear_viaje'),
    path('mis_viajes/', ListarViajesView.as_view(), name='mis_viajes'),
    path('<int:pk>/', ViajeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy', 'put': 'update'}), name='detalle_viaje'),

    # Rutas HTML
    path('dashboard/', vista_dashboard, name='vista_dashboard'),
    path('gestion/', vista_viajes, name='vista_viajes'),
]


