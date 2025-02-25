from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Vendedor)
admin.site.register(Comprador)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(ProductoCategoria)
admin.site.register(Chat)
admin.site.register(Compra)
admin.site.register(Envio)
admin.site.register(Valoracion)
