# Generated by Django 5.1.3 on 2024-11-21 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Taller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cant_horas', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_termino', models.DateTimeField()),
                ('cant_min', models.IntegerField()),
                ('cant_max', models.IntegerField()),
                ('prom_evalua_taller', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='adultoMayor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_adulto', models.CharField(max_length=20, unique=True)),
                ('p_nombre', models.CharField(max_length=20)),
                ('s_nombre', models.CharField(blank=True, max_length=20)),
                ('p_apellido', models.CharField(max_length=20)),
                ('s_apellido', models.CharField(blank=True, max_length=20)),
                ('direccion', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField()),
                ('correo_electronico', models.EmailField(max_length=100)),
                ('comprobante_domicilio', models.FileField(blank=True, null=True, upload_to='comprobantes_domicilio/')),
                ('comuna', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=20)),
                ('genero', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.genero')),
            ],
        ),
        migrations.CreateModel(
            name='InscripcionTaller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('inscrito', 'Inscrito'), ('finalizado', 'Finalizado')], default='inscrito', max_length=20)),
                ('adulto_mayor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.adultomayor')),
                ('taller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.taller')),
            ],
        ),
    ]
