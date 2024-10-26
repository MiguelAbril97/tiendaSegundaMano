from django.shortcuts import render
from django.db.models import Q,F,Prefetch
from django.db.models import Avg,Max,Min
from django.db.models import Count
from .models import Producto, Usuario, Categoria, ProductoCategoria
from django.views.defaults import page_not_found, permission_denied, bad_request, server_error


### filtro con None CHECK
### order by, CHECK
### limit, CHECK
### aggregate, CHECK
### OR CHECK
### relacion reversa
### filtros con AND preguntar si vale la , en un filtro

# Create your views here.
def index(request):
    return render(request, "index.html")

#Esta view muestra una lista con toda la informacion de todos los productos que hay
def listar_productos (request):
    producto = Producto.objects.select_related("vendedor").prefetch_related("categorias")
    producto = producto.all()
    total = producto.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"producto_mostrar":producto, 'total':total})

#Esta view muestra toda la informacion de un producto
def muestra_producto(request, id_producto):
    QSproducto = Producto.objects.select_related("vendedor").prefetch_related("categorias")
    producto = QSproducto.get(id=id_producto)
    return render(request, "productos/producto.html", {"producto_mostrar":producto})

#Esta view muestra una lista con toda la informacion de todos 
#los productos publicados en el anño y mes indicados
def listar_productos_fecha(request, anyo, mes):
    productos=Producto.objects.select_related("vendedor").prefetch_related("categorias")
    productos = productos.filter(fecha_de_publicacion__year = anyo, fecha_de_publicacion__month = mes)
    total = productos.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"producto_mostrar":productos, 'total':total}) 

#Muestra los productos de una categoria cuando le pasas el nombre de la
# categoria y cuenta cuantos hay
def listar_productos_categoria(request,nombre_categoria):
    productos= Producto.objects.select_related("vendedor").prefetch_related("categorias")
    productos=productos.filter(categorias__nombre=nombre_categoria)
    total = productos.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"producto_mostrar":productos, 'total':total})

#Muestra el ultimo productos de un mes
def ultimo_producto_fecha (request, anyo, mes):
    productos=Producto.objects.select_related("vendedor").prefetch_related("categorias")
    productos = productos.filter(fecha_de_publicacion__year = anyo, fecha_de_publicacion__month = mes).order_by("-fecha_de_publicacion")[:1].get()
    return render(request, "productos/producto.html", {"producto_mostrar":productos}) 

#Muestra los productos que sean de una categoria 
# O
# que sean inferior a un precio
def productos_categoria_precio(request, nombre_categoria, precio_max):
    productos = Producto.objects.select_related("vendedor").prefetch_related("categorias")
    productos = productos.filter(Q(categorias__nombre=nombre_categoria) | Q(precio__lt=precio_max))
    total = productos.aggregate(Count('id'))
    return render(request, 'productos/lista.html', {'producto_mostrar': productos, 'total':total})

#Muestra los usuarios que no tienen productos en venta

def usuario_sin_productos(request):
    usuarios = Usuario.objects.filter(producto_vendedor=None).all()
    return render(request, 'usuarios/lista.html',{'usuarios':usuarios})



##Crear una página de Error personalizada para cada uno de los 4 
# tipos de errores que pueden ocurrir en nuestra Web.

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'errores/500.html', None, None, 500)
