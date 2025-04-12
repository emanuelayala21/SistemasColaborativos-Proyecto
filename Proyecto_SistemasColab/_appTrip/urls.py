from django.urls import path
from .views import ViajeViewSet, ListarViajesView, vista_dashboard, vista_viajes
from .views import ListarViajesParticipanteView
from .views import ParticipantesViajeView
from . import views
from .views import NotasImportantesView

urlpatterns = [
    path('crear_viaje/', ViajeViewSet.as_view({'post': 'create'}), name='crear_viaje'),
    path('mis_viajes/', ListarViajesView.as_view(), name='mis_viajes'),
    path('incluido/', ListarViajesParticipanteView.as_view(), name='viajes_incluidos'),  
    path('<int:pk>/', ViajeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy', 'put': 'update'}), name='detalle_viaje'),
     path('participantes/<int:viaje_id>/', ParticipantesViajeView.as_view(), name='participantes_viaje'),
    path('notas/<int:viaje_id>/', NotasImportantesView.as_view(), name='notas_importantes'),
    

    # Rutas HTML
    path('dashboard/', vista_dashboard, name='vista_dashboard'),
    path('gestion/', vista_viajes, name='vista_viajes'),
    path('viaje_muro/', views.viaje_muro, name='viaje_muro'),
]


