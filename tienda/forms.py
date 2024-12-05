from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date

#CRUD de Usuario
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        labels = {
            'nombre':("Nombre de usuario"), 'correo_electronico':('Direccion de email')
        }
        
        help_texts={
            'correo_electronico':('Introduce una direccion valida')    
        }
        
        widgets = {
            'correo_electronico': forms.EmailInput()
        }    
    
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        correo_electronico = self.cleaned_data.get('correo_electronico')
        telefono = self.cleaned_data.get('telefono')
        direccion = self.cleaned_data.get('direccion')
        
        usuarioCorreo = Usuario.objects.filter(correo_electronico = correo_electronico).first()
        
        if(not usuarioCorreo is None):
            if(not self.instance is None and usuarioCorreo.id == self.instance.id):
                pass
            else:
                self.add_error('correo_electronico', 'Ya existe un usuario con ese correo')
        
         #Comprobamos que el campo telefono tenga 11 caracteres        
        if len(telefono) != 9:
            self.add_error('telefono','Debe tener 11 caracteres')
        
        return self.cleaned_data


class BuscarUsuario (forms.Form):
    
    buscarNombre = forms.CharField(required=False)
    buscarEmail = forms.CharField(required=False)
    buscarTlf = forms.CharField(required=False)
    buscarDireccion = forms.CharField(required=False)
    
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('buscarNombre')
        email = self.cleaned_data.get('buscarEmail')
        tlf = self.cleaned_data.get('buscarTlf')
        direccion = self.cleaned_data.get('buscarDireccion')
        
        if(nombre == "" and email == "" and tlf == "" and direccion == ""):
            self.add_error('nombre','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('email','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('tlf','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion','Debe introducir al menos un valor en un campo del formulario')
        else: 
            if(tlf != "" and len(tlf) < 3):
                self.add_error('tlf','Debe introducir al menos 3 carácteres')
        
        return self.cleaned_data

#CRUD de Categoria
class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion','existecias','destacada']
       
        widgets = {
            'descripcion': forms.Textarea(attrs={"maxlength":"100"}),
            'existecias': forms.NumberInput(),
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
        
        if(existencias == 0):
            self.add_error('existencias','No se puede crear una categoria sin existencias')
          
        
        return self.cleaned_data
    
class BuscarCategoria(forms.Form):
    
    buscarNombre = forms.CharField(required=False)
    buscarDescripcion = forms.CharField(required=False)
    sinExistencias = forms.BooleanField(
        label='Buscar categorias sin productos',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    destacada = forms.BooleanField(
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
            self.add_error('nombre','Busqueda inválida')
            self.add_error('descripcion','Busqueda inválida')
            self.add_error('existencias','Busqueda inválida')
            self.add_error('destacada','Busqueda inválida')
        
        else:
            if (nombre != "" and len(nombre) > 100):
                self.add_error('nombre','Nombre demasiado largo')
                
        return self.cleaned_data

    
#CRUD de Producto  
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
        labels = {
            'fecha_de_publicacion':('Fecha de publicación del producto')
        }
        
        widgets = {
            'fecha_de_publicacion':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'descripcion':forms.Textarea(attrs={"maxlength":"100"}),
            'precio':forms.NumberInput(attrs={'step': '0.01', 'min': '0',' max_digits':'10'}),
        }   
        
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        estado = self.cleaned_data.get('estado')
        vendedor = self.cleaned_data.get('vendedor')
        fecha_de_publicacion = self.cleaned_data.get('fecha_de_publicacion')
        categorias = self.cleaned_data.get('categorias')
        
        
        
        hoy = date.today()
        if(hoy > fecha_de_publicacion):
            self.add_error('fecha_de_publicacion','La fecha de publicacion debe ser mayor a la de hoy')   
        
        if(vendedor == None):
            self.add_error('vendedor', 'Indique un vendedor')
        
        if(estado == None):
            self.add_error('estado', 'Indique un estado')
        
        if(precio < 0):
            self.add_error('precio','El precio minimo es 0')
           
        
        return self.cleaned_data

#CRUD CALZADO 
class CalzadoForm(ModelForm):
    class Meta:
        model = Calzado
        fields = '__all__'  

        labels = {
            'talla': ('Talla del calzado'),
            'marca': ('Marca del calzado'),
            'color': ('Color del calzado'),
            'material': ('Material del calzado'),
        }

        widgets = {
            'talla': forms.TextInput(attrs={"maxlength": "2"}),
            'marca': forms.Select(attrs={"class": "form-control"}),
            'color': forms.TextInput(attrs={"maxlength": "20"}),
            'material': forms.TextInput(attrs={"maxlength": "30"}),
        }


    def clean(self):
        super().clean()
        talla = self.cleaned_data.get('talla')
        marca = self.cleaned_data.get('marca')
        color = self.cleaned_data.get('color')
        material = self.cleaned_data.get('material')
        producto = self.cleaned_data.get('producto')
        
        idProducto = Calzado.objects.filter(producto = producto)
        
        if ( not idProducto is None) :
             if(not self.instance is None and idProducto.id == self.instance.id):
                 pass
             else:
                self.add_error('producto','Ya existe un calzado con ese id asignado')


        if talla and (not talla.isdigit() or int(talla) < 1 or int(talla) > 50):
            self.add_error('talla', 'La talla debe ser un número entre 1 y 50.')

        if not material:
            self.add_error('material', 'El material es obligatorio.')

        return self.cleaned_data
    

#CRUD MUEBLE

class MuebleForm(ModelForm):
    class Meta:
        model = Muebles
        fields = '__all__'

        labels = {
            'material': ('Material del mueble'),
            'ancho': ('Ancho (cm)'),
            'alto': ('Alto (cm)'),
            'profundidad': ('Profundidad (cm)'),
            'peso': ('Peso (kg)'),
        }

        widgets = {
            'material': forms.TextInput(attrs={"maxlength": "30"}),
            'ancho': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
            'alto': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
            'profundidad': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
            'peso': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        }

    def clean(self):
        super().clean()
        ancho = self.cleaned_data.get('ancho')
        alto = self.cleaned_data.get('alto')
        profundidad = self.cleaned_data.get('profundidad')
        peso = self.cleaned_data.get('peso')
        producto = self.cleaned_data.get('producto')
        
        idProducto = Muebles.objects.filter(producto = producto)
        
        if ( not idProducto is None):
             if(not self.instance is None and idProducto.id == self.instance.id):
                 pass
             else:
                self.add_error('producto','Ya existe un mueble con ese id asignado')


        if (ancho <= 0):
            self.add_error('ancho', 'El ancho debe ser mayor a 0.')
        if (alto <= 0):
            self.add_error('alto', 'El alto debe ser mayor a 0.')
        if (profundidad <= 0):
            self.add_error('profundidad', 'La profundidad debe ser mayor a 0.')
        if (peso <= 0):
            self.add_error('peso', 'El peso debe ser mayor a 0.')

        return self.cleaned_data 
    

#CRUD CONSOLA
class ConsolasForm(ModelForm):
    class Meta:
        model = Consolas
        fields = '__all__'

        labels = {
            'producto': 'Producto asociado',
            'modelo': 'Modelo de la consola',
            'color': 'Color de la consola',
            'memoria': 'Memoria de la consola',
        }

        widgets = {
            'producto': forms.Select(attrs={"class": "form-control"}),
            'modelo': forms.TextInput(attrs={"maxlength": "50", "class": "form-control"}),
            'color': forms.TextInput(attrs={"maxlength": "20", "class": "form-control"}),
            'memoria': forms.TextInput(attrs={"maxlength": "20", "class": "form-control"}),
        }

    def clean(self):
        super().clean()
        modelo = self.cleaned_data.get('modelo')
        color = self.cleaned_data.get('color')
        memoria = self.cleaned_data.get('memoria')
        producto = self.cleaned_data.get('producto')
        
        idProducto = Consolas.objects.filter(producto = producto)
        
        if ( not idProducto is None) :
             if(not self.instance is None and idProducto.id == self.instance.id):
                 pass
             else:
                self.add_error('producto','Ya existe un calzado con ese id asignado')

        if modelo and len(modelo) < 3:
            self.add_error('modelo', 'El modelo debe tener al menos 3 caracteres.')

        if color and not color.isalpha():
            self.add_error('color', 'El color debe contener solo letras.')

        if memoria and not memoria.replace('GB', '').isdigit():
            self.add_error('memoria', 'La memoria debe ser un número seguido de "GB" (por ejemplo, "16GB").')

        return self.cleaned_data