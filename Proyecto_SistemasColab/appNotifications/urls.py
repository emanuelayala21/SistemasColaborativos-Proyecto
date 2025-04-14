from django.urls import path
from .views import NotificacionesNoLeidasView, MarcarNotificacionComoLeidaView, VerificarNuevasNotificacionesView

urlpatterns = [
    path('noleidas/', NotificacionesNoLeidasView.as_view(), name='notificaciones-no-leidas'),
    path('<int:pk>/leer/', MarcarNotificacionComoLeidaView.as_view(), name='marcar-notificacion-leida'),
    path('nuevas/', VerificarNuevasNotificacionesView.as_view()),
]
