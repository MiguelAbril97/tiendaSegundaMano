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
    path('usuarios/actualizar/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),
    path('usuario/eliminar/<int:usuario_id>/', views.usuario_eliminar, name='usuario_eliminar'),
    

    
    #CRUD categoria
    path('categoria/crear',views.categoria_crear,name='categoria_crear'),
    path('categoria/buscar', views.categoria_buscar, name='categoria_buscar'),
    path('categorias/actualizar/<int:categoria_id>/', views.categoria_editar, name='categoria_editar'),
    path('categoria/eliminar/<int:categoria_id>/', views.categoria_eliminar, name='categoria_eliminar'),

    
    #CRUD producto
    path('producto/crear', views.producto_crear, name='producto_crear'),
    path('producto/buscar', views.producto_buscar, name='producto_buscar'),
    path('producto/actualizar/<int:producto_id>/', views.producto_editar, name='producto_editar'),
    path('producto/eliminar/<int:producto_id>/', views.producto_eliminar, name='producto_eliminar'),

    #CRUD calzado
    path('calzado/crear', views.calzado_crear, name='calzado_crear'),
    path('calzado/buscar', views.calzado_buscar, name='calzado_buscar'),
    path('calzado/actualizar/<int:calzado_id>/', views.calzado_editar, name='calzado_editar'),
    path('calzado/eliminar/<int:calzado_id>/', views.calzado_eliminar, name='calzado_eliminar'),


    #CRUD mueble
    path('mueble/crear', views.mueble_crear, name='mueble_crear'),
    path('mueble/buscar', views.mueble_buscar, name='mueble_buscar'),
    path('mueble/actualizar/<int:mueble_id>/', views.mueble_editar, name='mueble_editar'),
    path('mueble/eliminar/<int:mueble_id>/', views.mueble_eliminar, name='mueble_eliminar'),

    
    #CRUD consola
    path('consola/crear', views.consola_crear,name='consola_crear'),
    path('consola/buscar', views.consola_buscar,name='consola_buscar'),
    path('consola/actualizar/<int:consola_id>/', views.consola_editar, name='consola_editar'),
    path('consola/eliminar/<int:consola_id>/', views.consola_eliminar, name='consola_eliminar'),

]