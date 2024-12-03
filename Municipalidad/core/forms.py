from django.forms import ModelForm
from django import forms  # Asegúrate de importar el módulo forms
from .models import * 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TallerForm(ModelForm):

     class Meta:
        model = Taller
        fields = ['nombre', 'cant_horas', 'descripcion', 'fecha_inicio', 'fecha_termino', 'cant_min', 'cant_max']
        exclude = ['integrantes']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_termino': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }



class CustomUserAndAdultoMayorForm(UserCreationForm):
    # Campos adicionales del modelo adultoMayor
    rut_adulto = forms.CharField(max_length=20, required=True)
    p_nombre = forms.CharField(max_length=20, required=True)
    s_nombre = forms.CharField(max_length=20, required=False)
    p_apellido = forms.CharField(max_length=20, required=True)
    s_apellido = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=255, required=True)
    fecha_nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    correo_electronico = forms.EmailField(max_length=100, required=True)
    comprobante_domicilio = forms.FileField(required=False)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=True)
    genero = forms.ModelChoiceField(queryset=Genero.objects.all(), required=True)
    telefono = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'rut_adulto',
            'p_nombre',
            's_nombre',
            'p_apellido',
            's_apellido',
            'direccion',
            'fecha_nacimiento',
            'correo_electronico',
            'comprobante_domicilio',
            'comuna',
            'genero',
            'telefono',
        ]


class AdultoMayorForm(ModelForm):
    
    class Meta:
        model = adultoMayor
        exclude = ['user']

