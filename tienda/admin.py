from django.contrib import admin
from .models import *
# Register your models here.

admin.site(Usuario)
admin.site(Categoria)
admin.site(Producto)
admin.site(ProductoCategoria)
admin.site(Calzado)
admin.site(Muebles)
admin.site(Chat)
admin.site(Compra)
admin.site(CompraProducto)
admin.site(Envio)
admin.site(Valoracion)
