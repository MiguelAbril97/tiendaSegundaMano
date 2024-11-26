from django import forms
from django.forms import ModelForm
from .models import *


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

    