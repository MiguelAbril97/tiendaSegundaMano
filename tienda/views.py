from django.shortcuts import render,redirect
from django.db.models import Q,F,Prefetch
from django.db.models import Avg,Max,Min
from django.db.models import Count
from .models import *
from .forms import *
from django.contrib import messages
from django.views.defaults import page_not_found, permission_denied, bad_request, server_error
from datetime import datetime
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group


# Preguntar que es lo de las fechas en su view de index y preguntas en la 
#view de registrar
#
def index(request):
    return render(request, "index.html")

#3 Esta view muestra toda la informacion de un producto
# def muestra_producto(request, id_producto):
#     producto = Producto.objects.select_related("vendedor").prefetch_related("categorias", Prefetch('producto_compra')).get(id=id_producto)
#     return render(request, "productos/producto.html", {"producto":producto})

# def categoria_listar(request):
#     categorias = Categoria.objects.prefetch_related(Prefetch("categorias")).all()
#     return render(request, 'categoria/lista.html',{'categorias':categorias})

# def listar_productos (request):
#     if(request.user.rol == 2):
#         productos = Producto.objects.select_related(
#                 'vendedor').prefetch_related('categorias'
#                                              ).exclude(producto_compra__comprador=request.user)
#     elif(request.user.rol == 3):
#         productos = Producto.objects.select_related(
#                 'vendedor').prefetch_related('categorias'
#                                              ).filter(vendedor=request.user)
#     else:
#         productos = Producto.objects.select_related(
#                 'vendedor').prefetch_related('categorias')
#     total = productos.aggregate(Count('id'))
#     return render(request, "productos/lista.html", {"productos":productos, 'total':total})

# def usuarios_listar(request):
#     usuarios = Usuario.objects.prefetch_related(Prefetch('producto_vendedor')).all()
#     return render(request, 'usuarios/lista.html',{'usuarios':usuarios})



#####################################################################
#####################################################################
##VIEWS DE CRUD


#VIEW USUARIO CREAR 

#Preguntar como mostrar los datos en el formulario 
# segun lo que escoja el usuario en el formulario

#Preguntar tambien si lo de formulario.cleaned_data.get('nombre') esta bien
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if (formulario.is_valid()):
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))            
            if (rol == Usuario.COMPRADOR):
                grupo = Group.objects.get(name='Compradores')
                grupo.user_set.add(user)
                comprador = Comprador.objects.create(
                    usuario=user,
                    nombre=formulario.cleaned_data.get('nombre'),
                    apellidos=formulario.cleaned_data.get('apellidos'),
                )
                comprador.save()
            elif rol == Usuario.VENDEDOR:
                grupo = Group.objects.get(name='Vendedores')
                grupo.user_set.add(user)
                vendedor = Vendedor.objects.create(
                    usuario=user,
                    razonSocial=formulario.cleaned_data.get('razonSocial'),
                    direccionFiscal=formulario.cleaned_data.get('direccionFiscal'),
                )
                vendedor.save()

                login(request, user)
            return redirect('index')
    else:
        formulario = UsuarioForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

   
"""
# def usuario_crear(request): 
#     datosFormulario = None
   
#     if(request.method == "POST"):
#         datosFormulario = request.POST
#     formulario = UsuarioForm(datosFormulario)
    
#     if(request.method == 'POST'):
#         usuario_creado = crear_usuario_modelo(formulario)
        
#         if(usuario_creado):
#             messages.success(request,"Usuario creado")
#             return redirect('usuarios_listar')
        
#     return render(request, 'usuarios/crear.html',{"formulario":formulario})

# def crear_usuario_modelo(formulario):
#     usuario_creado = False
    
#     if formulario.is_valid():
#         try:
#             formulario.save()
#             usuario_creado = True
#         except Exception as error:
#             print(error)
#     return usuario_creado
"""

#view Usuario buscar 
# @permission_required('tienda.view_user')
# def usuario_buscar(request):
#     if(len(request.GET) > 0):
#         formulario = BuscarUsuario(request.GET)
#         if formulario.is_valid():
#             mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
#             QSusuarios = Usuario.objects.prefetch_related(Prefetch('producto_vendedor'))
            
