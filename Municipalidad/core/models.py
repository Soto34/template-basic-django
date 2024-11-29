from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#py manage.py makemigrations
#py manage.py migrate

class Genero(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion

class Comuna(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion
    

class adultoMayor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adulto_mayor')
    rut_adulto = models.CharField(max_length=20, unique=True)
    p_nombre = models.CharField(max_length=20)
    s_nombre = models.CharField(max_length=20, blank=True)
    p_apellido = models.CharField(max_length=20)
    s_apellido = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    correo_electronico = models.EmailField(max_length=100)
    comprobante_domicilio = models.FileField(upload_to='comprobantes_domicilio/', blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)
    telefono = models.IntegerField()

    def __str__(self):
        return self.rut_adulto

    

class Instructor(models.Model):
    rut_instructor = models.CharField(max_length=20, unique=True)  # Asegurarse de que no se repitan los RUT
    p_nombre = models.CharField(max_length=20)
    s_nombre = models.CharField(max_length=20, blank=True)  # Puede no haber segundo nombre
    p_apellido = models.CharField(max_length=20)
    s_apellido = models.CharField(max_length=20, blank=True)  # Puede no haber segundo apellido
    fecha_nacimiento = models.DateField()  # Cambié a DateField para mejor manejo de fechas
    correo_electronico = models.EmailField(max_length=100)  # Cambié a EmailField
    comuna = models.ForeignKey(Comuna,on_delete=models.SET_NULL,null=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)  # Relación con el modelo Genero
    telefono = models.IntegerField(max_length=20)

    def __str__(self):
        return self.rut_instructor
    

class Taller(models.Model):
    nombre = models.CharField(max_length=100)
    cant_horas = models.IntegerField()  # Número de horas del taller
    descripcion = models.TextField()  # Descripción más larga para texto extenso
    fecha_inicio = models.DateTimeField()  # Fecha y hora de inicio del taller
    fecha_termino = models.DateTimeField()  # Fecha y hora de finalización del taller
    cant_min = models.IntegerField()  # Mínimo de participantes
    cant_max = models.IntegerField()  # Máximo de participantes
    prom_evalua_taller = models.IntegerField()  # Promedio de evaluación del taller

    def __str__(self):
        return self.nombre

class InscripcionTaller(models.Model):
    adulto_mayor = models.ForeignKey(adultoMayor, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('inscrito', 'Inscrito'), ('finalizado', 'Finalizado')], default='inscrito')

    