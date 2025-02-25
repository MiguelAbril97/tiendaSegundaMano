from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Prefetch
from .models import *
from datetime import date
import datetime

# CRUD de Usuario
class UsuarioForm(UserCreationForm):
    roles = (
        ('', 'Seleccione un rol'),
        (Usuario.COMPRADOR, 'comprador'),
        (Usuario.VENDEDOR, 'vendedor'),
    )
    rol = forms.ChoiceField(choices=roles, required=True)
    telefono = forms.CharField(max_length=9, label="Teléfono")
    direccion = forms.CharField(max_length=150, label="Dirección")
    nombre = forms.CharField(max_length=60, required=False, label="Nombre")
    apellidos = forms.CharField(max_length=60, required=False, label="Apellidos")
    razonSocial = forms.CharField(max_length=150, required=False, label="Razón Social")
    direccionFiscal = forms.CharField(max_length=150, required=False, label="Dirección Fiscal. Dejelo en blanco si es igual a su dirección")
    class Meta:
        model = Usuario
        fields = ('rol', 'username', 'email', 'telefono', 'direccion', 'password1', 'password2', 'nombre', 'apellidos', 'razonSocial', 'direccionFiscal')
        widgets = {
            'email': forms.EmailInput(),
        }
    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        correo_electronico = self.cleaned_data.get('email')
        telefono = self.cleaned_data.get('telefono')
        direccion = self.cleaned_data.get('direccion')
        rol = self.cleaned_data.get('rol')
        nombre = self.cleaned_data.get('nombre')
        apellidos = self.cleaned_data.get('apellidos')
        razonSocial = self.cleaned_data.get('razonSocial')
        direccionFiscal = self.cleaned_data.get('direccionFiscal')
        usuarioCorreo = Usuario.objects.filter(email = correo_electronico).first()
        username = Usuario.objects.filter(username = username).first()
        if(not usuarioCorreo is None):
            if(not self.instance is None and usuarioCorreo.id == self.instance.id):
                pass
            else:
                self.add_error('email', 'Ya existe un usuario con ese correo')
        if(not username is None):
            if(not self.instance is None and username.id == self.instance.id):
                pass
            else:
                self.add_error('username', 'Ya existe un usuario con ese nombre de usuario')
        if len(telefono) != 9:
            self.add_error('telefono','Debe tener 9 caracteres')
        if rol == str(Usuario.COMPRADOR):
            if not nombre or not apellidos:
                self.add_error('nombre', 'Campo obligatorio')
                self.add_error('apellidos','Campo obligatorio')
        elif rol == str(Usuario.VENDEDOR):
            if not razonSocial:
                self.add_error('razonSocial', 'Campo obligatorio')
            if not direccionFiscal:
                direccionFiscal = direccion
        return self.cleaned_data

