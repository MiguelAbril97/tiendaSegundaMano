from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q,Prefetch
from .models import *
from datetime import date
import datetime

#CRUD de Usuario
class UsuarioForm(UserCreationForm):
   
    roles = (
        ('', 'Seleccione un rol'),
        (Usuario.COMPRADOR, 'comprador'),
        (Usuario.VENDEDOR, 'vendedor'),
    )
    
    rol = forms.ChoiceField(choices=roles, required=True)
    telefono = forms.CharField(max_length=9, label="Teléfono")
    direccion = forms.CharField(max_length=150, label="Dirección")
    
    # Comprador
    nombre = forms.CharField(max_length=60, required=False, label="Nombre")
    apellidos = forms.CharField(max_length=60, required=False, label="Apellidos")
    
    # Vendedor
    razonSocial = forms.CharField(max_length=150, required=False, label="Razón Social")
    direccionFiscal = forms.CharField(max_length=150, required=False, 
                                      label="Dirección Fiscal. Dejelo en blanco si es igual a su dirección")
   
    class Meta:
        model = Usuario
        fields = ('rol', 'username', 'email',
            'telefono', 'direccion', 'password1', 'password2',
            'nombre', 'apellidos', 'razonSocial', 'direccionFiscal')     
        #Al usar el widget de email obligo al usuario a introducir un email con el formato correcto
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


        
        #Compruebo que el correo electronico no se repita, asi puedo usar el formulario para editar 
        # si el id es del propio objeto segura, si no os envia un mensaje de error 
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
        
         #Comprobamos que el campo telefono tenga 9 caracteres        
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
                #self.cleaned_data['direccionFiscal'] = direccion
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
        
        #Compruebo que no deje todos los campos vacios y que introduzca al menos 3 y 5
        # caracteres en campos email y telefono
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

#CRUD de Categoria
class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion','existecias','destacada']
       
       #Usando el widget con number input me aseguro que introduzca
       # solo numeros y que sea un numero mayor a 0
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

        # Me aseguro de que no haya otras categorias con ese nombre 
        
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
        
        #Me aseguro que al menos relle un campo y que la busqueda 
        # por nombre no sea demasiado larga
        if (nombre == "" and descripcion =="" and existencias and not destacada):
            self.add_error('buscarNombre','Busqueda inválida')
            self.add_error('buscarDescripcion','Busqueda inválida')
            self.add_error('sinExistencias','Busqueda inválida')
            self.add_error('destacada','Busqueda inválida')
        
        else:
            if (nombre != "" and len(nombre) > 100):
                self.add_error('buscarNombres','Nombre demasiado largo')
                
        return self.cleaned_data

    
