from django.db import models

from Nomina.models import Empleado

# Create your models here.

class Grupo(models.Model):
    nombreGrupo = models.CharField(verbose_name='Nombre', max_length=20)
    refrigerado = models.BooleanField(verbose_name = 'Refrigerado')
    congelado = models.BooleanField(verbose_name = 'Congelado')

    def __unicode__(self):
        return self.nombreGrupo

class Bodega(models.Model):
    codigoBodega = models.AutoField(primary_key=True, verbose_name='Codigo Bodega')
    nombreBodega = models.CharField(max_length=50, verbose_name='Nombre')
    direccionBodega = models.CharField(max_length=50, verbose_name='Direccion')
    telefonoBodega = models.CharField(max_length=10,verbose_name='Telefono')

    def __unicode__(self):
        return self.nombreBodega

class Producto(models.Model):
    codigoProducto = models.AutoField(primary_key=True, verbose_name='Codigo Producto')
    grupo = models.ForeignKey(Grupo)
    porcentajeCalidad = models.DecimalField(verbose_name = 'Calidad',max_digits=5, decimal_places=2, default=0 )
    nombreProducto = models.CharField(verbose_name = 'Nombre Producto',max_length=50)
    costoProducto = models.BigIntegerField(verbose_name = 'Costo Producto', default=0)
    vrVentaProducto = models.IntegerField(verbose_name = 'Valor de Venta', default=0)
    utilidadProducto = models.IntegerField(verbose_name = 'Ulilidad', default=0)
    rentabilidadProducto = models.DecimalField(verbose_name = 'Rentabilidad',max_digits=5, decimal_places=2, default=0 )
    gravado = models.BooleanField(verbose_name = 'Gravado', default=False)
    excento = models.BooleanField(verbose_name='Excento',default=False)
    excluido = models.BooleanField(verbose_name='Excluido',default=False)

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
    pesoProductoStock = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Peso en  Stock', default=0)
    pesoProductoKilos = models.IntegerField(verbose_name='Peso en  Stock(Kls)', default=0)
    unidadesStock = models.IntegerField(verbose_name='Unidades en Stock', default=0)

class SubProductoBodega(models.Model):
    subProducto = models.ForeignKey(SubProducto)
    bodega = models.ForeignKey(Bodega)
    pesoSubProductoStock = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Peso en  Stock')

class Traslado(models.Model):

    OpEstTraslado = (
    ('Enviado', 'Enviado'),
    ('Recibido', 'Recibido'),
    )


    codigoTraslado = models.AutoField(verbose_name='Codigo Traslado', primary_key=True)
    bodegaActual = models.ForeignKey(Bodega)
    bodegaDestino = models.CharField(max_length=10,verbose_name='Bodega Destino')
    empleado = models.ForeignKey(Empleado)
    fechaTraslado = models.DateField(verbose_name='Fecha',auto_now=True)
    estadoTraslado = models.CharField(verbose_name='Estado',max_length=9,choices=OpEstTraslado)
    descripcionTraslado = models.TextField(verbose_name='Descriopcion', max_length=200)

    def __unicode__(self):
        return self.codigoTraslado

class DetalleTraslado (models.Model):
    traslado = models.ForeignKey(Traslado)
    producto = models.ForeignKey(Producto,null=True,blank=True)
    SubProducto = models.ForeignKey(SubProducto,null=True,blank=True)
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

    tipoCompra = (
        ('insumo','Insumo'),
        ('ganado','Ganado'),
    )

    codigoCompra = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, verbose_name='Tipo de Compra',choices= tipoCompra)
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
    tipoPiel = (
        (25000,'Calentana'),
        (44000,'Firana'),
    )

    codigoGanado = models.AutoField(primary_key=True, verbose_name='Codigo Ganado')
    genero = models.CharField(verbose_name='Genero', choices=OpGenero, max_length=7)
    piel = models.IntegerField(verbose_name='Piel', choices= tipoPiel)
    pesoEnPie = models.DecimalField(verbose_name = 'Peso en Pie (grs)',max_digits=9, decimal_places=3)
    precioKiloEnPie = models.IntegerField(verbose_name='Precio Kilo en Pie')
    precioTotal = models.IntegerField(verbose_name='Precio Total')
    fechaIngreso = models.DateField(auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.codigoGanado

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra)
    producto = models.ForeignKey(Producto, null=True, blank=True)
    ganado = models.ForeignKey(Ganado, null=True, blank=True)
    pesoProducto = models.DecimalField(verbose_name = 'Peso Producto (grs)',max_digits=15   , decimal_places=3,null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades', null= True,default=0)
    vrCompraProducto = models.BigIntegerField(verbose_name = 'Valor de Compra')
    subtotal = models.BigIntegerField(default=0)
    estado = models.BooleanField()


class PlanillaRecepcion(models.Model):

    TipoGanado = (
        ('Mayor','Mayor'),
        ('Menor' , 'Menor'),
    )

    trans = (
        ('Frigovito','Frigovito'),
        ('Particular' , 'Particular'),
    )
    codigoRecepcion = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra)
    empleado = models.ForeignKey(Empleado)
    tipoGanado = models.CharField(verbose_name='Tipo Ganado', choices=TipoGanado, max_length=11)
    fechaRecepcion = models.DateField(verbose_name='fechaRecepcion',auto_now=True)
    cantCabezas = models.IntegerField(verbose_name='# Cabezas', default=0)
    provedor = models.ForeignKey(Proveedor)
    transporte = models.CharField(verbose_name='Transporte', choices=trans, max_length=11)
    difPieCanal = models.DecimalField(verbose_name='Diferencia de pie A canal',default=0,max_digits=9, decimal_places=3)


    def __unicode__(self):
        return self.codigoRecepcion


class Sacrificio(models.Model):


    recepcion = models.ForeignKey(PlanillaRecepcion)
    cantReses = models.IntegerField(verbose_name='Cantidad reses',default=0)
    piel = models.IntegerField(verbose_name='Piel',default=0)
    vrMenudo = models.IntegerField(verbose_name='Vr. Menudo', default=0)
    vrDeguello = models.IntegerField(verbose_name='Vr. Deguello', default=0)
    vrTransporte = models.IntegerField(verbose_name='Vr.Transporte', default=0)
    cola = models.DecimalField(verbose_name = 'Peso Cola',max_digits=9, decimal_places=3,null= True,default=0)
    rinones = models.DecimalField(verbose_name = 'Peso Rinyones',max_digits=9, decimal_places=3,null= True,default=0)
    creadillas = models.DecimalField(verbose_name = 'Peso Creadillas',max_digits=9, decimal_places=3,null= True,default=0)
    recortes = models.DecimalField(verbose_name = 'Peso Recortes',max_digits=9, decimal_places=3,null= True,default=0)
    desecho = models.DecimalField(verbose_name = 'Peso Desecho',max_digits=9, decimal_places=3,null= True,default=0)
    fechaSacrificio = models.DateField(verbose_name='Fecha Sacrificio',auto_now=True)


    def __unicode__(self):
        return self.id



