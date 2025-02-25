from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuario/registrar', views.registrar_usuario, name='registrar_usuario'),
    # path('productos/listar', views.listar_productos, name='lista_productos'),
    # path('producto/<int:id_producto>/', views.muestra_producto, name="muestra_producto"),
    # path('usuarios/listar', views.usuarios_listar, name="usuarios_listar"),
   
    
    # registro    

    # CRUD usuario
    # path('usuario/buscar', views.usuario_buscar, name="usuario_buscar"),
    # path('usuarios/actualizar/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),
    # path('usuario/eliminar/<int:usuario_id>/', views.usuario_eliminar, name='usuario_eliminar'),
    
    # CRUD categoria
    # path('categoria/crear', views.categoria_crear, name='categoria_crear'),
    # path('categoria/buscar', views.categoria_buscar, name='categoria_buscar'),
    # path('categorias/actualizar/<int:categoria_id>/', views.categoria_editar, name='categoria_editar'),
    # path('categoria/eliminar/<int:categoria_id>/', views.categoria_eliminar, name='categoria_eliminar'),

    # CRUD producto
    # path('producto/crear', views.producto_crear, name='producto_crear'),
    # path('producto/buscar', views.producto_buscar, name='producto_buscar'),
    # path('producto/actualizar/<int:producto_id>/', views.producto_editar, name='producto_editar'),
    # path('producto/eliminar/<int:producto_id>/', views.producto_eliminar, name='producto_eliminar'),
  
]