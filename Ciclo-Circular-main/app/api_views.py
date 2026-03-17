from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Oferta
from .serializers import OfertaSerializer
from .models import Necesidad
from .serializers import NecesidadSerializer

class EsSoloAdmin(permissions.BasePermission):
    """Solo los administradores pueden acceder"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class OfertaViewSet(viewsets.ModelViewSet):
    """
    API CRUD completa para Ofertas de Empleo
    - GET    /api/ofertas/       → lista todas
    - POST   /api/ofertas/       → crea una nueva
    - GET    /api/ofertas/1/     → ver una específica
    - PUT    /api/ofertas/1/     → editar completa
    - PATCH  /api/ofertas/1/     → editar parcial
    - DELETE /api/ofertas/1/     → eliminar
    """
    queryset = Oferta.objects.all().order_by('-creado')
    serializer_class = OfertaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [EsSoloAdmin]

    def perform_create(self, serializer):
        # Guarda automáticamente quién creó la oferta
        serializer.save(creado_por=self.request.user)
        


class NecesidadViewSet(viewsets.ModelViewSet):
    queryset = Necesidad.objects.all().order_by('-creado')
    serializer_class = NecesidadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [EsSoloAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)