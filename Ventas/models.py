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
    restaurante = models.BooleanField(default=False,verbose_name='Restaurantes')
    guardado = models.BooleanField(default=False,verbose_name='Guardado')

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
    listaPrecioPedido = models.ForeignKey(ListaDePrecios,verbose_name='Lista Precios')
    cliente = models.ForeignKey(Cliente)
    empleado = models.ForeignKey(Empleado)
    bodega = models.ForeignKey(Bodega)
    TotalVenta = models.IntegerField(verbose_name='Total Venta',default=0)
    credito = models.BooleanField(verbose_name='Credito',default=False)
    contado = models.BooleanField(verbose_name='Contado',default=False)

    def __unicode__(self):
        return self.numeroPedido

class DetallePedido (models.Model):
    pedido = models.ForeignKey(Pedido)
    producto = models.ForeignKey(Producto,null=True)
    subproducto = models.ForeignKey(SubProducto, null=True)
    pesoPedido = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso(grs)',null= True,default=0)
    unidadesPedido = models.IntegerField(verbose_name='Unidades',null= True,default=0)
    vrUnitario = models.IntegerField(verbose_name='Vr.Unitario', default=0)
    vrTotalPedido = models.IntegerField(verbose_name='Vr.Total',default=0)
    estado = models.BooleanField(verbose_name='Estado',default=False)

class VentaPunto(models.Model):
    jornadas = (
    ('AM', 'AM'),
    ('PM', 'PM'),
    )

    numeroVenta = models.AutoField(primary_key=True, verbose_name='Codigo')
    factura = models.IntegerField(verbose_name='No.Factura',default=0)
    encargado = models.ForeignKey(Empleado,verbose_name='Encargado')
    jornada = models.CharField(verbose_name='Jornada',max_length=5,choices=jornadas)
    fechaVenta = models.DateField(verbose_name='Fecha',auto_now=True)
    TotalVenta = models.IntegerField(verbose_name='Total Venta',default=0)
    restaurante = models.BooleanField(verbose_name='Restaurante',default=False)
    guardado = models.BooleanField(default=False,verbose_name='Guardado')

    def __unicode__(self):
        return self.numeroVenta

class DetalleVentaPunto (models.Model):
    venta = models.ForeignKey(VentaPunto)
    productoVenta = models.ForeignKey(Producto,null=True,verbose_name='Producto')
    pesoVentaPunto = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso',null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades',null= True,default=0)
    vrUnitarioPunto = models.IntegerField(verbose_name='Vr.Unitario', default=0)
    vrTotalPunto = models.IntegerField(verbose_name='Vr.Total',default=0)


class Caja (models.Model):
    jornadas = (
    ('AM', 'AM'),
    ('PM', 'PM'),
    )
    numeroCaja = models.AutoField(primary_key=True, verbose_name='Numero Caja')
    fechaCaja = models.DateField(verbose_name='Fecha')
    jornada = models.CharField(verbose_name='Jornada',max_length=5,choices=jornadas)
    encargado = models.ForeignKey(Empleado,verbose_name='Encargado')
    base = models.IntegerField(verbose_name='Base',default=0)
    TotalVenta = models.IntegerField(verbose_name='Venta',default=0)
    TotalRetiro = models.IntegerField(verbose_name='Venta',default=0)
    TotalRestaurante = models.IntegerField(verbose_name='Venta',default=0)
    TotalCaja = models.IntegerField(verbose_name='Caja',default=0)
    TotalEfectivo = models.IntegerField(verbose_name='Efectivo',default=0)
    TotalResiduo = models.IntegerField(verbose_name='Residuo',default=0)

class Retiros (models.Model):
    jornadas = (
    ('AM', 'AM'),
    ('PM', 'PM'),
    )

    fechaRetiro = models.DateField(verbose_name='Fecha',auto_now=True)
    encargado = models.ForeignKey(Empleado,verbose_name='Encargado')
    jornada = models.CharField(verbose_name='Jornada',max_length=5,choices=jornadas)
    nombreEncargado = models.CharField(verbose_name='Nombre Empleado',max_length=50,blank=True)
    cantidad = models.IntegerField(verbose_name='Cantidad',default=0)
    observacion = models.TextField(verbose_name='Observacion')
    guardado = models.BooleanField(default=False,verbose_name='Guardado')


class Devolucion (models.Model):

    fechaDevolucion = models.DateField(verbose_name='Fecha',auto_now=True)
    encargado = models.ForeignKey(Empleado,verbose_name='Encargado')
    observacion = models.TextField(verbose_name='Observacion')
    guardado = models.BooleanField(default=False,verbose_name='Guardado')

    def __unicode__(self):
        return self.id

class DetalleDevolucion (models.Model):

    devolucion = models.ForeignKey(Devolucion)
    productoDev = models.ForeignKey(Producto,verbose_name='Producto')
    pesoProducto = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso',null= True,default=0)
    cantidad = models.IntegerField(verbose_name='Und',default=0)

