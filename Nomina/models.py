from django.db import models

# Create your models here.
class Cargo(models.Model):
    codigoCargo = models.AutoField(primary_key=True, verbose_name='Codigo Cargo')
    nombreCargo = models.CharField(max_length=50, verbose_name='Cargo')

    def __unicode__(self):
        return self.nombreCargo

class Empleado(models.Model):
    codigoEmpleado = models.BigIntegerField(primary_key=True,verbose_name='Cedula')
    nombre = models.CharField(max_length= 50, verbose_name='Nombre')
    apellido = models.CharField(max_length= 50, verbose_name='Apellido')
    direccion = models.CharField(max_length=100,verbose_name='Direccion')
    telefono = models.CharField(max_length=10,verbose_name='Telefono')
    cargo = models.ForeignKey(Cargo)

    def __unicode__(self):
        cadena = self.nombre +' '+ self.apellido
        return cadena
