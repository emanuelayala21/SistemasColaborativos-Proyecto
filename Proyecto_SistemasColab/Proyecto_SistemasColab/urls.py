from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuario/', include('_appUser.urls')),
    path('api/viaje/', include('_appTrip.urls')),
    path('api/notificacion/', include('appNotifications.urls')),
]
