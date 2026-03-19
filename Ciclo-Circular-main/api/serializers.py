from rest_framework import serializers
from user.models import Usuario
from app.models import Oferta

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        #exclude define los campos que no apareceran en la consulta
        #exclude = ['user_permissions', 'groups', 'is_active', 'date_joined', 'is_superuser']
        fields = 'first_name', 'last_name', 'email', 'telefono'
        
class OfertaSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Oferta
        fields = [
            'id_oferta',
            'titulo',
            'empresa',
            'descripcion',
            'modalidad',
            'jornada',
            'salario',
            'ubicacion',
            'activa',
            'creado_por',
            'palabra1',
            'palabra2',
            'palabra3',
            'palabra4',
            'palabra5',
            'creado',
        ]