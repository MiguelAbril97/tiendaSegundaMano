from django.urls import path,re_path
from .import views

    
urlpatterns = [
    #1
    path('',views.index,name='index'),
    #2
    path('productos/listar',views.listar_productos,name='lista_productos'),
    #3
    path('producto/<int:id_producto>/', views.muestra_producto,name="muestra_producto"),
    #4
    path('productos/<int:anyo>/<int:mes>/', views.listar_productos_fecha, name="lista_productos_fecha"),
    #5
    path('productos/categoria/<str:nombre_categoria>/', views.listar_productos_categoria,name="lista_productos_categoria"),
    #6
    path('producto/ultimo/<int:anyo>/<int:mes>/', views.ultimo_producto_fecha, name="ultimo_producto_fecha"),
    #7
    path('productos/<str:nombre_categoria>/<int:precio_min>/', views.productos_categoria_precio,name="productos_categoria_precio"),
    #8
    path('usuario/sinproductos', views.usuario_sin_productos, name="usuario_sin_productos"),
    #9
    path('usuarios/listar',views.usuarios_listar,name="usuarios_listar"),
    #10
    re_path(r'^\w+[@]\w+.org/', views.usuarios_correo, name='usuarios_correo'),
    #11
    path('consolas/', views.lista_consolas, name='lista_consolas'),
    
    #URLS DE FORMULARIO#
    
    #CRUD usuario
    path('usuario/crear',views.usuario_crear, name='usuario_crear'),
    path('usuario/buscar',views.usuario_buscar,name="usuario_buscar"),
    
    #CRUD categoria
    path('categoria/crear',views.categoria_crear,name='categoria_crear'),
    path('categoria7buscar', views.categoria_buscar, name='categoria_buscar'),
    
    #CRUD producto
    path('producto/crear', views.producto_crear, name='producto_crear'),
    path('producto/buscar', views.producto_buscar, name='producto_buscar'),
    
    #CRUD calzado
    path('calzado/crear', views.calzado_crear, name='calzado_crear'),
    path('calzado/buscar', views.calzado_buscar, name='calzado_buscar'),


    #CRUD mueble
    path('mueble/crear', views.mueble_crear, name='mueble_crear'),
     path('mueble/buscar', views.mueble_buscar, name='mueble_buscar'),
    
    #CRUD consola
    path('consola/crear', views.consola_crear,name='consola_crear'),
    path('consola/buscar', views.consola_buscar,name='consola_buscar'),
]