#CRUD de Producto  
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','estado',
                  'fecha_de_publicacion','categorias']
        labels = {
            'fecha_de_publicacion':('Fecha de publicación del producto')
        }
        
        widgets = {
            'fecha_de_publicacion':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'descripcion':forms.Textarea(attrs={"maxlength":"100"}),
            'precio':forms.NumberInput(attrs={'min': '0',' max_digits':'10'}),
        }   
        
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        estado = self.cleaned_data.get('estado')
      #  vendedor = self.cleaned_data.get('vendedor')
        fecha_de_publicacion = self.cleaned_data.get('fecha_de_publicacion')
        categorias = self.cleaned_data.get('categorias')
             
        
        
   
    
      #  if(vendedor == None):
       #     self.add_error('vendedor', 'Indique un vendedor')
      
        if(estado == None):
            self.add_error('estado', 'Indique un estado')
        
        if(precio < 0):
            self.add_error('precio','El precio minimo es 0')
           
        
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
    buscarFecha = forms.DateField(
        label="Fecha de Publicación",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )


    #Si la solicitud es de un comprador se mostrara el campo vendedor
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BuscarProducto, self).__init__(*args, **kwargs)
        if (self.request.user.rol == 2 or self.request.user.rol == 1):
            self.fields["buscarVendedor"] = forms.ModelMultipleChoiceField(
                queryset=Usuario.objects.filter(producto_vendedor__isnull=False).distinct(),
                required=False,
                label="Vendedor"
            )
            self.fields["buscarCategorias"] = forms.ModelMultipleChoiceField(
                queryset=Categoria.objects.prefetch_related(
                    Prefetch('categorias')).filter(categorias__isnull=False).distinct(),
                required=False,
                widget=forms.CheckboxSelectMultiple(),
                label="Categorías"
                )
        else:
            categorias = Categoria.objects.filter(
                    productocategoria__producto__vendedor=self.request.user
                ).only("categorias").distinct()
            self.fields["buscarCategorias"] = forms.ModelMultipleChoiceField(
                queryset= categorias,
                required=False,
                widget=forms.CheckboxSelectMultiple(),
                label="Categorías"
            )
   
    
    
    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        nombre = self.cleaned_data.get('buscarNombre')
        descripcion = self.cleaned_data.get('buscarDescripcion')
        precio = self.cleaned_data.get('buscarPrecioMax')
        estado = self.cleaned_data.get('buscarEstado')

        if ('buscarVendedor' in self.cleaned_data):
            vendedor = self.cleaned_data.get('buscarVendedor')

        fecha = self.cleaned_data.get('buscarFecha')
        categoria = self.cleaned_data.get('buscarCategorias')
        
        #Compruebo que no deja todo vacio y la longitud de los campos precio y nombre
        if(nombre == "" 
           and descripcion==""
           and precio is None
           and len(estado) == 0 
           and fecha is None 
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
                self.add_error('buscarFecha', error_msg)
                self.add_error('buscarCategorias', error_msg)
            else:
                error_msg = "Debe introducir al menos un valor en un campo del formulario"
                self.add_error('buscarNombre', error_msg)
                self.add_error('buscarDescripcion', error_msg)
                self.add_error('buscarPrecioMax', error_msg)
                self.add_error('buscarEstado', error_msg)
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarFecha', error_msg)
                self.add_error('buscarCategorias', error_msg)
        else:
            
            if(precio is not None and precio > 9999999999):
                self.add_error('buscarPrecioMax', 'Introduzca un precio maximo más bajo')
            if(nombre != "" and len(nombre) > 100):
                self.add_error('buscarNombre', 'Introduzca un nombre más corto')

        
    

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
            'talla': forms.NumberInput(attrs={"min":'1',"max": "50"}),
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
        
        idProducto = Calzado.objects.filter(producto = producto).first()
        
        #Compruebo que no haya otro calzado con el mismo id de producto 
        if ( not idProducto is None) :
             if(not self.instance is None and idProducto.id == self.instance.id):
                 pass
             else:
                self.add_error('producto','Ya existe un calzado con ese id asignado')

        if (len(material)<6):
            self.add_error('material', 'Minimo 6 caracteres')

        return self.cleaned_data

class BuscarCalzado(forms.Form):
    
    buscarTalla = forms.DecimalField(
        required=False,
        label="Talla",
        min_value=0,
        widget=forms.NumberInput()
    )
    
    buscarMarca = forms.ChoiceField(
        choices=Calzado.MARCAS,
        required=False,
        widget=forms.RadioSelect()
    )
    buscarColor = forms.CharField(required=False, label="Color")
    buscarMaterial = forms.CharField(required=False, label="Material")
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput()
    )

    def clean(self):
        
        super().clean()

        talla = self.cleaned_data.get('buscarTalla')
        marca = self.cleaned_data.get('buscarMarca')
        color = self.cleaned_data.get('buscarColor')
        material = self.cleaned_data.get('buscarMaterial')
        precio = self.cleaned_data.get('buscarPrecioMax')
        
        #Verifico que no lo deje en blanco, que la talla y el precio esten en un
        #rango concreto y la longitude del campo material 
        if (not talla is None 
            and marca is None 
            and color == "" 
            and material == "" 
            and precio == ""):
            error_msg = "Debe introducir al menos un valor en un campo del formulario"
            self.add_error('buscarTalla', error_msg)
            self.add_error('buscarMarca', error_msg)
            self.add_error('buscarColor', error_msg)
            self.add_error('buscarMaterial', error_msg)
            self.add_error('buscarPrecioMax', error_msg)
        
        if(material != "" and len(material) < 3):
            self.add_error('buscarMaterial', 
                           'Material debe contener al menos 3 caracteres ')
        if(not talla is None and talla > 50):
            self.add_error('buscarTalla', 
                           'La talla debe ser entre 1 y 50')
        if(not precio !="" and precio > 999):
            self.add_error('buscarPrecioMax', 'El precio maximo es 999')

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
            'ancho': forms.NumberInput(attrs={'min': '0'}),
            'alto': forms.NumberInput(attrs={'min': '0'}),
            'profundidad': forms.NumberInput(attrs={'min': '0'}),
            'peso': forms.NumberInput(attrs={'min': '0'}),
        }

    def clean(self):
        super().clean()
        ancho = self.cleaned_data.get('ancho')
        alto = self.cleaned_data.get('alto')
        profundidad = self.cleaned_data.get('profundidad')
        peso = self.cleaned_data.get('peso')
        producto = self.cleaned_data.get('producto')
        
        idProducto = Muebles.objects.filter(producto = producto).first()
        
        if ( not idProducto is None):
             if(not self.instance is None and idProducto.id == self.instance.id):
                 pass
             else:
                self.add_error('producto','Ya existe un mueble con ese id asignado')

        #Aunque con los widgets me aseguro de que el numero sea
        #mayor a 0 personalizo el mensaje

        if (ancho <= 0):
            self.add_error('ancho', 'El ancho debe ser mayor a 0.')
        if (alto <= 0):
            self.add_error('alto', 'El alto debe ser mayor a 0.')
        if (profundidad <= 0):
            self.add_error('profundidad', 'La profundidad debe ser mayor a 0.')
        if (peso <= 0):
            self.add_error('peso', 'El peso debe ser mayor a 0.')

        return self.cleaned_data 
    

