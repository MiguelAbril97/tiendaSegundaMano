from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
import datetime

@api_view(['GET'])
def categoria_listar(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vendedores_listar(request):
    vendedores = Vendedor.objects.select_related('usuario').all()
    serializer = VendedorSerializer(vendedores, many=True)
    return Response(serializer.data)

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
def mueble_listar(request):
    muebles = Muebles.objects.select_related('producto').all()
    serializers = MueblesSerializer(muebles, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def producto_buscar_simple(request):
    formulario = BusquedaProductoSimple(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        productos = Producto.objects.select_related('vendedor').prefetch_related('categorias').filter(
            nombre__contains=texto).all()
        serializer = ProductoSerializerMejorado(productos, many=True)
        return Response(serializer.data)
    else: 
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def producto_buscar(request):
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
    
@api_view(['POST'])
def producto_crear(request):
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
    

@api_view(['GET'])
def consola_buscar(request):
    if(len(request.query_params) > 0):
        formulario = BuscarConsola(request.query_params)
        if(formulario.is_valid()):
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            QSconsolas = Consolas.objects.select_related('producto').prefetch_related(Prefetch('producto__categorias'))
            
            nombre = formulario.cleaned_data.get('buscarNombre')
            marca = formulario.cleaned_data.get('buscarMarca')
            modelo = formulario.cleaned_data.get('buscarModelo')
            almacenamiento = formulario.cleaned_data.get('buscarAlmacenamiento')
            precio = formulario.cleaned_data.get('buscarPrecioMax')

            if(nombre):
                QSconsolas = QSconsolas.filter(producto__nombre__icontains=nombre)
                mensaje_busqueda += " Nombre que contenga " + nombre + "\n"
            
            if(marca):
                QSconsolas = QSconsolas.filter(marca=marca)
                mensaje_busqueda += " Marca: " + marca + "\n"

            if(modelo):
                QSconsolas = QSconsolas.filter(modelo__icontains=modelo)
                mensaje_busqueda += " Modelo que contenga " + modelo + "\n"

            if(almacenamiento):
                QSconsolas = QSconsolas.filter(almacenamiento__gte=almacenamiento)
                mensaje_busqueda += " Almacenamiento mayor o igual a " + str(almacenamiento) + " GB\n"

            if(precio is not None):
                QSconsolas = QSconsolas.filter(producto__precio__lte=precio)
                mensaje_busqueda += " Precio menor o igual a " + str(precio) + "\n"

            consolas = QSconsolas.all()
            serializer = ConsolasSerializer(consolas, many=True)

            return Response(serializer.data)
        else:
                    return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def consola_crear(request):
    print(request.data)
    consolaCreateSerializer = ConsolaCreateSerializer(
        data=request.data)
    if consolaCreateSerializer.is_valid():
        try:
            consolaCreateSerializer.save()
            return  Response('Consola creada')
        except serializers.ValidationError as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(consolaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def calzado_buscar(request):
    if(len(request.query_params) > 0):
        formulario = BuscarCalzado(request.query_params)
        if(formulario.is_valid()):
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            QScalzados = Calzado.objects.select_related('producto').prefetch_related(Prefetch('producto__categorias'))

            nombre = formulario.cleaned_data.get('buscarNombre')
            talla = formulario.cleaned_data.get('buscarTalla')
            marca = formulario.cleaned_data.get('buscarMarca')
            color = formulario.cleaned_data.get('buscarColor')
            material = formulario.cleaned_data.get('buscarMaterial')
            precio = formulario.cleaned_data.get('buscarPrecioMax')

            if(nombre):
                QScalzados = QScalzados.filter(producto__nombre__icontains=nombre)
                mensaje_busqueda += " Nombre que contenga " + nombre + "\n"
            
            if(talla):
                QScalzados = QScalzados.filter(talla=talla)
                mensaje_busqueda += " Talla: " + str(talla) + "\n"

            if(marca and marca != "''"):
                QScalzados = QScalzados.filter(marca=marca)
                mensaje_busqueda += " Marca: " + marca + "\n"

            if(color):
                QScalzados = QScalzados.filter(color__icontains=color)
                mensaje_busqueda += " Color que contenga " + color + "\n"

            if(material):
                QScalzados = QScalzados.filter(material__icontains=material)
                mensaje_busqueda += " Material que contenga " + material + "\n"

            if(precio is not None):
                QScalzados = QScalzados.filter(producto__precio__lte=precio)
                mensaje_busqueda += " Precio menor o igual a " + str(precio) + "\n"

            calzados = QScalzados.all()
            serializer = CalzadoSerializer(calzados, many=True)

            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def calzado_crear(request):
    print(request.data)
    calzadoCreateSerializer = CalzadoCreateSerializer(
        data=request.data)
    if calzadoCreateSerializer.is_valid():
        try:
            calzadoCreateSerializer.save()
            return  Response('Calzado creado')
        except serializers.ValidationError as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(calzadoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def mueble_buscar(request):
        if(len(request.query_params) > 0):
            formulario = BuscarMueble(request.query_params)
            if(formulario.is_valid()):
                mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
                QSmuebles = Muebles.objects.select_related('producto').prefetch_related(Prefetch('producto__categorias'))

                nombre = formulario.cleaned_data.get('buscarNombre')
                material = formulario.cleaned_data.get('buscarMaterial')
                ancho_min = formulario.cleaned_data.get('buscarAnchoMin')
                ancho_max = formulario.cleaned_data.get('buscarAnchoMax')
                alto_min = formulario.cleaned_data.get('buscarAltoMin')
                alto_max = formulario.cleaned_data.get('buscarAltoMax')
                profundidad_min = formulario.cleaned_data.get('buscarProfundidadMin')
                profundidad_max = formulario.cleaned_data.get('buscarProfundidadMax')
                peso_max = formulario.cleaned_data.get('buscarPesoMax')

                if(nombre):
                    QSmuebles = QSmuebles.filter(producto__nombre__icontains=nombre)
                    mensaje_busqueda += " Nombre que contenga " + nombre + "\n"
                    
                if(material):
                    QSmuebles = QSmuebles.filter(material__icontains=material)
                    mensaje_busqueda += " Material que contenga " + material + "\n"
                
                if(ancho_min is not None):
                    QSmuebles = QSmuebles.filter(ancho__gte=ancho_min)
                    mensaje_busqueda += " Ancho mayor o igual a " + str(ancho_min) + "\n"
                if(ancho_max is not None):
                    QSmuebles = QSmuebles.filter(ancho__lte=ancho_max)
                    mensaje_busqueda += " Ancho menor o igual a " + str(ancho_max) + "\n"

                if(alto_min is not None):
                    QSmuebles = QSmuebles.filter(alto__gte=alto_min)
                    mensaje_busqueda += " Alto mayor o igual a " + str(alto_min) + "\n"

                if(alto_max is not None):
                    QSmuebles = QSmuebles.filter(alto__lte=alto_max)
                    mensaje_busqueda += " Alto menor o igual a " + str(alto_max) + "\n"

                if(profundidad_min is not None):
                    QSmuebles = QSmuebles.filter(profundidad__gte=profundidad_min)
                    mensaje_busqueda += " Profundidad mayor o igual a " + str(profundidad_min) + "\n"

                if(profundidad_max is not None):
                    QSmuebles = QSmuebles.filter(profundidad__lte=profundidad_max)
                    mensaje_busqueda += " Profundidad menor o igual a " + str(profundidad_max) + "\n"

                if(peso_max is not None):
                    QSmuebles = QSmuebles.filter(peso__lte=peso_max)
                    mensaje_busqueda += " Peso menor o igual a " + str(peso_max) + "\n"

                muebles = QSmuebles.all()
                serializer = MueblesSerializer(muebles, many=True)

                return Response(serializer.data)
            else:
                return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def mueble_crear(request):
    print(request.data)
    muebleCreateSerializer = MuebleCreateSerializer(
        data=request.data)
    if muebleCreateSerializer.is_valid():
        try:
            muebleCreateSerializer.save()
            return  Response('Mueble creado')
        except serializers.ValidationError as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(muebleCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)