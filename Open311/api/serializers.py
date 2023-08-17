from rest_framework import serializers
from solicitudes.models import *

class SolicitudesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'usuario', 'categoria', 'sub_categoria', 'comentario', 'ubicacion', 'fecha_creacion']
        read_only_fields = ['id', 'usuario','fecha_creacion']
