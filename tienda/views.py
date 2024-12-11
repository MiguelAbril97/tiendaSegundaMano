from django.shortcuts import render,redirect
from django.db.models import Q,F,Prefetch
from django.db.models import Avg,Max,Min
from django.db.models import Count
from .models import *
from .forms import *
from django.contrib import messages
from django.views.defaults import page_not_found, permission_denied, bad_request, server_error
from datetime import datetime



#
#       VIEWS DE CRUD LINEA 100
#

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


#####################################################################
#####################################################################
##VIEWS DE CRUD


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

#view Usuario buscar 

def usuario_buscar(request):
    if(len(request.GET) > 0):
        formulario = BuscarUsuario(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSusuarios = Usuario.objects.prefetch_related(Prefetch('producto_vendedor'))
            
            nombre = formulario.cleaned_data.get('buscarNombre')
            email = formulario.cleaned_data.get('buscarEmail')
            tlf = formulario.cleaned_data.get('buscarTlf')
            direccion = formulario.cleaned_data.get('buscarDireccion')
            
            if(nombre != ""):
                QSusuarios = QSusuarios.filter(nombre__contains = nombre)
                mensaje_busqueda += "Nombre que contiene:"+nombre+"\n"
                
            if(email != ""):
                QSusuarios = QSusuarios.filter(email__contains = email)
                mensaje_busqueda += "Email que contiene:"+email+"\n"
            
            if(tlf != ""):
                QSusuarios = QSusuarios.filter(telefono__contains = tlf)
                mensaje_busqueda += "Telefono que contiene:"+tlf+"\n"
                
            if(direccion != ""):
                QSusuarios = QSusuarios.filter(direccion__contains = direccion)
                mensaje_busqueda += "Direccion que contiene:"+direccion+"\n"
            
            usuarios = QSusuarios.all()
            
            return render(request,'usuarios/lista.html',{'usuarios_mostrar':usuarios,'mensaje':mensaje_busqueda})
    else:
        formulario = BuscarUsuario(None) 
    return render(request, 'usuarios/buscar.html',{'formulario':formulario})    


###Usuario editar

def usuario_editar(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = UsuarioForm(datosFormulario,instance = usuario)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el usuario'+formulario.cleaned_data.get('correo_electronico')+" correctamente")
                return redirect('usuarios_listar')  
            except Exception as error:
                print(error)
    return render(request, 'usuarios/actualizar.html',{"formulario":formulario,"usuario":usuario}) 
                
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
            return redirect('index')
    
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

#Categoria buscar

def categoria_buscar(request):
    if(len(request.GET) > 0):
        formulario = BuscarCategoria(request.GET)
    
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            QScategorias = Categoria.objects.prefetch_related(Prefetch('categorias'))
            
            nombre = formulario.cleaned_data('buscarNombre')
            descripcion = formulario.cleaned_data('buscarDescripcion')
            existencias = formulario.cleaned_data('sinExistencias')
            destacada = formulario.cleaned_data('destacada')

            if(nombre != ""):
                QScategorias = QScategorias.filter(nombre__contains = nombre)
                mensaje_busqueda += "Nombre contiene"+nombre+"\n"
                
            if(descripcion != ""):
                QScategorias = QScategorias.filter(descripcion__contains = descripcion)
                mensaje_busqueda += "Descripcion contiene"+nombre+"\n"
                
            if(existencias):
                QScategorias = QScategorias.filter(existencias__gte = 0)
                mensaje_busqueda += "Incluir categorias sin existencias"+"\n"

            else:
                QScategorias = QScategorias.filter(existencias__gt = 0)
                mensaje_busqueda += "Excluir categorias sin existencias"+"\n"

            if(destacada):
                QScategorias = QScategorias.filter(destacada = True)
                mensaje_busqueda += "Solo categorias destacadas"+"\n"

            else:
                QScategorias = QScategorias.filter(Q (destacada = False) | Q (destacada = False))
                mensaje_busqueda += "Categorias destacadas y no destacadas"+"\n"
                
            return render(request, 'categoria/lista.html',
                          {'formulario':formulario, 'mensaje':mensaje_busqueda})
    else:
        formulario = BuscarCategoria(None)
            
    return render(request, 'categoria/buscar.html',
                          {'formulario':formulario})
        
def categoria_editar (request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = CategoriaForm(datosFormulario,instance = categoria)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la categoría'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('index')  
            except Exception as error:
                print(error)
    return render(request, 'categoria/actualizar.html',{"formulario":formulario,"categoria":categoria}) 

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
    
#Producto buscar

def producto_buscar(request):
    
    if(len(request.GET) > 0):
        formulario = BuscarProducto(request.GET)
        
        if formulario.is_valid():            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSproductos = Producto.objects.select_related('vendedor').prefetch_related('categorias')
            
            nombre = formulario.cleaned_data.get('buscarNombre')
            descripcion = formulario.cleaned_data.get('buscarDescripcion')
            precio = formulario.cleaned_data.get('buscarPrecioMax')
            estado = formulario.cleaned_data.get('buscarEstado')
            vendedor = formulario.cleaned_data.get('buscarVendedor')
            fecha = formulario.cleaned_data.get('buscarFecha')
            categoria = formulario.cleaned_data.get('buscarCategorias')
            
            if(nombre != ""):
                QSproductos = QSproductos.filter(nombre__contains = nombre)
                mensaje_busqueda +=" Nombre que contenga "+nombre+"\n"
            
            if(descripcion != ""):
                QSproductos = QSproductos.filter(descripcion__contains = descripcion)
                mensaje_busqueda +=" Descripcion que contenga "+descripcion+"\n"
            
            if (precio is not None):
                QSproductos = QSproductos.filter(precio__lte = precio)
                mensaje_busqueda += "Precio menor o igual a "+precio+"\n"    
          
            if(len(estado) > 0):
                mensaje_busqueda +="El estado sea "+estado[0]
                filtroOR = Q(i=estado[0])
                for i in estado[1:]:
                    mensaje_busqueda += " o "+i
                    filtroOR |= Q(i=i)
                mensaje_busqueda += "\n"
                QSproductos =  QSproductos.filter(filtroOR)
            
            if(len(vendedor) > 0 ):
                mensaje_busqueda +="Vendedores: {vendedor[0].email}"
                filtroOR = Q(vendedor=vendedor[0])
                for i in vendedor[1:]:
                    mensaje_busqueda += " o {i[0].email}"
                    filtroOR |= Q(vendedor=i)
                mensaje_busqueda += "\n"
                QSproductos = QSproductos.filter(filtroOR)
                        
            if(not fecha is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha,'%d-%m-%Y')+"\n"
                QSproductos = QSproductos.filter(fecha_de_publicacion__gte=fecha)
            
            if(len(categoria) > 0):
                mensaje_busqueda +="Categorias: {categoria[0].nombre}"
                filtroOR = Q(categorias = categoria)
                for i in vendedor[1:]:
                    mensaje_busqueda += " o {i[0].nombre}"
                    filtroOR |= Q(categorias = i)
                mensaje_busqueda += "\n"
                QSproductos = QSproductos.filter(filtroOR)
        
            return render(request, 'productos/lista.html',
                          {'formulario':formulario, 'mensaje':mensaje_busqueda})
    else:
        formulario = BuscarProducto(None)
            
    return render(request, 'productos/buscar.html',
                        {'formulario':formulario})
                
#Producto editar
def producto_editar (request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = ProductoForm(datosFormulario,instance = producto)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el producto'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('productos_listar')  
            except Exception as error:
                print(error)
    return render(request, 'productos/actualizar.html',{"formulario":formulario,"producto":producto}) 


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
            return redirect('index')

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

def calzado_buscar(request):
    if(len(request.GET) > 0):
        formulario = BuscarCalzado(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSCalzado = Calzado.objects.all()
            
            talla = formulario.cleaned_data.get('buscarTalla')
            marca = formulario.cleaned_data.get('buscarMarca')
            color = formulario.cleaned_data.get('buscarColor')
            material = formulario.cleaned_data.get('buscarMaterial')
            precio_max = formulario.cleaned_data.get('buscarPrecioMax')
            
            if(talla != ""):
                QSCalzado = QSCalzado.filter(talla__contains=talla)
                mensaje_busqueda += "Talla que contiene:" + talla + "\n"
                
            if(marca != ""):
                QSCalzado = QSCalzado.filter(marca=marca)
                mensaje_busqueda += "Marca seleccionada:" + marca + "\n"
            
            if(color != ""):
                QSCalzado = QSCalzado.filter(color__contains=color)
                mensaje_busqueda += "Color que contiene:" + color + "\n"
            
            if(material != ""):
                QSCalzado = QSCalzado.filter(material__contains=material)
                mensaje_busqueda += "Material que contiene:" + material + "\n"
            
            if(precio_max != None):
                QSCalzado = QSCalzado.filter(precio__lte=precio_max)
                mensaje_busqueda += "Precio máximo:" + str(precio_max) + "\n"
            
            calzados = QSCalzado.all()
            
            return render(request, 'calzados/lista.html', {'calzados': calzados, 'mensaje': mensaje_busqueda})
    else:
        formulario = BuscarCalzado(None) 
    
    return render(request, 'calzados/buscar.html', {'formulario': formulario})

#Editar calzado
def calzado_editar(request, calzado_id):
    calzado = Calzado.objects.get(id=calzado_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
    
    formulario = CalzadoForm(datosFormulario, instance=calzado)
    
    if (request.method == "POST"):
        if (formulario.is_valid()):
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el calzado correctamente')
                return redirect('index')
            except Exception as error:
                print(error)
    
    return render(request, 'calzados/actualizar.html', {"formulario": formulario, "calzado": calzado})


#MUEBLE CREAR

def mueble_crear(request):
    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST
    formulario = MuebleForm(datosFormulario)

    if request.method == 'POST':
        mueble_creado = mueble_creado_modelo(formulario)
        if mueble_creado:
            messages.success(request, 'Mueble añadido con éxito')
            return redirect('index')

    return render(request, 'muebles/crear.html', {'formulario': formulario})

def mueble_creado_modelo(formulario):
    mueble_creado = False

    if formulario.is_valid():
        try:
            formulario.save()
            mueble_creado = True
        except Exception as error:
            print(error)

    return mueble_creado


#Buscar mueble

def mueble_buscar(request):
    if(len(request.GET) > 0):
        formulario = BuscarMueble(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSMueble = Muebles.objects.all()
            
            material = formulario.cleaned_data.get('buscarMaterial')
            ancho_min = formulario.cleaned_data.get('buscarAnchoMin')
            ancho_max = formulario.cleaned_data.get('buscarAnchoMax')
            alto_min = formulario.cleaned_data.get('buscarAltoMin')
            alto_max = formulario.cleaned_data.get('buscarAltoMax')
            profundidad_min = formulario.cleaned_data.get('buscarProfundidadMin')
            profundidad_max = formulario.cleaned_data.get('buscarProfundidadMax')
            peso_max = formulario.cleaned_data.get('buscarPesoMax')
            
            if(material != ""):
                QSMueble = QSMueble.filter(material__contains=material)
                mensaje_busqueda += "Material que contiene:" + material + "\n"
            
            if(ancho_min is not None):
                QSMueble = QSMueble.filter(ancho__gte=ancho_min)
                mensaje_busqueda += "Ancho mínimo:" + str(ancho_min) + "\n"
                
            if(ancho_max is not None):
                QSMueble = QSMueble.filter(ancho__lte=ancho_max)
                mensaje_busqueda += "Ancho máximo:" + str(ancho_max) + "\n"
            
            if(alto_min is not None):
                QSMueble = QSMueble.filter(alto__gte=alto_min)
                mensaje_busqueda += "Alto mínimo:" + str(alto_min) + "\n"
                
            if(alto_max is not None):
                QSMueble = QSMueble.filter(alto__lte=alto_max)
                mensaje_busqueda += "Alto máximo:" + str(alto_max) + "\n"
            
            if(profundidad_min is not None):
                QSMueble = QSMueble.filter(profundidad__gte=profundidad_min)
                mensaje_busqueda += "Profundidad mínima:" + str(profundidad_min) + "\n"
                
            if(profundidad_max is not None):
                QSMueble = QSMueble.filter(profundidad__lte=profundidad_max)
                mensaje_busqueda += "Profundidad máxima:" + str(profundidad_max) + "\n"
            
            if(peso_max is not None):
                QSMueble = QSMueble.filter(peso__lte=peso_max)
                mensaje_busqueda += "Peso máximo:" + str(peso_max) + "\n"
            
            muebles = QSMueble.all()
            
            return render(request, 'muebles/lista.html', {'muebles': muebles, 'mensaje': mensaje_busqueda})
    else:
        formulario = BuscarMueble(None)
    
    return render(request, 'muebles/buscar.html', {'formulario': formulario})

#Editar mueble_buscar

def mueble_editar(request, mueble_id):
    mueble = Muebles.objects.get(id=mueble_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
    
    formulario = MuebleForm(datosFormulario, instance=mueble)
    
    if (request.method == "POST"):
        if (formulario.is_valid()):
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el mueble')
                return redirect('index') 
            except Exception as error:
                print(error)
    
    return render(request, 'muebles/actualizar.html', {"formulario": formulario, "mueble": mueble})


#Consola_crear
def consola_crear(request):
    datosFormulario = None

    if request.method == 'POST':
        datosFormulario = request.POST
    formulario = ConsolasForm(datosFormulario)

    if request.method == 'POST':
        consola_creada = consola_creada_modelo(formulario)
        if consola_creada:
            messages.success(request, 'Consola añadida con éxito')
            return redirect('lista_consolas')

    return render(request, 'consolas/crear.html', {'formulario': formulario})

def consola_creada_modelo(formulario):
    consola_creada = False

    if formulario.is_valid():
        try:
            formulario.save()
            consola_creada = True
        except Exception as error:
            print(error)

    return consola_creada

#Buscar consola

def consola_buscar(request):
    if(len(request.GET) > 0):
        formulario = BuscarConsola(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSConsola = Consolas.objects.all()
            
            modelo = formulario.cleaned_data.get('buscarModelo')
            color = formulario.cleaned_data.get('buscarColor')
            memoria = formulario.cleaned_data.get('buscarMemoria')
            precio_max = formulario.cleaned_data.get('buscarPrecioMax')
            
            if(modelo != ""):
                QSConsola = QSConsola.filter(modelo__contains=modelo)
                mensaje_busqueda += "Modelo que contiene:" + modelo + "\n"
                
            if(color != ""):
                QSConsola = QSConsola.filter(color__contains=color)
                mensaje_busqueda += "Color que contiene:" + color + "\n"
            
            if(memoria != ""):
                QSConsola = QSConsola.filter(memoria__contains=memoria)
                mensaje_busqueda += "Memoria que contiene:" + memoria + "\n"
                
            if(precio_max is not None):
                QSConsola = QSConsola.filter(precio__lte=precio_max)
                mensaje_busqueda += "Precio máximo:" + str(precio_max) + "\n"
            
            consolas = QSConsola.all()
            
            return render(request, 'consolas/lista.html', {'consolas': consolas, 'mensaje': mensaje_busqueda})
    else:
        formulario = BuscarConsola(None)
    
    return render(request, 'consolas/buscar.html', {'formulario': formulario})


def consola_editar(request, consola_id):
    consola = Consolas.objects.get(id=consola_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
    
    formulario = ConsolasForm(datosFormulario, instance=consola)
    
    if (request.method == "POST"):
        if (formulario.is_valid()):
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la consola correctamente.')
                return redirect('lista_consolas')
            except Exception as error:
                print(error)
    
    return render(request, 'consolas/actualizar.html', {"formulario": formulario, "consola": consola})


##Todos los delete

def usuario_eliminar (request,usuario_id):
    usuario = Usuario.objects.get(usuario_id)
    try:
        usuario.delete()
    except:
        pass
    return redirect('usuarios_lista')

def categoria_eliminar(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    try:
        categoria.delete()
    except:
        pass
    return redirect('categorias_lista')  # Cambiar por la URL correspondiente para listar categorías


def producto_eliminar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        producto.delete()
    except:
        pass
    return redirect('productos_lista')

def calzado_eliminar(request, calzado_id):
    calzado = Calzado.objects.get(id=calzado_id)
    try:
        calzado.delete()
    except:
        pass
    return redirect('index')

def mueble_eliminar(request, mueble_id):
    mueble = Muebles.objects.get(id=mueble_id)
    try:
        mueble.delete()
    except:
        pass
    return redirect('index')

def consola_eliminar(request, consola_id):
    consola = Consolas.objects.get(id=consola_id)
    try:
        consola.delete()
    except:
        pass
    return redirect('lista_consolas')







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
