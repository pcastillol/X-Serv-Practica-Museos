from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Museo(models.Model):
    nombre = models.CharField(max_length=256)
    enlace = models.CharField(max_length=512)
    direccion = models.CharField(max_length=256)
    barrio = models.CharField(max_length=64)
    distrito = models.CharField(max_length=64)
    contacto = models.CharField(max_length=256)
    accesibilidad = models.CharField(max_length=2)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
	museo_id = models.ForeignKey(Museo)    #1museo-Ncomentarios
	texto = models.TextField()

class Seleccionado(models.Model):
	user = models.ForeignKey(User, default="")
	museo_id = models.ForeignKey(Museo)
	fecha = models.DateField(auto_now=True)    #The field is automatically updated when Seleccionado.save()

class CSS(models.Model):
	user = models.CharField(max_length=128, blank=True)    #blank=True para permitir valor vacio
	titulo = models.CharField(max_length=128, blank=True)
	color = models.CharField(max_length=64, blank=True)
	size = models.IntegerField(blank=True)