class BuscarMueble(forms.Form):
    buscarMaterial = forms.CharField(required=False, label="Material")
    buscarAnchoMin = forms.FloatField(
        required=False,
        label="Ancho mínimo",
        widget=forms.NumberInput()
    )
    buscarAnchoMax = forms.FloatField(
        required=False,
        label="Ancho máximo",
        widget=forms.NumberInput()
    )
    buscarAltoMin = forms.FloatField(
        required=False,
        label="Alto mínimo",
        widget=forms.NumberInput()
    )
    buscarAltoMax = forms.FloatField(
        required=False,
        label="Alto máximo",
        widget=forms.NumberInput()
    )
    buscarProfundidadMin = forms.FloatField(
        required=False,
        label="Profundidad mínima",
        widget=forms.NumberInput()
    )
    buscarProfundidadMax = forms.FloatField(
        required=False,
        label="Profundidad máxima",
        widget=forms.NumberInput()
    )
    buscarPesoMax = forms.IntegerField(
        required=False,
        label="Peso máximo",
        widget=forms.NumberInput()
    )
    
    def clean(self):
       
        super().clean()

        material = self.cleaned_data.get('buscarMaterial')
        ancho_min = self.cleaned_data.get('buscarAnchoMin')
        ancho_max = self.cleaned_data.get('buscarAnchoMax')
        alto_min = self.cleaned_data.get('buscarAltoMin')
        alto_max = self.cleaned_data.get('buscarAltoMax')
        profundidad_min = self.cleaned_data.get('buscarProfundidadMin')
        profundidad_max = self.cleaned_data.get('buscarProfundidadMax')
        peso_max = self.cleaned_data.get('buscarPesoMax')

        if(material == "" 
             and ancho_min is None and ancho_max is None 
             and alto_min is None and alto_max is None
             and profundidad_min is None and profundidad_max is None
             and peso_max is None
             ):

             error_msg = "Debe introducir al menos un valor en un campo del formulario"


             self.add_error('buscarMaterial', error_msg)
             self.add_error('buscarAnchoMin', error_msg)
             self.add_error('buscarAnchoMax', error_msg)
             self.add_error('buscarAltoMin', error_msg)
             self.add_error('buscarAltoMax', error_msg)
             self.add_error('buscarProfundidadMin', error_msg)
             self.add_error('buscarProfundidadMax', error_msg)
             self.add_error('buscarPesoMax', error_msg)

        #Me aseguro de que ninguno de los màximos sean menores que los mínimos
        if(not ancho_min is None and not ancho_max is None and ancho_min > ancho_max):
            self.add_error('buscarAnchoMin','El ancho mínimo no puede ser mayor al maximo')
            self.add_error('buscarAnchoMax','El ancho mínimo no puede ser mayor al maximo')
        
        if(not alto_min is None and not alto_max is None and  alto_min > alto_max):
            self.add_error('buscarAltoMin', 'El alto mínimo no puede ser mayor al máximo')
            self.add_error('buscarAltoMax', 'El alto mínimo no puede ser mayor al máximo')

        if(not profundidad_max is None and not profundidad_min is None and  profundidad_min > profundidad_max):
            self.add_error('buscarProfundidadMin', 'La profundidad mínima no puede ser mayor a la máxima')
            self.add_error('buscarProfundidadMax', 'La profundidad mínima no puede ser mayor a la máxima')
        
        #tambien de que el peso maximo no sea menor o igual a 0
        if(not peso_max is None and peso_max <= 0):
            self.add_error('buscarPesoMax', 'El peso debe ser mayor a 0')

        
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
        
        idProducto = Consolas.objects.filter(producto = producto).first()
        
        #Hago lo de siempre con el id producto
        if (not idProducto is None) :
             if(not self.instance is None and idProducto.id == self.instance.id):
                 pass
             else:
                self.add_error('producto','Ya existe una consola con ese id asignado')

        if (modelo and len(modelo) < 3):
            self.add_error('modelo', 'El modelo debe tener al menos 3 caracteres.')

        #Me aseguro de que no haya numero en el color
        #is alpha devuelve true si todos los caracteres de la cadena son de a-z
        #no lo he probado con la ñ
        if (color and not color.isalpha()):
            self.add_error('color', 'El color debe contener solo letras.')
        
        #Con memoria uso isdigit que es lo mismo pero a la inversa
        #no uso un input de numero porque el modelo es charfield y
        # y no se si podria dar error al usar un input que no devuelva string
        if (memoria != "" and not memoria.isdigit()):
            raise forms.ValidationError("El campo memoria debe contener solo números.")


        return self.cleaned_data

