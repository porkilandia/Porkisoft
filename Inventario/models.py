from django.db import models

from Nomina.models import Empleado

# Create your models here.

class Bodega(models.Model):
    codigoBodega = models.AutoField(primary_key=True, verbose_name='Codigo Bodega')
    nombreBodega = models.CharField(max_length=50, verbose_name='Nombre')
    direccionBodega = models.CharField(max_length=50, verbose_name='Direccion')
    telefonoBodega = models.CharField(max_length=10,verbose_name='Telefono')

    def __unicode__(self):
        return self.nombreBodega

class Producto(models.Model):
    codigoProducto = models.AutoField(primary_key=True, verbose_name='Codigo Producto')
    nombreProducto = models.CharField(verbose_name = 'Nombre Producto',max_length=50)
    costoProducto = models.IntegerField(verbose_name = 'Costo Producto')
    vrVentaProducto = models.IntegerField(verbose_name = 'Valor de Venta')
    utilidadProducto = models.IntegerField(verbose_name = 'Ulilidad')
    rentabilidadProducto = models.DecimalField(verbose_name = 'Rentabilidad',max_digits=5, decimal_places=2 )
    gravado = models.BooleanField(verbose_name = 'Gravado')
    excento = models.BooleanField(verbose_name='Excento')
    excluido = models.BooleanField(verbose_name='Excluido')
    refrigerado = models.BooleanField(verbose_name = 'Refrigerado')
    congelado = models.BooleanField(verbose_name = 'Congelado')


    def __unicode__(self):
        return self.nombreProducto

class SubProducto(models.Model):
    codigoSubProducto= models.AutoField(verbose_name='Codigo', primary_key=True)
    nombreSubProducto = models.CharField(verbose_name = 'Nombre',max_length=50)
    costoSubProducto = models.IntegerField(verbose_name = 'Costo')
    vrVentaSubProducto = models.IntegerField(verbose_name = 'Vr. Venta')
    utilidadSubProducto = models.IntegerField(verbose_name = 'Ulilidad')
    rentabilidadSubProducto = models.DecimalField(verbose_name = 'Rentabilidad',max_digits=5, decimal_places=2 )
    gravado = models.BooleanField(verbose_name = 'Gravado')
    excento = models.BooleanField(verbose_name='Excento')
    excluido = models.BooleanField(verbose_name='Excluido')
    refrigerado = models.BooleanField(verbose_name = 'Refrigerado')
    congelado = models.BooleanField(verbose_name = 'Congelado')


    def __unicode__(self):
        return self.nombreSubProducto

class DetalleSubProducto(models.Model):
    subproducto = models.ForeignKey(SubProducto)
    producto = models.ForeignKey(Producto, verbose_name='Producto')
    pesoUnitProducto = models.DecimalField(verbose_name = 'Peso Producto (grs)',max_digits=9, decimal_places=3,null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades', null= True,default=0)

class ProductoBodega(models.Model):
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    pesoProductoStock = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Peso en  Stock')
    unidadesStock = models.IntegerField(verbose_name='Unidades en Stock')

class SubProductoBodega(models.Model):
    subProducto = models.ForeignKey(SubProducto)
    bodega = models.ForeignKey(Bodega)
    pesoSubProductoStock = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Peso en  Stock')

class Traslado(models.Model):

    OpEstTraslado = (
    ('ENV', 'Enviado'),
    ('REC', 'Recibido'),
    )
    codigoTraslado = models.AutoField(verbose_name='Codigo Traslado', primary_key=True)
    bodegaActual = models.ForeignKey(Bodega)
    bodegaDestino = models.IntegerField(verbose_name='Bodega Destino')
    empleado = models.ForeignKey(Empleado)
    fechaTraslado = models.DateTimeField(verbose_name='Fecha',auto_now=True)
    estadoTraslado = models.CharField(verbose_name='Estado',max_length=9,choices=OpEstTraslado)
    descripcionTraslado = models.TextField(verbose_name='Descriopcion', max_length=200)

    def __unicode__(self):
        return self.numeroTraslado

class DetalleTraslado (models.Model):
    traslado = models.ForeignKey(Traslado)
    producto = models.ForeignKey(Producto,null=True)
    SubProducto = models.ForeignKey(SubProducto,null=True)
    cantPiezas = models.IntegerField(verbose_name='Cant. Piezas')
    pesoPiezasTraslado = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Piezas (grs)',default=0,null=True)
    unidadesTraslado = models.IntegerField(verbose_name='Unidades', default=0,null=True)
    pesoEnvio = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Envio (grs)')
    pesoLlegada = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Llegada (grs)', null=True, default=0)

class Proveedor (models.Model):
    codigoProveedor = models.AutoField(primary_key=True)
    nit = models.CharField(verbose_name='Nit', max_length=11)
    nombreProv= models.CharField(max_length=50,verbose_name='Nombre')
    direccionProv = models.CharField(max_length=50, verbose_name='Direccion')
    telefonoProv = models.CharField(max_length=10,verbose_name='Telefono')
    email = models.EmailField(verbose_name='E-Mail')
    contacto = models.CharField(verbose_name='Contacto', max_length=50)
    ciudad = models.CharField(verbose_name='Ciudad',max_length=50)
    departamento = models.CharField (max_length=50)

    def __unicode__(self):

        return self.nombreProv

class Compra(models.Model):
    codigoCompra = models.AutoField(primary_key=True)
    encargado = models.ForeignKey(Empleado)
    proveedor = models.ForeignKey(Proveedor)
    fechaCompra = models.DateField(verbose_name='Fecha', auto_now=True, blank=True,null=True)
    vrCompra = models.IntegerField(verbose_name='Valor Compra', default=0)

    def __unicode__(self):
        return self.codigoCompra

class Ganado(models.Model):
    OpGenero = (
        ('M','Macho'),
        ('H' , 'Hembra'),
    )
    codigoGanado = models.AutoField(primary_key=True, verbose_name='Codigo Ganado')
    genero = models.CharField(verbose_name='Genero', choices=OpGenero, max_length=7)
    pesoEnPie = models.DecimalField(verbose_name = 'Peso en Pie (grs)',max_digits=9, decimal_places=3)
    precioKiloEnPie = models.IntegerField(verbose_name='Precio Kilo en Pie')
    precioTotal = models.IntegerField(verbose_name='Precio Total')
    difPieCanal = models.DecimalField(verbose_name='Diferencia de pie A canal',default=0,max_digits=9, decimal_places=3)
    fechaIngreso = models.DateField(auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.codigoGanado

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra)
    producto = models.ForeignKey(Producto, null=True, blank=True)
    ganado = models.ForeignKey(Ganado, null=True, blank=True)
    pesoProducto = models.DecimalField(verbose_name = 'Peso Producto (grs)',max_digits=9, decimal_places=3,null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades', null= True,default=0)
    vrCompraProducto = models.IntegerField(verbose_name = 'Valor de Compra')
    subtotal = models.IntegerField(default=0)
    estado = models.BooleanField()
