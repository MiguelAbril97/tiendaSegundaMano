from django import forms
from django.forms import ModelForm
from .models import *

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