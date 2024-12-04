from django.shortcuts import render,redirect
from django.db.models import Q,F,Prefetch
from django.db.models import Avg,Max,Min
from django.db.models import Count
from .models import *
from .forms import *
from django.contrib import messages
from django.views.defaults import page_not_found, permission_denied, bad_request, server_error

#1 Create your views here.
def index(request):
    return render(request, "index.html")

#2 Esta view muestra una lista con toda la informacion de todos los productos que hay
def listar_productos (request):
    productos = Producto.objects.select_related("vendedor").prefetch_related(
        "categorias", Prefetch('producto_compra')).all()
    total = productos.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"producto_mostrar":productos, 'total':total})

#3 Esta view muestra toda la informacion de un producto
def muestra_producto(request, id_producto):
    producto = Producto.objects.select_related("vendedor").prefetch_related("categorias", Prefetch('producto_compra')).get(id=id_producto)
    return render(request, "productos/producto.html", {"producto":producto})

#4 Esta view muestra una lista con toda la informacion de todos 
#los productos publicados en el anño y mes indicados
def listar_productos_fecha(request, anyo, mes):
    productos = Producto.objects.select_related("vendedor").prefetch_related("categorias", Prefetch('producto_compra'))
    productos = productos.filter(fecha_de_publicacion__year = anyo, fecha_de_publicacion__month = mes).all()
    total = productos.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"producto_mostrar":productos, 'total':total}) 

#5 Muestra los productos de una categoria cuando le pasas el nombre de la
# categoria y cuenta cuantos hay.
def listar_productos_categoria(request,nombre_categoria):
    productos = Producto.objects.select_related("vendedor").prefetch_related("categorias", Prefetch('producto_compra'))
    productos=productos.filter(categorias__nombre=nombre_categoria).all()
    total = productos.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"producto_mostrar":productos, 'total':total})

#6 Muestra el ultimo productos de un mes. 
def ultimo_producto_fecha (request, anyo, mes):
    productos = Producto.objects.select_related("vendedor").prefetch_related(
        "categorias", Prefetch('producto_compra'))
    
    productos = productos.filter(fecha_de_publicacion__year = anyo, 
                                 fecha_de_publicacion__month = mes).order_by(
                                     "-fecha_de_publicacion")[:1].get()
    return render(request, "productos/producto.html", {"producto":productos}) 

#7 Muestra los productos que sean de una categoria 
# O
# que sean SUPERIORES a un precio
def productos_categoria_precio(request, nombre_categoria, precio_min):
    productos = Producto.objects.select_related("vendedor").prefetch_related(
        "categorias", Prefetch('producto_compra'))
    
    productos = productos.filter(Q(categorias__nombre=nombre_categoria)
                                 | Q(precio__gte=precio_min)).order_by("-precio")
    
    total = productos.aggregate(Count('id'))
    return render(request, 'productos/lista.html', {'producto_mostrar': productos, 'total':total})

#8 Muestra los usuarios que no tienen productos en venta

def usuario_sin_productos(request):
    usuarios = Usuario.objects.filter(producto_vendedor=None).all()
    return render(request, 'usuarios/lista.html',{'usuarios':usuarios})

#9 Lista de todos los usuarios

def usuarios_listar(request):
    usuarios = Usuario.objects.prefetch_related(Prefetch('producto_vendedor')).all()
    return render(request, 'usuarios/lista.html',{'usuarios':usuarios})

#10 Muestra todos los usuarios que en su correo terminen en .org
def usuarios_correo(request):
    usuarios = Usuario.objects.prefetch_related(Prefetch('producto_vendedor')).filter(
        correo_electronico__regex=r'^\w+[@]\w+\.org$').all()
    return render(request, 'usuarios/lista.html',{'usuarios':usuarios})


#11 Lista todas las consolas. Hago Prefetch categorias del modelo Producto 
# y producto__vendedor para reducir consultas adicionales. Sin ello hacia 16 querys

def lista_consolas(request):
    consolas = Consolas.objects.select_related('producto','producto__vendedor').prefetch_related(
        Prefetch('producto__categorias') )
    return render(request, 'consolas/lista.html', {'consolas': consolas})


#VIEW USUARIO CREAR 

def usuario_crear(request): 
    datosFormulario = None
    if(request.method == "POST"):
        datosFormulario = request.POST
    formulario = UsuarioForm(datosFormulario)
    
    if(request.method == 'POST'):
        usuario_creado = crear_usuario_modelo(formulario)
        
        if(usuario_creado):
            messages.success(request,"Usuario creado")
            return redirect('usuarios_listar')
        
    return render(request, 'usuarios/crear.html',{"formulario":formulario})

def crear_usuario_modelo(formulario):
    usuario_creado = False
    
    if formulario.is_valid():
        try:
            formulario.save()
            usuario_creado = True
        except Exception as error:
            print(error)
    return usuario_creado



#View CATEGORIA CREAR

def categoria_crear (request):
    datosFormulario = None
    if(request.method == "POST"):
        datosFormulario = request.POST
    formulario = CategoriaForm(datosFormulario)
    
    if(request.method == 'POST'):
        categoria_creada = crear_categoria_modelo(formulario)
        if(categoria_creada):
            messages.success(request, 'Se ha creado la categoria')
            return redirect('lista_categoria')
    
    return render(request, 'categoria/crear.html',{"formulario":formulario})

def crear_categoria_modelo(formulario):
    categoria_creada = False
    
    if formulario.is_valid():
        try:
            formulario.save()
            categoria_creada = True
        except Exception as error:
            print(error)
        return categoria_creada


#View Producto CREAR


def producto_crear(request):
    datosFormulario = None
    
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = ProductoForm(datosFormulario)
    
    if(request.method == 'POST'):
        producto_creado = producto_creado_modelo(formulario)
        if(producto_creado):
            messages.success(request, 'Producto añadido')
            return redirect('lista_productos')

    return render(request, 'productos/crear.html',{'formulario':formulario})

def producto_creado_modelo(formulario):
    producto_creado = False
    
    if(formulario.is_valid()):
        try:
            formulario.save()
            producto_creado = True
        
        except Exception as error:    
            print(error)
        
        return producto_creado

#VIEW DE CALZADO CREAR

def calzado_crear(request):
    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST
    formulario = CalzadoForm(datosFormulario)

    if request.method == 'POST':
        calzado_creado = calzado_creado_modelo(formulario)
        if calzado_creado:
            messages.success(request, 'Calzado añadido con éxito')
            return redirect('lista_calzados')

    return render(request, 'calzados/crear.html', {'formulario': formulario})

def calzado_creado_modelo(formulario):
    calzado_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            calzado_creado = True
        except Exception as error:
            print(error)

    return calzado_creado

#MUEBLE CREAR


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
