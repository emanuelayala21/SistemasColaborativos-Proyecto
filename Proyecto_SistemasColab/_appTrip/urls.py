from django.urls import path
from .views import (
    ViajeViewSet,     ListarViajesView,    ListarViajesParticipanteView,    ParticipantesViajeView,    NotasImportantesView, UnirseAViajeView,
    CrearNotaImportante,
    vista_dashboard,    vista_viajes,    viaje_muro,
)

urlpatterns = [
    # Rutas API relacionadas con viajes
    path('crear_viaje/', ViajeViewSet.as_view({'post': 'create'}), name='crear_viaje'),
    path('mis_viajes/', ListarViajesView.as_view(), name='mis_viajes'),
    path('incluido/', ListarViajesParticipanteView.as_view(), name='viajes_incluidos'),
    path('<int:pk>/', ViajeViewSet.as_view({'get': 'retrieve','patch': 'partial_update','delete': 'destroy','put': 'update'}), name='detalle_viaje'),
    path('participantes/<int:viaje_id>/', ParticipantesViajeView.as_view(), name='participantes_viaje'),
    path('notas/<int:viaje_id>/', NotasImportantesView.as_view(), name='notas_importantes'),
    path('unirse/', UnirseAViajeView.as_view(), name='unirse_a_viaje'),
    path('notas/<int:viaje_id>/crear/', CrearNotaImportante.as_view(), name='crear_nota_importante'),

    # Rutas para vistas HTML (Frontend)
    path('dashboard/', vista_dashboard, name='vista_dashboard'),
    path('gestion/', vista_viajes, name='vista_viajes'),
    path('viaje_muro/', viaje_muro, name='viaje_muro'),
]