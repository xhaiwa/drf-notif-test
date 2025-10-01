from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, NotificationViewSet

# Router DRF pour les ViewSets (CRUD automatique)
v1 = DefaultRouter()
v1.register(r'notifications', NotificationViewSet)

# Combiner routes automatiques + route personnalisée
urlpatterns = [
    path('health/', health),           # route personnalisée
    path('v1/', include(v1.urls)),    # routes CRUD automatiques
]
