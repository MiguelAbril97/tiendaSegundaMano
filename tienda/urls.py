from django.urls import path,re_path
from .import views
 
"""path('',views.index,name='index'),
    path("libros/listar/<str:idioma>/", views.dame_libros_idioma,name="dame_libros_idioma"),
    path("biblioteca/<int:id_biblioteca>/libros/<str:texto_libro>", views.dame_libros_biblioteca,name="dame_libros_biblioteca"),
    path('biblioteca/<int:id_biblioteca>/',views.dame_biblioteca,name='dame_biblioteca'),
    path('ultimo-cliente-libro/<int:libro>',views.dame_ultimo_cliente_libro,name='ultimo_cliente_libro'),
    path('dame-libros-titulo-descripcion',views.dame_libros_titulo_en_descripcion,name="dame_libros_titulo_en_descripcion"),
    path('dame-agrupaciones-puntos-clientes',views.dame_agrupaciones_puntos_cliente,name="dame_agrupaciones_puntos_cliente"),
    re_path(r"^filtro[0-9]$", views.libros_no_prestados,name="libros_no_prestados"),
    
    Debe existir al menos una URL con r_path
    otra usando dos paramétros CHECK 
    otra usando un parámetro entero CHECK
    y otra usando un parámetro str CHECK
    
    """

    
    
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
    path('consolas/', views.lista_consolas, name='lista_consolas'),
    #11
    re_path(r'^\w+[@]\w+.org/', views.usuarios_correo, name='usuarios_correo'),
]