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
def producto_listar_avanzado(request):
    productos = Producto.objects.select_related('vendedor').prefetch_related('categorias',
                                                                             Prefetch('producto_compra')).all()
    serializer = ProductoSerializer(productos,many = True)
    return Response(serializer.data)