from django.http import HttpResponseForbidden, HttpResponseNotFound
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


# Create your views here.
def index(request):
    talleres = Taller.objects.all()
    aux = {
        'lista' : talleres
    }
    return render(request, 'core/index.html',aux)


#Talleres
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


def inscribir_taller(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        rut = request.POST.get('rut')
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        taller_id = request.POST.get('taller')

        # Obtener el taller al que se está inscribiendo
        try:
            taller = Taller.objects.get(id=taller_id)
        except Taller.DoesNotExist:
            return render(request, 'core/mensaje.html', {'mensaje': 'Taller no encontrado.'})

        # Verificar si el taller ya tiene el máximo de participantes
        if taller.integrantes:
            integrantes = taller.integrantes.split(',')
        else:
            integrantes = []

        # Verificar si el taller tiene espacio
        if len(integrantes) < taller.cant_max:
            # Agregar el RUT del adulto mayor al campo 'integrantes'
            if (rut in taller.integrantes):
                return render(request, 'core/mensaje.html', {'mensaje': f'Ya estas en el taller {taller.nombre}!'})
            else:
                integrantes.append(rut)
                taller.integrantes = ','.join(integrantes)
                taller.save()

            # Mensaje de éxito
            return render(request, 'core/mensaje.html', {'mensaje': f'Inscripción exitosa a {taller.nombre}!'})
        else:
            # Si el taller ya está lleno
            return render(request, 'core/mensaje.html', {'mensaje': f'El taller {taller.nombre} está lleno.'})

    else:
        # Si no es un POST, solo mostrar el formulario
        talleres = Taller.objects.all()  # Lista de talleres
        return render(request, 'core/index.html', {'lista': talleres})
    
def mensaje(request):
    return render(request, 'core/mensaje.html')

#Adultos
def detalleAdultos(request):
    # Obtener todos los adultos mayores
    adultos_mayores = adultoMayor.objects.all()
    aux = {
        'lista': adultos_mayores
    }
    
    # Pasar la lista de adultos mayores al template
    return render(request, 'core/detalle_adultos.html', aux)

def adultoAdd(request):
    # Verificar permisos
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")

    if request.method == 'POST':
        form = CustomUserAndAdultoMayorForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Crear el objeto adultoMayor asociado
            adulto_mayor = adultoMayor.objects.create(
                user=user,
                rut_adulto=form.cleaned_data['rut_adulto'],
                p_nombre=form.cleaned_data['p_nombre'],
                s_nombre=form.cleaned_data.get('s_nombre', ''),
                p_apellido=form.cleaned_data['p_apellido'],
                s_apellido=form.cleaned_data.get('s_apellido', ''),
                direccion=form.cleaned_data['direccion'],
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                correo_electronico=form.cleaned_data['correo_electronico'],
                comprobante_domicilio=form.cleaned_data.get('comprobante_domicilio', None),
                comuna=form.cleaned_data['comuna'],
                genero=form.cleaned_data['genero'],
                telefono=form.cleaned_data['telefono'],
            )

            return redirect('detalleAdultos')  # Redirigir a la lista de adultos
        else:
            return render(request, 'core/crud/add_adulto.html', {'form': form, 'ms': 'Error en el formulario'})

    # GET: Mostrar formulario vacío
    form = CustomUserAndAdultoMayorForm()
    return render(request, 'core/crud/add_adulto.html', {'form': form})

def adultoDelete(request, id):
    # Verificar si el usuario tiene permiso (staff o pertenece al grupo 'admin')
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")

    try:
        adulto = adultoMayor.objects.get(id=id)
        # Eliminar al usuario asociado si existe
        if adulto.user:  # Asumiendo que el campo relacionado se llama 'usuario'
            adulto.user.delete()
        # Eliminar al adulto mayor
        adulto.delete()

    except adultoMayor.DoesNotExist:
        return HttpResponseNotFound("El adulto mayor no existe.")
    
    return redirect(to="detalleAdultos")



def adultoUpdate(request,id):
    # Verificar si el usuario tiene permiso (staff o pertenece al grupo 'admin')
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    
    adulto = adultoMayor.objects.get(id=id)
    aux ={
        'form' : AdultoMayorForm(instance=adulto)
    }

    if request.method == 'POST':
        formulario = AdultoMayorForm(data=request.POST,instance=adulto)
        if formulario.is_valid():
            formulario.save()
            aux['ms'] = 'adulto mayor modificado correctamente.'
            return redirect(to="detalleAdultos")
        else:
            aux['form'] = formulario
            aux['ms'] = 'el adulto mayor no ha sido modificado.'

    return render(request,'core/crud/update_adulto.html',aux)

def register(request):
    aux = {
        'form': CustomUserAndAdultoMayorForm()
    }
    
    if request.method == 'POST':
        formulario = CustomUserAndAdultoMayorForm(data=request.POST, files=request.FILES)
        
        if formulario.is_valid():
            # Guardar el usuario (User)
            user = formulario.save(commit=False)  # No guardar aún el usuario
            user.save()  # Guardar el usuario en la base de datos

            # Crear el perfil de adultoMayor y asociarlo con el usuario
            adulto_mayor = adultoMayor(
                rut_adulto=formulario.cleaned_data['rut_adulto'],
                p_nombre=formulario.cleaned_data['p_nombre'],
                s_nombre=formulario.cleaned_data['s_nombre'],
                p_apellido=formulario.cleaned_data['p_apellido'],
                s_apellido=formulario.cleaned_data['s_apellido'],
                direccion=formulario.cleaned_data['direccion'],
                fecha_nacimiento=formulario.cleaned_data['fecha_nacimiento'],
                correo_electronico=formulario.cleaned_data['correo_electronico'],
                comprobante_domicilio=formulario.cleaned_data['comprobante_domicilio'],
                comuna=formulario.cleaned_data['comuna'],
                genero=formulario.cleaned_data['genero'],
                telefono=formulario.cleaned_data['telefono'],
                user=user  # Asignar el usuario al perfil de adultoMayor
            )
            adulto_mayor.save()  # Guardar el perfil en la base de datos

            # Asignar al grupo "Adulto Mayor"
            group = Group.objects.get(name='Adulto Mayor')
            user.groups.add(group)

            return redirect("index")
        else:
            aux['form'] = formulario

    return render(request, 'registration/register.html', aux)