#             nombre = formulario.cleaned_data.get('buscarNombre')
#             email = formulario.cleaned_data.get('buscarEmail')
#             tlf = formulario.cleaned_data.get('buscarTlf')
#             direccion = formulario.cleaned_data.get('buscarDireccion')
            
#             if(nombre != ""):
#                 QSusuarios = QSusuarios.filter(nombre__contains = nombre)
#                 mensaje_busqueda += "Nombre que contiene:"+nombre+"\n"
                
#             if(email != ""):
#                 QSusuarios = QSusuarios.filter(email__contains = email)
#                 mensaje_busqueda += "Email que contiene:"+email+"\n"
            
#             if(tlf != ""):
#                 QSusuarios = QSusuarios.filter(telefono__contains = tlf)
#                 mensaje_busqueda += "Telefono que contiene:"+tlf+"\n"
                
#             if(direccion != ""):
#                 QSusuarios = QSusuarios.filter(direccion__contains = direccion)
#                 mensaje_busqueda += "Direccion que contiene:"+direccion+"\n"
            
#             usuarios = QSusuarios.all()
            
#             return render(request,'usuarios/lista.html',{'usuarios':usuarios,'mensaje':mensaje_busqueda})
#     else:
#         formulario = BuscarUsuario(None) 
#     return render(request, 'usuarios/buscar.html',{'formulario':formulario})    


###Usuario editar
# @permission_required('tienda.change_user')
# def usuario_editar(request,usuario_id):
#     usuario = Usuario.objects.get(id=usuario_id)
    
#     datosFormulario = None
    
#     if request.method == "POST":
#         datosFormulario = request.POST
    
    
#     formulario = UsuarioForm(datosFormulario,instance = usuario)
    
#     if (request.method == "POST"):
       
#         if formulario.is_valid():
#             try:  
#                 formulario.save()
#                 messages.success(request, 'Se ha editado el usuario'+formulario.cleaned_data.get('correo_electronico')+" correctamente")
#                 return redirect('usuarios_listar')  
#             except Exception as error:
#                 print(error)
#     return render(request, 'usuarios/actualizar.html',{"formulario":formulario,"usuario":usuario}) 
                
#View CATEGORIA CREAR
# @permission_required('tienda.add_categoria')
# def categoria_crear (request):
#     datosFormulario = None
#     if(request.method == "POST"):
#         datosFormulario = request.POST
#     formulario = CategoriaForm(datosFormulario)
    
#     if(request.method == 'POST'):
#         categoria_creada = crear_categoria_modelo(formulario)
#         if(categoria_creada):
#             messages.success(request, 'Se ha creado la categoria')
#             return redirect('categoria_listar')
    
#     return render(request, 'categoria/crear.html',{"formulario":formulario})

# def crear_categoria_modelo(formulario):
#     categoria_creada = False
    
#     if formulario.is_valid():
#         try:
#             formulario.save()
#             categoria_creada = True
#         except Exception as error:
#             print(error)
#         return categoria_creada

#Categoria buscar
# @permission_required('tienda.view_categoria')
# def categoria_buscar(request):
#     if(len(request.GET) > 0):
#         formulario = BuscarCategoria(request.GET)
    
#         if formulario.is_valid():
            
#             mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

#             QScategorias = Categoria.objects.prefetch_related(Prefetch('categorias'))
            
#             nombre = formulario.cleaned_data.get('buscarNombre')
#             descripcion = formulario.cleaned_data.get('buscarDescripcion')
#             existencias = formulario.cleaned_data.get('sinExistencias')
#             destacada = formulario.cleaned_data.get('destacada')

#             if(nombre != ""):
#                 QScategorias = QScategorias.filter(nombre__contains = nombre)
#                 mensaje_busqueda += "Nombre contiene"+nombre+"\n"
                
#             if(descripcion != ""):
#                 QScategorias = QScategorias.filter(descripcion__contains = descripcion)
#                 mensaje_busqueda += "Descripcion contiene"+nombre+"\n"
                
