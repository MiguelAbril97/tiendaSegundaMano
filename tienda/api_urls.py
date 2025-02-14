from django.urls import path
from .api_views import *

urlpatterns = [
    path('categorias/',categoria_listar),
    path('productos/',producto_listar),
    path('productos-mejorado/',producto_listar_mejorado),
    path('productos/buscar_simple/',producto_buscar_simple),
    path('productos/buscar_avanzada/',producto_buscar),
    path('productos/crear/',producto_crear),
    path('compras/listar/',compra_listar),
    path('compras/crear/',compra_crear),
    path('valoraciones/crear/',valoracion_crear),
    
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