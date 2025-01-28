from django.urls import path
from .api_views import *

urlpatterns = [
    path('productos/',producto_listar),
    path('productos-mejorado/',producto_listar_mejorado),
    path('calzados/',calzado_listar),
    path('consolas/',consolas_listar),
]