from django.db import models
from Telemercadeo.models import *
from Inventario.models import Bodega,Producto,SubProducto
from Nomina.models import Empleado

# Create your models here.
class ListaDePrecios(models.Model):
    codigoLista = models.AutoField(primary_key=True)
    fecha = models.DateField(verbose_name='Fecha')
    nombreLista = models.CharField(max_length=50,verbose_name='Nombre')

    def __unicode__(self):
        cadena = '%d | %s'%(self.codigoLista,self.nombreLista)
        return cadena

class DetalleLista(models.Model):
    lista = models.ForeignKey(ListaDePrecios,verbose_name='Lista')
    productoLista = models.ForeignKey(Producto,verbose_name='Producto')
    costoKilo = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Costo Kilo',null= True,default=0)
    precioVenta = models.IntegerField(verbose_name='Precio Venta')


class Venta(models.Model):
    jornadas = (
    ('AM', 'AM'),
    ('PM', 'PM'),
    )
    numeroVenta = models.AutoField(primary_key=True, verbose_name='Numero Factura')
    fechaVenta = models.DateField(verbose_name='Fecha')
    lista = models.ForeignKey(ListaDePrecios,null=True,blank=True)
    bodega = models.ForeignKey(Bodega)
    TotalRegistradora = models.IntegerField(verbose_name='Total Registradora',default=0)
    TotalVenta = models.IntegerField(verbose_name='Total Venta',default=0)
    TotalCredito = models.IntegerField(verbose_name='Total Credito',default=0)
    TotalContado = models.IntegerField(verbose_name='Total Contado',default=0)
    efectivo = models.IntegerField(verbose_name='Efectivo',default=0)
    descuadre = models.IntegerField(verbose_name='Descuadre',default=0)
    residuo = models.IntegerField(default=0)
    jornada = models.CharField(verbose_name='Jornada',max_length=5,choices=jornadas)

    def __unicode__(self):
        return self.numeroVenta

class DetalleVenta (models.Model):
    venta = models.ForeignKey(Venta)
    peso = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso en Venta',null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades en Venta',null= True,default=0)
    productoVenta = models.ForeignKey(Producto,null=True)
    vrUnitario = models.IntegerField(verbose_name='Vr.Unitario', default=0)
    vrTotal = models.IntegerField(verbose_name='Vr.Total',default=0)
    credito = models.BooleanField(verbose_name='Credito',default=False)
    contado = models.BooleanField(verbose_name='Contado',default=False)



class Pedido(models.Model):
    numeroPedido = models.AutoField(primary_key=True, verbose_name='Numero Pedido')
    numeroFactura = models.BigIntegerField(verbose_name='Factura No.',default=0)
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



