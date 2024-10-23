from django.urls import path,re_path
from .import views
 
"""path('',views.index,name='index'),
    path("libros/listar/<str:idioma>/", views.dame_libros_idioma,name="dame_libros_idioma"),
    path("biblioteca/<int:id_biblioteca>/libros/<str:texto_libro>", views.dame_libros_biblioteca,name="dame_libros_biblioteca"),
    path('biblioteca/<int:id_biblioteca>/',views.dame_biblioteca,name='dame_biblioteca'),
    path('ultimo-cliente-libro/<int:libro>',views.dame_ultimo_cliente_libro,name='ultimo_cliente_libro'),
    path('dame-libros-titulo-descripcion',views.dame_libros_titulo_en_descripcion,name="dame_libros_titulo_en_descripcion"),
    path('dame-agrupaciones-puntos-clientes',views.dame_agrupaciones_puntos_cliente,name="dame_agrupaciones_puntos_cliente"),
    re_path(r"^filtro[0-9]$", views.libros_no_prestados,name="libros_no_prestados"),"""
urlpatterns = [
    path('',views.index,name='index'),
    path('productos/listar',views.listar_productos,name='lista_productos'),
    path('productos/<int:id_producto>/', views.muestra_producto,name="muestra_producto"),
    path('productos/<int:anyo>/<int:mes>', views.listar_productos_fecha, name="lista_productos_fecha"),
]