#             if(existencias):
#                 QScategorias = QScategorias.filter(existecias__gte = 0)
#                 mensaje_busqueda += "Incluir categorias sin existencias"+"\n"

#             else:
#                 QScategorias = QScategorias.filter(existecias__gt = 0)
#                 mensaje_busqueda += "Excluir categorias sin existencias"+"\n"

#             if(destacada):
#                 QScategorias = QScategorias.filter(destacada = True)
#                 mensaje_busqueda += "Solo categorias destacadas"+"\n"

#             else:
#                 QScategorias = QScategorias.filter(Q (destacada = False) | Q (destacada = False))
#                 mensaje_busqueda += "Categorias destacadas y no destacadas"+"\n"
                
            
#             categorias = QScategorias.all()
#             return render(request, 'categoria/lista.html',
#                           {'categorias':categorias, 'mensaje':mensaje_busqueda})
#     else:
#         formulario = BuscarCategoria(None)
            
#     return render(request, 'categoria/buscar.html',
#                           {'formulario':formulario})

# @permission_required('tienda.change_categoria') 
# def categoria_editar (request, categoria_id):
#     categoria = Categoria.objects.get(id=categoria_id)
    
#     datosFormulario = None
    
#     if request.method == "POST":
#         datosFormulario = request.POST
    
    
#     formulario = CategoriaForm(datosFormulario,instance = categoria)
    
#     if (request.method == "POST"):
       
#         if formulario.is_valid():
#             try:  
#                 formulario.save()
#                 messages.success(request, 'Se ha editado la categoría'+formulario.cleaned_data.get('nombre')+" correctamente")
#                 return redirect('categoria_listar')  
#             except Exception as error:
#                 print(error)
#     return render(request, 'categoria/actualizar.html',{"formulario":formulario,"categoria":categoria}) 

#View Producto CREAR
# @permission_required('tienda.add_producto')
# def producto_crear(request):
#     if(request.method == 'POST'):
#         formulario = ProductoForm(request.POST)
    
#         if formulario.is_valid():
#             try:
#                 producto = Producto.objects.create(
#                     nombre=formulario.cleaned_data.get('nombre'),
#                     descripcion=formulario.cleaned_data.get('descripcion'),
#                     precio=formulario.cleaned_data.get('precio'),
#                     estado=formulario.cleaned_data.get('estado'),
#                     vendedor=request.user,
#                 )
#                 producto.categorias.set(formulario.cleaned_data.get('categorias'))
#                 producto.save()
#                 return redirect('lista_productos')
#             except Exception as error:
#                     print(error)
#     else:
#         formulario = ProductoForm()
#     return render(request, 'productos/crear.html',{'formulario':formulario})

#Producto buscar

# @permission_required('tienda.view_producto')
# def producto_buscar(request):
#     if(len(request.GET) > 0):
#         formulario = BuscarProducto(request.GET,request=request)

#         if formulario.is_valid():
#             mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
#             if(request.user.rol == 2):
#                 QSproductos = Producto.objects.select_related(
#                 'vendedor').prefetch_related('categorias'
#                                              ).exclude(producto_compra__comprador=request.user)
#             elif(request.user.rol == 3):
#                 QSproductos = Producto.objects.select_related(
#                 'vendedor').prefetch_related('categorias'
#                                              ).filter(vendedor=request.user)
#             else:
#                 QSproductos = Producto.objects.select_related(
#                 'vendedor').prefetch_related('categorias')
                
#             nombre = formulario.cleaned_data.get('buscarNombre')
#             descripcion = formulario.cleaned_data.get('buscarDescripcion')
#             precio = formulario.cleaned_data.get('buscarPrecioMax')
#             estado = formulario.cleaned_data.get('buscarEstado')
#             vendedor = formulario.cleaned_data.get('buscarVendedor')
#             fecha = formulario.cleaned_data.get('buscarFecha')
#             categoria = formulario.cleaned_data.get('buscarCategorias')

