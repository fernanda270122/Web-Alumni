from rest_framework import serializers
from .models import Oferta
from .models import Necesidad

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'
        read_only_fields = ['creado', 'actualizado']

class NecesidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Necesidad
        fields = '__all__'
        read_only_fields = ['creado']