from rest_framework import serializers
from .models import *
from .forms import *
from django.utils import timezone
                
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'
        
class VendedorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = Vendedor
        fields = '__all__'

class CompradorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = Comprador
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

class CompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['producto','comprador',
                  'fecha_de_compra','garantia']
        model = Compra
        
        def validate_producto(self,producto):
            if len(producto) < 1:
                raise serializers.ValidationError('Debe indicar un producto')
            return producto
        
        def validate_comprador(self,comprador):
            if len(comprador) != 1:
                raise serializers.ValidationError('Debe indicar un comprador')
            return comprador
        
        def validate_fecha_de_compra(self,fecha_de_compra):
            if fecha_de_compra > timezone.now():
                raise serializers.ValidationError('La fecha de compra no puede ser mayor a la fecha actual')
            return fecha_de_compra
        
        def validate_garantia(self,garantia):
            if garantia not in ['UNO', 'DOS']:
                raise serializers.ValidationError('Garantía no válida')
            return garantia
        
        def create(self, validated_data):
            compra = Compra.objects.create(
                producto = validated_data['producto'],
                comprador = validated_data['comprador'],
                fecha_de_compra = validated_data['fecha_de_compra'],
                garantia = validated_data['garantia']
            )
            return compra

class ValoracionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['usuario','compra','puntuacion'
                  ,'comentario','fecha_valoracion']
        model = Valoracion
        
        def validate_puntuacion(self,puntuacion):
            if puntuacion < 1 or puntuacion > 5:
                raise serializers.ValidationError('Puntuación inválida')
            return puntuacion
        
        def validate_comentario(self,comentario):
            if comentario and len(comentario) > 200:
                raise serializers.ValidationError('Comentario inválido')
            return comentario
        
        def validate_fecha_valoracion(self,fecha_valoracion):
            if fecha_valoracion > timezone.now():
                raise serializers.ValidationError('Fecha inválida')
            return fecha_valoracion
        
        def create(self, validated_data):
            valoracion = Valoracion.objects.create(
                usuario = validated_data['usuario'],
                compra = validated_data['compra'],
                puntuacion = validated_data['puntuacion'],
                comentario = validated_data['comentario'],
                fecha_valoracion = validated_data['fecha_valoracion']
            )
            return valoracion
    
    
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

       