from django.forms import ModelForm
from django import forms  # Asegúrate de importar el módulo forms
from .models import * 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TallerForm(ModelForm):

     class Meta:
        model = Taller
        fields = ['nombre', 'cant_horas', 'descripcion', 'fecha_inicio', 'fecha_termino', 'cant_min', 'cant_max', 'prom_evalua_taller']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_termino': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class InscripcionForm(ModelForm):

    class Meta:
        model = InscripcionTaller
        fields = '__all__'



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    