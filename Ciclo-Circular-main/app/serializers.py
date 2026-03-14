from rest_framework import serializers
from .models import Oferta

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'
        read_only_fields = ['creado', 'actualizado']