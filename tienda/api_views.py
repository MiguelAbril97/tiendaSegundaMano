from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

import datetime

@api_view(['GET'])
def obtener_producto(request,producto_id):
    if request.user.has_perm("view_producto"):
        producto = Producto.objects.select_related('vendedor').prefetch_related('categorias')
        producto = producto.get(id=producto_id)
        serializer = ProductoSerializerMejorado(producto)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def obtener_compra(request,compra_id):
    if request.user.has_perm("view_compra"):
        compra = Compra.objects.select_related('comprador').prefetch_related('producto').get(id=compra_id)
        serializer = CompraSerializer(compra)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def obtener_valoracion(request,valoracion_id):
    if request.user.has_perm("view_valoracion"):
        valoracion = Valoracion.objects.get(id=valoracion_id)
        serializer = ValoracionSerializer(valoracion)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def categoria_listar(request):
    if request.user.has_perm("view_categoria"):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def compra_listar(request):
    if request.user.has_perm("view_compra"):
        compras = Compra.objects.select_related('comprador').prefetch_related('producto').all()
        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def vendedores_listar(request):
    if request.user.has_perm("view_vendedor"):
        vendedores = Vendedor.objects.select_related('usuario').all()
        serializer = VendedorSerializer(vendedores, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def compradores_listar(request):
    if request.user.has_perm("view_comprador"):
        compradores = Comprador.objects.select_related('usuario').all()
        serializers = CompradorSerializer(compradores, many=True)
        return Response(serializers.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def valoraciones_listar(request):
    if request.user.has_perm("view_valoracion"):
        valoraciones = Valoracion.objects.select_related('usuario','compra').all()
        serializers = ValoracionSerializer(valoraciones, many=True)
        return Response(serializers.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
#@request.user.has_perm("view_producto")
def producto_listar(request):
    if request.user.has_perm("view_producto"):
        productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').all()
        serializer = ProductoSerializer(productos,many = True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def producto_listar_mejorado(request):
    if request.user.has_perm("view_producto"):
        productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').all()
        serializer = ProductoSerializerMejorado(productos,many = True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def producto_buscar_simple(request):
    if request.user.has_perm("view_producto"):
        formulario = BusquedaProductoSimple(request.query_params)
        if(formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').filter(
                nombre__contains=texto).all()
            serializer = ProductoSerializerMejorado(productos, many=True)
            return Response(serializer.data)
        else: 
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def producto_buscar(request):
    if request.user.has_perm("view_producto"):
        if(len(request.query_params) > 0):
            formulario = BuscarProductoAPI(request.query_params)
            if formulario.is_valid():
                mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
                QSproductos = Producto.objects.select_related(
                    'vendedor').prefetch_related('categorias')
                
                nombre = formulario.cleaned_data.get('buscarNombre')
                descripcion = formulario.cleaned_data.get('buscarDescripcion')
                precio = formulario.cleaned_data.get('buscarPrecioMax')
                estado = formulario.cleaned_data.get('buscarEstado')
                vendedor = formulario.cleaned_data.get('buscarVendedor')
                fecha = formulario.cleaned_data.get('buscarFecha')
                categoria = formulario.cleaned_data.get('buscarCategorias')

                if(nombre != ""):
                    QSproductos = QSproductos.filter(nombre__icontains=nombre)
                    mensaje_busqueda +=" Nombre que contenga "+nombre+"\n"

                if(descripcion != ""):
                    QSproductos = QSproductos.filter(descripcion__icontains=descripcion)
                    mensaje_busqueda +=" Descripcion que contenga "+descripcion+"\n"

                if(precio is not None):
                    QSproductos = QSproductos.filter(precio__lte=precio)
                    mensaje_busqueda += "Precio menor o igual a "+str(precio)+"\n"

                if(len(estado) > 0):
                    QSproductos = QSproductos.filter(estado__in=estado)
                    mensaje_busqueda +=" El estado sea "+estado[0]
                    for i in estado[1:]:
                        mensaje_busqueda += " o "+i
                    mensaje_busqueda += "\n"

                if(vendedor):
                    QSproductos = QSproductos.filter(vendedor__username=vendedor.username)
                    mensaje_busqueda +=" Vendedor: "+vendedor.username+"\n"

                if(not fecha is None):
                    QSproductos = QSproductos.filter(fecha_de_publicacion__gte=fecha)
                    mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha, '%d-%m-%Y')+"\n"

                if(categoria):
                    QSproductos = QSproductos.filter(categorias__nombre=categoria.nombre)
                    mensaje_busqueda +=" Categoria: "+categoria.nombre+"\n"
                
                productos = QSproductos.all()
                serializer = ProductoSerializerMejorado(productos, many=True)
                
                return Response(serializer.data)
            else:
                return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
#
#CRUD ManyToMany con tabla intermedia
#

@api_view(['POST'])
def producto_crear(request):
    if request.user.has_perm("add_producto"):
        print(request.data)
        productoCreateSerializer = ProductoCreateSerializer(
            data=request.data)
        if productoCreateSerializer.is_valid():
            try:
                productoCreateSerializer.save()
                return  Response('Producto creado')
            except serializers.ValidationError as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
def producto_editar(request,producto_id):
    if request.user.has_perm("change_producto"):
        producto = Producto.objects.get(id=producto_id)
        productoCreateSerializer = ProductoCreateSerializer(
            data = request.data, instance = producto)
        if productoCreateSerializer.is_valid():
            try:
                productoCreateSerializer.save()
                return  Response('Producto editado')
            except serializers.ValidationError as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#He tenido que hacer esto porque me he llevado un monton de 
# tiempo intentando arreglar lo del csrf token y no podia
#En otras view de patch no me da error, no se por que en esta si
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['PATCH']) 
def producto_actualizar_nombre(request,producto_id):
    if request.user.has_perm("change_producto"):
        producto = Producto.objects.get(id=producto_id)
        serializer = ProductoSerializerActualizarNombre(
            data=request.data,instance=producto
        )
        if serializer.is_valid():
            try:
                serializer.save()
                return Response('Nombre actualizado')
            except Exception as error:
                print(repr(error))
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
def producto_eliminar(request,producto_id):
    if request.user.has_perm("delete_producto"):
        producto = Producto.objects.get(id=producto_id)
        try:
            producto.delete()
            return Response('Producto eliminado')
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    

#
#CRUD ManyToOne
#
@api_view(['POST'])
def valoracion_crear(request):
    if request.user.has_perm("add_valoracion"):
        print(request.data)
        valoracionCreateSerializer = ValoracionCreateSerializer(
            data=request.data)
        if valoracionCreateSerializer.is_valid():
            try:
                valoracionCreateSerializer.save()
                return  Response('Valoracion creada')
            except serializers.ValidationError as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(valoracionCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
@api_view(['PUT'])
def valoracion_editar(request,valoracion_id):
    if request.user.has_perm("change_valoracion"):
        valoracion = Valoracion.objects.get(id=valoracion_id)
        valoracionCreateSerializer = ValoracionCreateSerializer(
            data = request.data, instance = valoracion)
        if valoracionCreateSerializer.is_valid():
            try:
                valoracionCreateSerializer.save()
                return  Response('Valoracion editada')
            except serializers.ValidationError as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(valoracionCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['PATCH'])
def valoracion_actualizar_puntuacion(request,valoracion_id):
    if request.user.has_perm("change_valoracion"):
        valoracion = Valoracion.objects.get(id=valoracion_id)
        serializer = ValoracionActualizarPuntuacionSerializer(
            data=request.data,instance=valoracion
        )
        if serializer.is_valid():
            try:
                serializer.save()
                return Response('Puntuacion actualizada')
            except Exception as error:
                print(repr(error))
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
@api_view(['DELETE'])
def valoracion_eliminar(request,valoracion_id):
    if request.user.has_perm("delete_valoracion"):
        valoracion = Valoracion.objects.get(id=valoracion_id)
        try:
            valoracion.delete()
            return Response('Valoracion eliminada')
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
        

#################
##  REGISTRO
#################
from rest_framework import generics
from rest_framework.permissions import AllowAny

class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                   username = serializers.data.get("username"), 
                    email = serializers.data.get("email"), 
                    password = serializers.data.get("password1"),
                    rol = rol,
                    telefono = serializers.data.get("telefono"),
                    direccion = serializers.data.get("direccion")
                    )
                
                ####
                #Obtengo los valores directamente de la request en vez del serializer
                #porque al definir la variable dentro del metodo no me la devuelve
                
                if(rol== '2'):
                    grupo = Group.objects.get(name="Compradores")
                    grupo.user_set.add(user)
                    comprador = Comprador.objects.create(
                        usuario = user,
                        nombre = request.data.get("nombre"),
                        apellidos = request.data.get("apellidos")
                    )
                    comprador.save()
                elif(rol == '3'):
                    grupo = Group.objects.get(name="Vendedores")
                    grupo.user_set.add(user)
                    vendedor = Vendedor.objects.create(
                        usuario = user,
                        razonSocial = request.data.get("razonSocial"),
                        direccionFiscal = request.data.get("direccionFiscal")
                    )
                    vendedor.save()
            
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            
            except Exception as error:
               print(repr(error))
               return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)