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

def adultoUpdate(request, id):
    # Verificar permisos
    if not user_in_group(request.user, 'funcionario'):
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    
    try:
        # Obtener el objeto adultoMayor
        adulto = adultoMayor.objects.get(id=id)
    except adultoMayor.DoesNotExist:
        return HttpResponseNotFound("El adulto mayor no existe.")
    
    # Si el formulario es enviado (POST)
    if request.method == 'POST':
        form = CustomUserAndAdultoMayorForm(request.POST, request.FILES, instance=adulto)
        if form.is_valid():
            # Actualizar adultoMayor
            adulto.rut_adulto = form.cleaned_data['rut_adulto']
            adulto.p_nombre = form.cleaned_data['p_nombre']
            adulto.s_nombre = form.cleaned_data.get('s_nombre', '')
            adulto.p_apellido = form.cleaned_data['p_apellido']
            adulto.s_apellido = form.cleaned_data.get('s_apellido', '')
            adulto.direccion = form.cleaned_data['direccion']
            adulto.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            adulto.correo_electronico = form.cleaned_data['correo_electronico']
            adulto.comprobante_domicilio = form.cleaned_data.get('comprobante_domicilio', None)
            adulto.comuna = form.cleaned_data['comuna']
            adulto.genero = form.cleaned_data['genero']
            adulto.telefono = form.cleaned_data['telefono']
            adulto.save()

            return redirect('detalleAdultos')  # Redirigir a la lista de adultos
        else:
            # Si el formulario no es válido, renderizarlo nuevamente con el mensaje de error
            return render(request, 'core/crud/update_adulto.html', {'form': form, 'ms': 'Error en el formulario'})

    # Si es un GET, mostrar el formulario con los datos actuales
    form = CustomUserAndAdultoMayorForm(instance=adulto)
    return render(request, 'core/crud/update_adulto.html', {'form': form})

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