#             if(nombre != ""):
#                 QSproductos = QSproductos.filter(nombre__icontains=nombre)
#                 mensaje_busqueda +=" Nombre que contenga "+nombre+"\n"

#             if(descripcion != ""):
#                 QSproductos = QSproductos.filter(descripcion__icontains=descripcion)
#                 mensaje_busqueda +=" Descripcion que contenga "+descripcion+"\n"

#             if(precio is not None):
#                 QSproductos = QSproductos.filter(precio__lte=precio)
#                 mensaje_busqueda += "Precio menor o igual a "+str(precio)+"\n"

#             if(len(estado) > 0):
#                 QSproductos = QSproductos.filter(estado__in=estado)
#                 mensaje_busqueda +=" El estado sea "+estado[0]
#                 for i in estado[1:]:
#                     mensaje_busqueda += " o "+i
#                 mensaje_busqueda += "\n"

#             if(len(vendedor) > 0):
#                 QSproductos = QSproductos.filter(vendedor__in=vendedor)
#                 mensaje_busqueda +=" Vendedores: "+vendedor[0].email
#                 for v in vendedor[1:]:
#                     mensaje_busqueda += " o "+v.email
#                 mensaje_busqueda += "\n"

#             if(not fecha is None):
#                 QSproductos = QSproductos.filter(fecha_de_publicacion__gte=fecha)
#                 mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha, '%d-%m-%Y')+"\n"

#             if(len(categoria) > 0):
#                 QSproductos = QSproductos.filter(categorias__in=categoria)
#                 mensaje_busqueda +=" Categorias: "+categoria[0].nombre
#                 for c in categoria[1:]:
#                     mensaje_busqueda += " o "+c.nombre
#                 mensaje_busqueda += "\n"
        
#             productos = QSproductos.all()
#             return render(request, 'productos/lista.html',
#                           { 'mensaje': mensaje_busqueda, 'productos': productos})

#     else:
#         formulario = BuscarProducto(None,request=request)

#     return render(request, 'productos/buscar.html', {'formulario': formulario})

                
#Producto editar
# @permission_required('tienda.change_producto')
# def producto_editar (request, producto_id):
#     producto = Producto.objects.get(id=producto_id)
    
#     datosFormulario = None
    
#     if request.method == "POST":
#         datosFormulario = request.POST
    
    
#     formulario = ProductoForm(datosFormulario,instance = producto)
    
#     if (request.method == "POST"):
       
#         if formulario.is_valid():
#             try:  
#                 formulario.save()
#                 messages.success(request, 'Se ha editado el producto'+formulario.cleaned_data.get('nombre')+" correctamente")
#                 return redirect('lista_productos')  
#             except Exception as error:
#                 print(error)
#     return render(request, 'productos/actualizar.html',{"formulario":formulario,"producto":producto}) 

##Todos los delete
# @permission_required('tienda.delete_user')
# def usuario_eliminar (request,usuario_id):
#     usuario = Usuario.objects.get(usuario_id)
#     try:
#         usuario.delete()
#     except:
#         pass
#     return redirect('usuarios_listar')

# @permission_required('tienda.delete_categoria')
# def categoria_eliminar(request, categoria_id):
#     categoria = Categoria.objects.get(id=categoria_id)
#     try:
#         categoria.delete()
#     except:
#         pass
#     return redirect('categoria_listar') 

# @permission_required('tienda.delete_producto')
# def producto_eliminar(request, producto_id):
#     producto = Producto.objects.get(id=producto_id)
#     try:
#         producto.delete()
#     except:
#         pass
#     return redirect('lista_productos')



##Crear una página de Error personalizada para cada uno de los 4 
# tipos de errores que pueden ocurrir en nuestra Web.

# def mi_error_400(request, exception=None):
#     return render(request, 'errores/400.html', None, None, 400)

# def mi_error_403(request, exception=None):
#     return render(request, 'errores/403.html', None, None, 403)

# def mi_error_404(request, exception=None):
#     return render(request, 'errores/404.html', None, None, 404)

# def mi_error_500(request):
#     return render(request, 'errores/500.html', None, None, 500)
