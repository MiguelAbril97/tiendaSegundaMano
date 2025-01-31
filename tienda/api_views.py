from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch

@api_view(['GET'])
def producto_listar(request):
    productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').all()
    serializer = ProductoSerializer(productos,many = True)
    return Response(serializer.data)

@api_view(['GET'])
def producto_listar_mejorado(request):
    productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').all()
    serializer = ProductoSerializerMejorado(productos,many = True)
    return Response(serializer.data)

@api_view(['GET'])
def calzado_listar(request):
    calzados = Calzado.objects.select_related('producto').all()
    serializers = CalzadoSerializer(calzados,many = True)
    return Response(serializers.data)

@api_view(['GET'])
def consolas_listar(request):
    consolas = Consolas.objects.select_related('producto').all()
    serializers = ConsolasSerializer(consolas,many = True)
    return Response(serializers.data)


@api_view(['GET'])
def producto_buscar_simple(request):
    formulario = BusquedaProductoSimple(request.query_params)
    if(formulario.is_valid):
        texto = formulario.data.get('textoBusqueda')
        productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').filter(
            nombre__contains=texto).all()
        serializer = ProductoSerializerMejorado(productos, many=True)
        return Response(serializer.data)
    else: 
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    
def producto_buscar(request):
    if(len(request.query_params) > 0):
        formulario = BuscarProducto(request.GET)
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

            if(len(vendedor) > 0):
                QSproductos = QSproductos.filter(vendedor__in=vendedor)
                mensaje_busqueda +=" Vendedores: "+vendedor[0].email
                for v in vendedor[1:]:
                    mensaje_busqueda += " o "+v.email
                mensaje_busqueda += "\n"

            if(not fecha is None):
                QSproductos = QSproductos.filter(fecha_de_publicacion__gte=fecha)
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha, '%d-%m-%Y')+"\n"

            if(len(categoria) > 0):
                QSproductos = QSproductos.filter(categorias__in=categoria)
                mensaje_busqueda +=" Categorias: "+categoria[0].nombre
                for c in categoria[1:]:
                    mensaje_busqueda += " o "+c.nombre
                mensaje_busqueda += "\n"
        
            productos = QSproductos.all()
            serializer = ProductoSerializerMejorado(productos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
