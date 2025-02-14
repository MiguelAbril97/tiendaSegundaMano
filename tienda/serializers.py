from rest_framework import serializers
from .models import *
from .forms import *
from django.utils import timezone
                
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class VendedorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = Vendedor
        fields = '__all__'
        
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        
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
        
class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['nombre','descripcion',
                  'precio','estado','vendedor',
                  'categorias','fecha_de_publicacion']
        model = Producto
        
        def validate_precio(self,precio):
            if precio <= 0:
                raise serializers.ValidationError('El precio debe ser mayor a cero')
            return precio
        
        def validate_estado(self, estado):
            if estado not in ['CN','U','MU']:
                raise serializers.ValidationError('Estado no válido')
            return estado
        
        def validate_vendedor(self,vendedor):
            if len(vendedor) < 1:
                raise serializers.ValidationError('Debe indicar un vendedor')
            return vendedor
        
        def fecha_publicacion(self,fecha_de_publicacion):
            if fecha_de_publicacion > timezone.now():
                raise serializers.ValidationError('La fecha de publicación no puede ser mayor a la fecha actual')
            return fecha_de_publicacion

        def create(self, validated_data):
            categorias = self.initial_data['categorias']
            
            if len(categorias) < 1:
                raise serializers.ValidationError(
                                                  {'categorias':
                                                    ['Debe indicar al menos una categoría']
                                                  })
                
            producto = Producto.objects.create(
                nombre = validated_data['nombre'],
                descripcion = validated_data['descripcion'],
                precio = validated_data['precio'],
                estado = validated_data['estado'],
                vendedor = validated_data['vendedor'],
                fecha_de_publicacion = validated_data['fecha_de_publicacion'],    
            )
            
            for categoria in categorias:
                modeloCategoria = Categoria.objects.get(id=categoria)
                ProductoCategoria.objects.create(categoria=modeloCategoria,
                                                 producto=producto)
            return producto
        
        
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
        
class CalzadoCreateSerializer(serializers.ModelSerializer):
#    producto = ProductoCreateSerializer()
    class Meta:
        fields = ['producto','talla','marca','color','material']
        model = Calzado
        
        def validate_talla(self,talla):
            if talla <= 0 and talla > 55:
                raise serializers.ValidationError('Talla inválida')
            return talla
        def validate_marca(self,marca):
            if marca not in ['NIKE','ADID','PUMA','RBK','NB','CLRK','GUCCI']:
                raise serializers.ValidationError('Marca inválida')
            return marca
        
        def validate_color(self,color):
            if len(color) > 20:
                raise serializers.ValidationError('Color inválido')
            return color
        
        def validate_material(self,material):
            if len(material) > 30:
                raise serializers.ValidationError('Material inválido')
            return material
        
        def create(self, validated_data):
            
            calzado = Calzado.objects.create(
               producto = validated_data['producto'],
               talla = validated_data['talla'],
               marca = validated_data['marca'],
               color = validated_data['color'],
               material = validated_data['material']
            )
            return calzado
                   
class ConsolasSerializer(serializers.ModelSerializer):
    producto = ProductoSerializerMejorado()
    class Meta:
        fields = ['producto','modelo','color',
                  'memoria']
        model = Consolas

class ConsolaCreateSerializer(serializers.ModelSerializer):
#    producto = ProductoCreateSerializer()
    class Meta:
        fields = ['producto','modelo','color',
                  'memoria']
        model = Consolas
        
        def validate_modelo(self,modelo):
            if len(modelo) > 50:
                raise serializers.ValidationError('Modelo inválido')
            return modelo
        
        def validate_color(self,color):
            if len(color) > 20:
                raise serializers.ValidationError('Color inválido')
            return color
        
        def validate_memoria(self,memoria):
            if memoria <= 0 or len(memoria) > 20:
                raise serializers.ValidationError('Memoria inválida')
            return memoria
        
        def create(self, validated_data):
            consola = Consolas.objects.create(
                producto = validated_data['producto'],
                modelo = validated_data['modelo'],
                color = validated_data['color'],
                memoria = validated_data['memoria']
            )
            return consola


class MueblesSerializer(serializers.ModelSerializer):
    producto = ProductoSerializerMejorado()
    class Meta:
        fields = ['producto', 'material', 'ancho', 
                  'alto', 'profundidad', 'peso']
        model = Muebles
        
class MuebleCreateSerializer(serializers.ModelSerializer):
#    producto = ProductoCreateSerializer()
    class Meta:
        fields = ['producto', 'material', 'ancho', 
                  'alto', 'profundidad', 'peso']
        model = Muebles
        
        def validate_material(self,material):
            if len(material) > 30 or material=='':
                raise serializers.ValidationError('Material inválido')
            return material
        
        def validate_ancho(self,ancho):
            if ancho <= 0:
                raise serializers.ValidationError('Ancho inválido')
            return ancho
        
        def validate_alto(self,alto):
            if alto <= 0:
                raise serializers.ValidationError('Alto inválido')
            return alto
        
        def validate_profundidad(self,profundidad):
            if profundidad <= 0:
                raise serializers.ValidationError('Profundidad inválida')
            return profundidad
        
        def validate_peso(self,peso):
            if peso <= 0:
                raise serializers.ValidationError('Peso inválido')
            return peso
        
        def create(self, validated_data):
            mueble = Muebles.objects.create(
                producto = validated_data['producto'],
                material = validated_data['material'],
                ancho = validated_data['ancho'],
                alto = validated_data['alto'],
                profundidad = validated_data['profundidad'],
                peso = validated_data['peso']
            )
            return mueble

       