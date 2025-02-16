from django.urls import path
from .api_views import *

urlpatterns = [
    path('categorias/',categoria_listar),
    path('productos/',producto_listar),
    
    path('productos/<int:id>/',obtener_producto),
    path('compras/<int:id>/',obtener_compra),
    path('valoraciones/<int:id>/',obtener_valoracion),
    
    path('productos-mejorado/',producto_listar_mejorado),
    path('productos/buscar_simple/',producto_buscar_simple),
    path('productos/buscar_avanzada/',producto_buscar),
    
    
    path('productos/crear/',producto_crear),
    path('productos/editar/<int:id>/',producto_editar),
    path('productos/actualizar/<int:id>/',producto_actualizar_nombre),
    path('productos/eliminar/<int:id>/',producto_eliminar),
    
    path('compras/listar/',compra_listar),
    path('compras/crear/',compra_crear),
    path('compras/editar/<int:id>/',compra_editar),
    path('compras/actualizar/<int:id>/',compra_actualizar_garantia),
    path('compras/eliminar/<int:id>/',compra_eliminar),
    
    path('valoraciones/crear/',valoracion_crear),
    path('valoraciones/editar/<int:id>/',valoracion_editar),
    path('valoraciones/actualizar/<int:id>/',valoracion_actualizar_puntuacion),
    path('valoraciones/eliminar/<int:id>/',valoracion_eliminar),
    
    path('vendedores/listar/',vendedores_listar),
    path('compradores/listar/',compradores_listar),
    
    
    path('calzados/',calzado_listar),
    path('calzados/buscar/',calzado_buscar),
    path('calzados/crear/',calzado_crear),
    path('consolas/',consolas_listar),
    path('consolas/buscar/',consola_buscar),
    path('consolas/crear', consola_crear),
    path('muebles/',mueble_listar),
    path('muebles/buscar/',mueble_buscar),
    path('muebles/crear/',mueble_crear),
    
]