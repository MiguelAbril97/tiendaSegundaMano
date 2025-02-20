from django.urls import path
from .api_views import *

urlpatterns = [
    path('categorias/',categoria_listar),
    path('productos/',producto_listar),
    
    path('productos/<int:producto_id>/',obtener_producto),
    path('compras/<int:compras_id>/',obtener_compra),
    path('valoraciones/<int:valoracion_id>/',obtener_valoracion),
    
    path('productos-mejorado/',producto_listar_mejorado),
    path('productos/buscar_simple/',producto_buscar_simple),
    path('productos/buscar_avanzada/',producto_buscar),
    
    
    path('productos/crear/',producto_crear),
    path('productos/editar/<int:producto_id>/',producto_editar),
    path('productos/actualizar/<int:producto_id>/',producto_actualizar_nombre),
    path('productos/eliminar/<int:producto_id>/',producto_eliminar),
    
    path('compras/listar/',compra_listar),
    path('compras/crear/',compra_crear),
    path('compras/editar/<int:compras_id>/',compra_editar),
    path('compras/actualizar/<int:compras_id>/',compra_actualizar_garantia),
    path('compras/eliminar/<int:compras_id>/',compra_eliminar),
    
    path('valoraciones/crear/',valoracion_crear),
    path('valoraciones/editar/<int:valoraciones_id>/',valoracion_editar),
    path('valoraciones/actualizar/<int:valoraciones_id>/',valoracion_actualizar_puntuacion),
    path('valoraciones/eliminar/<int:valoraciones_id>/',valoracion_eliminar),
    
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