from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=60)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=9)
    direccion = models.CharField(max_length=150)
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class Producto(models.Model):
    ESTADOS=[
        ("CN", "Como nuevo"),
        ("U", "Usado"),
        ("MU", "Muy usado"),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS
    )
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_de_publicacion = models.DateTimeField(default=timezone.now)
    categorias = models.ManyToManyField(Categoria, through='ProductoCategoria')

class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Calzado(models.Model):
    MARCAS = [
        ("NIKE", "Nike"),
        ("ADID", "Adidas"),
        ("PUMA", "Puma"),
        ("RBK", "Reebok"),
        ("NB", "New Balance"),
        ("CLRK", "Clarks"),
        ("GUCCI", "Gucci"),
    ]
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=2)
    marca = models.CharField(
        max_length=5,
        choices=MARCAS
    )
    color = models.CharField(max_length=20, blank=True)


class Muebles(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    material = models.CharField(max_length=30)
    dimensiones = models.CharField(max_length=255)
    peso=models.IntegerField()

class Chat(models.Model):
    usuario1 = models.ForeignKey(Usuario, related_name='chat_usuario1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(Usuario, related_name='chat_usuario2', on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin= models.DateTimeField(blank=True)

class Compra(models.Model):
    comprador = models.ForeignKey(Usuario, related_name='compras_comprador', on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Usuario, related_name='compras_vendedor',      on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=7, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Envio(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    direccion=models.TextField()	
    fecha_envio = models.DateTimeField()
    fecha_recepcion = models.DateTimeField()

class Valoracion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True)
    fecha_valoracion = models.DateTimeField(default=timezone.now)


