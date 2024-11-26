from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from .models import * 
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

#group required
def user_in_group(user, group_name):
    #$return user.groups.filter(name=group_name).exists() # sin staff
    return user.is_superuser or user.groups.filter(name=group_name).exists() #Con staff includio

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if user_in_group(request.user, group_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permisos para acceder a esta pagina")
        return _wrapped_view
    return decorator

@login_required
# Create your views here.
def index(request):
    talleres = Taller.objects.all()
    aux = {
        'lista' : talleres
    }
    return render(request, 'core/index.html',aux)



def tallerAdd(request):
    # Verificar si el usuario tiene permiso (staff o pertenece al grupo 'admin')
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    aux ={
        'form' : TallerForm()
    }
    if request.method == 'POST':
        formulario = TallerForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            aux['ms'] = 'Taller Agregado correctamente.'
            return redirect(to="detalleTalleres")
        else:
            aux['form'] = formulario
            aux['ms'] = 'Taller no ha sido agregado.'
            

    return render(request,'core/crud/add.html',aux)


def tallerUpdate(request,id):
    # Verificar si el usuario tiene permiso (staff o pertenece al grupo 'admin')
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    
    taller = Taller.objects.get(id=id)
    aux ={
        'form' : TallerForm(instance=taller)
    }

    if request.method == 'POST':
        formulario = TallerForm(data=request.POST,instance=taller)
        if formulario.is_valid():
            formulario.save()
            aux['ms'] = 'Taller modificado correctamente.'
            return redirect(to="detalleTalleres")
        else:
            aux['form'] = formulario
            aux['ms'] = 'Taller no ha sido modificado.'

    return render(request,'core/crud/update.html',aux)


def tallerDelete(request,id):
    # Verificar si el usuario tiene permiso (staff o pertenece al grupo 'admin')
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    taller = Taller.objects.get(id=id)
    taller.delete()

    return redirect(to="detalleTalleres")

def detalleTalleres(request):
    # Verificar si el usuario tiene permiso (staff o pertenece al grupo 'admin')
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    
    talleres = Taller.objects.all()
    aux = {
        'lista' : talleres
    }
    return render(request,'core/detalle_Talleres.html',aux)


def register(request):
    aux = {
        'form' : CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name='Adulto Mayor')
            user.groups.add(group)
            return redirect("index")
        else:
            aux['form'] = formulario

    return render(request,'registration/register.html',aux)
