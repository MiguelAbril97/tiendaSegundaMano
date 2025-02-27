from rest_framework import serializers
from .models import *
from .forms import *
                
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
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
    estado = serializers.CharField(source='get_estado_display')
    class Meta:
        fields = ['id','nombre','descripcion','precio',
                  'estado']
        model = Producto

class CompraSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(many=True, read_only=True)
    class Meta:
        model = Compra
        fields = '__all__'

class ValoracionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    compra = CompraSerializer()
    class Meta:
        model = Valoracion
        fields = '__all__'

class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['nombre','descripcion',
                  'precio','estado','vendedor',
                  'categorias']
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
            )
            
            for categoria in categorias:
                modeloCategoria = Categoria.objects.get(id=categoria)
                ProductoCategoria.objects.create(categoria=modeloCategoria,
                                                 producto=producto)
            return producto
        
        def update (self, instance, validated_data):
            categorias = self.initial_data['categorias']
            
            if len(categorias) < 1:
                raise serializers.ValidationError(
                                                  {'categorias':
                                                    ['Debe indicar al menos una categoría']
                                                  })
            instance.nombre = validated_data['nombre']
            instance.descripcion = validated_data['descripcion']
            instance.precio = validated_data['precio']
            instance.estado = validated_data['estado']
            instance.vendedor = validated_data['vendedor']
            
            instance.save()
            
            instance.categorias.clear()
            for categoria in categorias:
                modeloCategoria = Categoria.objects.get(id=categoria)
                ProductoCategoria.objects.create(categoria=modeloCategoria,
                                                 producto=instance)
            return instance

class ProductoSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre']
        
        def validate_nombre(self,nombre):
            if len(nombre) > 100:
                raise serializers.ValidationError('Nombre inválido')
            return nombre   
        
class ProductoSerializerMejorado(serializers.ModelSerializer): 
    vendedor = UsuarioSerializer()
    categorias = ProductoCategoriaSerializer(many=True, source='productocategoria_set')
    estado = serializers.CharField(source='get_estado_display')
    class Meta:
        fields = '__all__'
        model = Producto

class CompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['producto','comprador',
                  'garantia','total']
        model = Compra
        
        def validate_producto(self,producto):
            if len(producto) < 1:
                raise serializers.ValidationError('Debe indicar un producto')
            return producto
        
        def validate_comprador(self,comprador):
            if len(comprador) != 1:
                raise serializers.ValidationError('Debe indicar un comprador')
            return comprador
           
        def validate_garantia(self,garantia):
            if garantia not in ['UNO', 'DOS']:
                raise serializers.ValidationError('Garantía no válida')
            return garantia

        def validate_total(self,total):
            if total < 1:
                raise serializers.ValidationError('Total debe ser mayor que 0')
            return total
        
        def create(self, validated_data):
            compra = Compra.objects.create(
                producto = validated_data['producto'],
                comprador = validated_data['comprador'],
                garantia = validated_data['garantia']
            )
            return compra

        def update(self, instance, validated_data):
            instance.comprador = validated_data['comprador']
            instance.garantia = validated_data['garantia']
            instance.total = validated_data['total']
            instance.save()
            
            instance.producto.set(validated_data['producto'])
            
            return instance

class CompraActualizarGarantiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['garantia']
        
        def validate_garantia(self,garantia):
            if garantia not in ['UNO', 'DOS']:
                raise serializers.ValidationError('Garantía no válida')
            return garantia

class ValoracionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['usuario','compra','puntuacion'
                  ,'comentario']
        model = Valoracion
        
        def validate_comprador(self,comprador):
            if len(comprador) != 1:
                raise serializers.ValidationError('Solo puede ser 1 comprador') 
            return comprador
        
        def validate_puntuacion(self,puntuacion):
            if puntuacion < 1 or puntuacion > 5:
                raise serializers.ValidationError('Puntuación inválida')
            return puntuacion
        
        def validate_comentario(self,comentario):
            if comentario and len(comentario) > 200:
                raise serializers.ValidationError('Comentario inválido')
            return comentario
        
        def create(self, validated_data):
            valoracion = Valoracion.objects.create(
                usuario = validated_data['usuario'],
                compra = validated_data['compra'],
                puntuacion = validated_data['puntuacion'],
                comentario = validated_data['comentario'],
            )
            return valoracion

        def update(self, instance, validated_data):
            instance.usuario = validated_data['usuario']
            instance.compra = validated_data['compra']
            instance.puntuacion = validated_data['puntuacion']
            instance.comentario = validated_data['comentario']
            instance.save()
            return instance

class ValoracionActualizarPuntuacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = ['puntuacion']
        
        def validate_puntuacion(self,puntuacion):
            if puntuacion < 1 or puntuacion > 5:
                raise serializers.ValidationError('Puntuación inválida')
            return puntuacion
        
class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    rol = serializers.IntegerField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    telefono = serializers.CharField()
    direccion = serializers.CharField()
    nombre = serializers.CharField()
    apellidos = serializers.CharField()
    razonSocial = serializers.CharField()
    direccionFiscal = serializers.CharField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username
    
    def validate_rol(self,rol):
        if(rol < 2 or rol > 3):
            raise serializers.ValidationError('Rol incorrecto')
        return rol
    
    def validate_password(self,password1,password2):
        if(password1 != password2):
            raise serializers.ValidationError('Las contraseñas deben ser iguales')
        return password1
    
    def validate_email(self, email):
        correo = Usuario.objects.filter(email=email).first()
        if (not correo is None):
            raise serializers.ValidationError("El correo no es válido")
        return email
    
    if(rol == Usuario.COMPRADOR):
        def validate_nombre(self,nombre):
            if(len(nombre) > 60):
                raise serializers.ValidationError("El nombre no puede exceder los 60 carácteres")
            return nombre
        
        def validate_apellidos(self,apellidos):
           if(len(apellidos) > 60):
               raise serializers.ValidationError("Los apellidos no pueden exceder los 60 carácteres")
           return apellidos
    
    elif(rol == Usuario.VENDEDOR):
        
        def validate_razonSocial(self,razonSocial):
            if(len(razonSocial) > 150):
                raise serializers.ValidationError("La razon social no puede exceder los 150 carácteres")   
            return razonSocial
        
        def validate_direccionFiscal(self,direccionFiscal):
            if(len(direccionFiscal) > 150):
                raise serializers.ValidationError("La dirección fiscal no puede exceder los 150 carácteres")   
            return direccionFiscal