class BuscarUsuario (forms.Form):
    buscarNombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Introduce el nombre'
        })
    )
    buscarEmail = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Introduce el correo electrónico'
        })
    )
    buscarTlf = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Introduce el teléfono'
        })
    )
    buscarDireccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Introduce la dirección'
        })
    )
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('buscarNombre')
        email = self.cleaned_data.get('buscarEmail')
        tlf = self.cleaned_data.get('buscarTlf')
        direccion = self.cleaned_data.get('buscarDireccion')
        if(nombre == "" and email == "" and tlf == "" and direccion == ""):
            self.add_error('buscarNombre','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('buscarEmail','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('buscarTlf','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('buscarDireccion','Debe introducir al menos un valor en un campo del formulario')
        else: 
            if(tlf != "" and len(tlf) < 3):
                self.add_error('tlf','Debe introducir al menos 3 carácteres')
            if(email != "" and len(email) < 5):
                self.add_error('email','Debe introducir al menos 3 carácteres')
        return self.cleaned_data

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion','existecias','destacada']
        widgets = {
            'descripcion': forms.Textarea(attrs={"maxlength":"100"}),
            'existecias': forms.NumberInput(attrs={'min':'1'}),
        }
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        existencias = self.cleaned_data.get('existencias')
        destacada = self.cleaned_data.get('destacada')
        categoriaNombre = Categoria.objects.filter(nombre = nombre).first()
        if(not categoriaNombre is None):
            if(not self.instance is None and categoriaNombre.id == self.instance.id):
                pass
            else:
                self.add_error('nombre','Ya existe una categoria con este nombre')
        return self.cleaned_data

class BuscarCategoria(forms.Form):
    buscarNombre = forms.CharField(required=False)
    buscarDescripcion = forms.CharField(required=False)
    sinExistencias = forms.BooleanField(
        required=False,
        label='Buscar categorias sin productos',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    destacada = forms.BooleanField(
        required=False, 
        label='Solo categorias destacadas',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get("buscarNombre")
        descripcion = self.cleaned_data.get('buscarDescripcion')
        existencias = self.cleaned_data.get("sinExistencias")
        destacada = self.cleaned_data.get('destacada')
        if (nombre == "" and descripcion =="" and existencias and not destacada):
            self.add_error('buscarNombre','Busqueda inválida')
            self.add_error('buscarDescripcion','Busqueda inválida')
            self.add_error('sinExistencias','Busqueda inválida')
            self.add_error('destacada','Busqueda inválida')
        else:
            if (nombre != "" and len(nombre) > 100):
                self.add_error('buscarNombres','Nombre demasiado largo')
        return self.cleaned_data

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','estado','categorias']
        widgets = {
            'descripcion': forms.Textarea(attrs={"maxlength":"100"}),
            'precio': forms.NumberInput(attrs={'min': '0',' max_digits':'10'}),
        }   
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        estado = self.cleaned_data.get('estado')
        categorias = self.cleaned_data.get('categorias')
        if(estado == None):
            self.add_error('estado', 'Indique un estado')
        if(precio < 0):
            self.add_error('precio','El precio minimo es 0')
        return self.cleaned_data

class BusquedaProductoSimple(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BuscarProductoAPI(forms.Form):
    buscarNombre = forms.CharField(required=False, label="Nombre")
    buscarDescripcion = forms.CharField(required=False, label="Descripción")
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput(attrs={'min': '0'})
    )
    ESTADOS = [
        ("CN", "Como nuevo"),
        ("U", "Usado"),
        ("MU", "Muy usado"),
    ]
    buscarEstado = forms.MultipleChoiceField(
        choices=ESTADOS,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Estado"
    )
    buscarCategorias = forms.CharField(
        label='Categorías',
        required=False,
    )
    buscarVendedor = forms.CharField(
        label="Vendedor",
        required=False,
    )
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('buscarNombre')
        descripcion = self.cleaned_data.get('buscarDescripcion')
        precio = self.cleaned_data.get('buscarPrecioMax')
        estado = self.cleaned_data.get('buscarEstado')
        vendedor = self.cleaned_data.get('buscarVendedor')
        categoria = self.cleaned_data.get('buscarCategorias')
        return self.cleaned_data

class BuscarProducto(forms.Form): 
    buscarNombre = forms.CharField(required=False, label="Nombre")
    buscarDescripcion = forms.CharField(required=False,label="Descripción")
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput(attrs={'min': '0'})
    )
    buscarEstado = forms.MultipleChoiceField(
        choices=Producto.ESTADOS,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Estado"
    )
    buscarCategorias = forms.CharField(
        label= 'Categorías',
        required=False,
    )
    buscarVendedor = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(producto_vendedor__isnull=False).distinct(),
        required=False,
        label="Vendedor"
    )
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('buscarNombre')
        descripcion = self.cleaned_data.get('buscarDescripcion')
        precio = self.cleaned_data.get('buscarPrecioMax')
        estado = self.cleaned_data.get('buscarEstado')
        vendedor = self.cleaned_data.get('buscarVendedor')
        categoria = self.cleaned_data.get('buscarCategorias')
        if(nombre == "" 
           and descripcion==""
           and precio is None
           and len(estado) == 0 
           and len(categoria)==0
           ):
            if(vendedor and len(vendedor)==0):
                error_msg = "Debe introducir al menos un valor en un campo del formulario"
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarNombre', error_msg)
                self.add_error('buscarDescripcion', error_msg)
                self.add_error('buscarPrecioMax', error_msg)
                self.add_error('buscarEstado', error_msg)
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarCategorias', error_msg)
            else:
                error_msg = "Debe introducir al menos un valor en un campo del formulario"
                self.add_error('buscarNombre', error_msg)
                self.add_error('buscarDescripcion', error_msg)
                self.add_error('buscarPrecioMax', error_msg)
                self.add_error('buscarEstado', error_msg)
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarCategorias', error_msg)
        else:
            if(precio is not None and precio > 9999999999):
                self.add_error('buscarPrecioMax', 'Introduzca un precio maximo más bajo')
            if(nombre != "" and len(nombre) > 100):
                self.add_error('buscarNombre', 'Introduzca un nombre más corto')
        return self.cleaned_data