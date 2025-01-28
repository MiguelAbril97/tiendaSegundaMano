from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

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