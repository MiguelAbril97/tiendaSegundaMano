from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','email']
        
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion','destacada']
        
class ProductoCategoriaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    class Meta:
        model = ProductoCategoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer): 
    fecha_de_publicacion = serializers.DateTimeField(format=('%d-%m-%Y'))
    estado = serializers.CharField(source='get_estado_display')
    class Meta:
        fields = ['nombre','descripcion','precio',
                  'estado','fecha_de_publicacion']
        model = Producto
        
class ProductoSerializerMejorado(serializers.ModelSerializer): 
    vendedor = UsuarioSerializer()
    categorias = ProductoCategoriaSerializer(read_only=True, many=True, source='productocategoria_set')
    fecha_de_publicacion = serializers.DateTimeField(format=('%d-%m-%Y'))
    estado = serializers.CharField(source='get_estado_display')
    class Meta:
        fields = ['nombre','descripcion','precio','estado',
                  'vendedor','fecha_de_publicacion','categorias']
        model = Producto
        
class CalzadoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializerMejorado()
    marca = serializers.CharField(source='get_marca_display')
    class Meta:
        fields = ['producto','talla','marca','color','material']
        model = Calzado
        
class ConsolasSerializer(serializers.ModelSerializer):
    producto = ProductoSerializerMejorado()
    class Meta:
        fields = ['producto','modelo','color',
                  'memoria']
        model = Consolas