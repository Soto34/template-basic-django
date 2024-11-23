from django.shortcuts import render,redirect
from .models import * 
from .forms import *
# Create your views here.
def index(request):
    talleres = Taller.objects.all()
    aux = {
        'lista' : talleres
    }
    return render(request, 'core/index.html',aux)


def meetings(request):
    return render(request,'core/meetings.html')

def tallerAdd(request):
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
    taller = Taller.objects.get(id=id)
    taller.delete()

    return redirect(to="detalleTalleres")




def detalleTalleres(request):
    talleres = Taller.objects.all()
    aux = {
        'lista' : talleres
    }
    return render(request,'core/detalle_Talleres.html',aux)

