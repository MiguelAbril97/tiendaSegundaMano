from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','vendedor','fecha_de_publicacion','categorias']