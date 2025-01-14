from django.urls import path,re_path
from .import views

    
urlpatterns = [

    path('',views.index,name='index'),

    path('productos/listar',views.listar_productos,name='lista_productos'),
 
    path('producto/<int:id_producto>/', views.muestra_producto,name="muestra_producto"),

    path('usuarios/listar',views.usuarios_listar,name="usuarios_listar"),

    path('consolas/', views.lista_consolas, name='lista_consolas'),
    
    path('categorias/',views.categoria_listar, name="'categoria_listar"),
    
    path('muebles/listar', views.muebles_listar, name="muebles_listar"),
     
    path('calzados/listar', views.calzados_listar, name="calzados_listar"),
    
    #registro    
    path('usuario/registrar',views.registrar_usuario, name='registrar_usuario'),

    #CRUD usuario
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