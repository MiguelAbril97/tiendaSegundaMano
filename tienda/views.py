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
def muestra_producto(request, id_producto):
    producto = Producto.objects.select_related("vendedor").prefetch_related("categorias", Prefetch('producto_compra')).get(id=id_producto)
    return render(request, "productos/producto.html", {"producto":producto})

def categoria_listar(request):
    categorias = Categoria.objects.prefetch_related(Prefetch("categorias")).all()
    return render(request, 'categoria/lista.html',{'categorias':categorias})

def listar_productos (request):
    productos = Producto.objects.select_related("vendedor").prefetch_related(
        "categorias", Prefetch('producto_compra')).all()
    total = productos.aggregate(Count('id'))
    return render(request, "productos/lista.html", {"productos":productos, 'total':total})

def usuarios_listar(request):
    usuarios = Usuario.objects.prefetch_related(Prefetch('producto_vendedor')).all()
    return render(request, 'usuarios/lista.html',{'usuarios':usuarios})

def lista_consolas(request):
    consolas = Consolas.objects.select_related('producto','producto__vendedor').prefetch_related(
        Prefetch('producto__categorias') )
    return render(request, 'consolas/lista.html', {'consolas': consolas})

def muebles_listar(request):
    muebles = Muebles.objects.select_related('producto','producto__vendedor').all()
    return render(request, 'muebles/lista.html', {'muebles': muebles})

def calzados_listar(request):
    calzados = Calzado.objects.select_related('producto','producto__vendedor').all()
    return render(request, 'calzados/lista.html', {'calzados': calzados})



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
"""

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
            
            return render(request,'usuarios/lista.html',{'usuarios':usuarios,'mensaje':mensaje_busqueda})
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
            return redirect('categoria_listar')
    
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
            
            nombre = formulario.cleaned_data.get('buscarNombre')
            descripcion = formulario.cleaned_data.get('buscarDescripcion')
            existencias = formulario.cleaned_data.get('sinExistencias')
            destacada = formulario.cleaned_data.get('destacada')

            if(nombre != ""):
                QScategorias = QScategorias.filter(nombre__contains = nombre)
                mensaje_busqueda += "Nombre contiene"+nombre+"\n"
                
            if(descripcion != ""):
                QScategorias = QScategorias.filter(descripcion__contains = descripcion)
                mensaje_busqueda += "Descripcion contiene"+nombre+"\n"
                
            if(existencias):
                QScategorias = QScategorias.filter(existecias__gte = 0)
                mensaje_busqueda += "Incluir categorias sin existencias"+"\n"

            else:
                QScategorias = QScategorias.filter(existecias__gt = 0)
                mensaje_busqueda += "Excluir categorias sin existencias"+"\n"

            if(destacada):
                QScategorias = QScategorias.filter(destacada = True)
                mensaje_busqueda += "Solo categorias destacadas"+"\n"

            else:
                QScategorias = QScategorias.filter(Q (destacada = False) | Q (destacada = False))
                mensaje_busqueda += "Categorias destacadas y no destacadas"+"\n"
                
            
            categorias = QScategorias.all()
            return render(request, 'categoria/lista.html',
                          {'categorias':categorias, 'mensaje':mensaje_busqueda})
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
                return redirect('categoria_listar')  
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
            return render(request, 'productos/lista.html',
                          { 'mensaje': mensaje_busqueda, 'productos': productos})

    else:
        formulario = BuscarProducto(None)

    return render(request, 'productos/buscar.html', {'formulario': formulario})

                
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
                return redirect('lista_productos')  
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
            return redirect('calzados_listar')

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
            
            QSCalzado = Calzado.objects.select_related('producto','producto__vendedor')
            
            talla = formulario.cleaned_data.get('buscarTalla')
            marca = formulario.cleaned_data.get('buscarMarca')
            color = formulario.cleaned_data.get('buscarColor')
            material = formulario.cleaned_data.get('buscarMaterial')
            precio_max = formulario.cleaned_data.get('buscarPrecioMax')
            
            if(not talla is None):
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
                return redirect('calzados_listar')
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
            return redirect('muebles_listar')

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
            
            QSMueble = Muebles.objects.select_related('producto','producto__vendedor')
            
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
                return redirect('muebles_listar') 
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
            
            QSConsola = Consolas.objects.select_related('producto','producto__vendedor')
            
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
    return redirect('usuarios_listar')

def categoria_eliminar(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    try:
        categoria.delete()
    except:
        pass
    return redirect('categoria_listar')  # Cambiar por la URL correspondiente para listar categorías


def producto_eliminar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        producto.delete()
    except:
        pass
    return redirect('lista_productos')

def calzado_eliminar(request, calzado_id):
    calzado = Calzado.objects.get(id=calzado_id)
    try:
        calzado.delete()
    except:
        pass
    return redirect('calzados_listar')

def mueble_eliminar(request, mueble_id):
    mueble = Muebles.objects.get(id=mueble_id)
    try:
        mueble.delete()
    except:
        pass
    return redirect('muebles_listar')

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
