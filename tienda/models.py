from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    COMPRADOR = 2
    VENDEDOR = 3
    ROLES = (
        (ADMINISTRADOR, 'administradores'),
        (COMPRADOR, 'compradores'),
        (VENDEDOR, 'vendedores')
    )
    rol = models.PositiveSmallIntegerField(choices=ROLES,default=1)
    telefono = models.CharField(max_length=9)
    direccion = models.CharField(max_length=150)
    
    def __str__(self):
        return self.username

class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    razonSocial = models.CharField(max_length=150)
    direccionFiscal = models.CharField(max_length=150)

class Comprador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)


    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=50, blank=True)
    existecias = models.IntegerField()
    destacada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

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
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, 
                                 related_name='producto_vendedor')
    categorias = models.ManyToManyField(Categoria, through='ProductoCategoria', 
                                        related_name="categorias")
    
    def __str__(self):
        return self.nombre

class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Chat(models.Model):
    usuario1 = models.ForeignKey(Usuario, related_name='chat_usuario1', 
                                 on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(Usuario, related_name='chat_usuario2', 
                                 on_delete=models.CASCADE)

class Compra(models.Model):
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    GARANTIA=[
        ("UNO", "Un año"),
        ("DOS", "Dos años"),
    ]
    garantia = models.CharField(max_length=3, choices=GARANTIA)
    producto = models.ManyToManyField(Producto)
    
class Envio(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion=models.TextField()	
    fecha_envio = models.DateTimeField()
    fecha_recepcion = models.DateTimeField()
    recepcionEstimada = models.DateTimeField()

class Valoracion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True)



