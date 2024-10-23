from django.shortcuts import render
from django.db.models import Q,F,Prefetch
from django.db.models import Avg,Max,Min
from .models import Producto, Usuario, Categoria, ProductoCategoria

# Create your views here.
def index(request):
    return render(request, "index.html")

#Esta view muestra una lista con toda la informacion de todos los productos que hay
def listar_productos (request):
    producto = Producto.objects.select_related("vendedor").prefetch_related("categorias")
    producto = producto.all()
    return render(request, "productos/lista.html", {"producto_mostrar":producto})

def muestra_producto(request, id_producto):
    QSproducto = Producto.objects.select_related("vendedor").prefetch_related("categorias")
    producto = QSproducto.get(id=id_producto)
    return render(request, "productos/producto.html", {"producto_mostrar":producto})

def listar_productos_fecha(request, anyo, mes):
    productos=Producto.objects.select_related("vendedor").prefetch_related("categorias")
    productos = productos.filter(fecha_de_publicacion__year = anyo, fecha_de_publicacion__month = mes)
    return render(request, "productos/lista.html", {"producto_mostrar":productos}) 

#Muestra los productos de una categoria cuando le pasas el nombre de la categoria
def listar_productos_categoria(request,categoria):
    productos= Producto.objects.select_related("vendedor").prefetch_related("categorias")
    productos=productos,filter(categorias=categoria)
    return render(request, "productos/listar.html", {"producto_mostrar":productos})

