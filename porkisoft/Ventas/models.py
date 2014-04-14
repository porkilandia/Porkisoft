from django.db import models
from Telemercadeo.models import *
from Inventario.models import Bodega,Producto,SubProducto
from Nomina.models import Empleado

# Create your models here.
class Venta(models.Model):
    numeroVenta = models.AutoField(primary_key=True, verbose_name='Numero Factura')
    fechaVentav = models.DateTimeField(verbose_name='Fecha', auto_now=True)
    TotalVenta = models.IntegerField(verbose_name='Total Venta')
    descuento = models.BooleanField(verbose_name='Descuento',default=False)
    empleado = models.ForeignKey(Empleado)
    cliente = models.ForeignKey(Cliente)
    bodega = models.ForeignKey(Bodega)

    def __unicode__(self):
        return self.numeroVenta

class DetalleVenta (models.Model):
    venta = models.ForeignKey(Venta)
    producto = models.ForeignKey(Producto,null=True)
    subproducto = models.ForeignKey(SubProducto, null=True)
    peso = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso en Venta',null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades en Venta',null= True,default=0)