class BuscarConsola(forms.Form):
    buscarModelo = forms.CharField(required=False, label="Modelo")
    buscarColor = forms.CharField(required=False, label="Color")
    buscarMemoria = forms.IntegerField(
        required=False,
        label="Memoria",
        widget=forms.NumberInput()
    )
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '1000.00'})
    )

    def clean(self):
        super().clean()

        modelo = self.cleaned_data.get('buscarModelo')
        color = self.cleaned_data.get('buscarColor')
        memoria = self.cleaned_data.get('buscarMemoria')
        precio = self.cleaned_data.get('buscarPrecioMax')

        if (modelo == "" 
            and color == "" 
            and memoria is None  
            and precio is None):
            error_msg = "Debe introducir al menos un valor en un campo del formulario"
            self.add_error('buscarModelo', error_msg)
            self.add_error('buscarColor', error_msg)
            self.add_error('buscarMemoria', error_msg)
            self.add_error('buscarPrecioMax', error_msg)

        #Compruebo la longitud del color y vulvo a usar la validacion de antes
        if (not color !="" and len(color) < 4):
            self.add_error('buscarColor', 'Color invalido')
        elif(color and not color.isalpha()):
            self.add_error('color', 'El color debe contener solo letras.')
        if (memoria != "" and not memoria.isdigit()):
            raise forms.ValidationError("El campo memoria debe contener solo números.")

        



        return self.cleaned_data
