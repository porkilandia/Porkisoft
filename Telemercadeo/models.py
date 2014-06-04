from django.db import models

from Inventario.models import *

# Create your models here.
class Cliente (models.Model):
    codigoCliente  = models.AutoField(primary_key=True, verbose_name='Codigo Cliente')
    nit = models.CharField(verbose_name='Nit',max_length=15,default=0)
    nombreCliente = models.CharField(max_length=50)
    telefonoCliente = models.CharField(max_length=10,verbose_name='Telefono')
    direccionCliente = models.CharField(max_length=50,verbose_name='Direccion')

    def __unicode__(self):
        return self.nombreCliente

