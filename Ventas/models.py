from django.db import models
from Telemercadeo.models import *
from Inventario.models import Bodega,Producto,SubProducto
from Nomina.models import Empleado

# Create your models here.
class Venta(models.Model):
    numeroVenta = models.AutoField(primary_key=True, verbose_name='Numero Factura')
    fechaVenta = models.DateTimeField(verbose_name='Fecha', auto_now=True)
    empleado = models.ForeignKey(Empleado)
    cliente = models.ForeignKey(Cliente)
    bodega = models.ForeignKey(Bodega)
    descuento = models.BooleanField(verbose_name='Descuento',default=False)
    TotalVenta = models.IntegerField(verbose_name='Total Venta',default=0)

    def __unicode__(self):
        return self.numeroVenta

class DetalleVenta (models.Model):
    venta = models.ForeignKey(Venta)
    producto = models.ForeignKey(Producto,null=True)
    subproducto = models.ForeignKey(SubProducto, null=True)
    peso = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso en Venta',null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades en Venta',null= True,default=0)
    vrUnitario = models.IntegerField(verbose_name='Vr.Unitario', default=0)
    vrTotal = models.IntegerField(verbose_name='Vr.Total',default=0)


class Pedido(models.Model):
    numeroPedido = models.AutoField(primary_key=True, verbose_name='Numero Pedido')
    fechaPedido = models.DateTimeField(verbose_name='Fecha', auto_now=True)
    cliente = models.ForeignKey(Cliente)
    empleado = models.ForeignKey(Empleado)
    bodega = models.ForeignKey(Bodega)
    TotalVenta = models.IntegerField(verbose_name='Total Venta',default=0)
    descuento = models.BooleanField(verbose_name='Descuento',default=False)


    def __unicode__(self):
        return self.numeroPedido

class DetallePedido (models.Model):
    pedido = models.ForeignKey(Pedido)
    producto = models.ForeignKey(Producto,null=True)
    subproducto = models.ForeignKey(SubProducto, null=True)
    peso = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso(grs)',null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades',null= True,default=0)
    vrUnitario = models.IntegerField(verbose_name='Vr.Unitario', default=0)
    vrTotal = models.IntegerField(verbose_name='Vr.Total',default=0)
    estado = models.BooleanField(verbose_name='Estado',default=False)
