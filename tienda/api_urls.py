from django.urls import path
from .api_views import *

urlpatterns = [
    path('categorias/',categoria_listar),
    path('productos/',producto_listar),
    
    ###Usuarios
    path("registrar/usuario",registrar_usuario.as_view()),
    
    path('productos/<int:producto_id>/',obtener_producto),
    path('compras/<int:compra_id>/',obtener_compra),
    path('valoraciones/<int:valoracion_id>/',obtener_valoracion),
    
    path('productos-mejorado/',producto_listar_mejorado),
    path('productos/buscar_simple/',producto_buscar_simple),
    path('productos/buscar_avanzada/',producto_buscar),
    
    
    path('productos/crear/',producto_crear),
    path('productos/editar/<int:producto_id>/',producto_editar),
    path('productos/actualizar/<int:producto_id>/',producto_actualizar_nombre),
    path('productos/eliminar/<int:producto_id>/',producto_eliminar),
    
    path('compras/listar/',compra_listar),
   
    path('valoraciones/listar/',valoraciones_listar), 
    path('valoraciones/crear/',valoracion_crear),
    path('valoraciones/editar/<int:valoracion_id>/',valoracion_editar),
    path('valoraciones/actualizar/<int:valoracion_id>/',valoracion_actualizar_puntuacion),
    path('valoraciones/eliminar/<int:valoracion_id>/',valoracion_eliminar),
    
    path('vendedores/listar/',vendedores_listar),
    path('compradores/listar/',compradores_listar),

]