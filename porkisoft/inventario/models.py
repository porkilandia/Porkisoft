from django.db import models
# Create your models here.



class Bodega(models.Model):
    nombreBodega = models.CharField(max_length=50, verbose_name='Nombre')
    direccionBodega = models.CharField(max_length=50, verbose_name='Direccion')
    telefonoBodega = models.CharField(max_length=10,verbose_name='Telefono')

    def __unicode__(self):
        return self.nombreBodega

class Producto(models.Model):
    nombreProducto = models.CharField(verbose_name = 'Nombre Producto',max_length=50)
    costoProducto = models.IntegerField(verbose_name = 'Costo Producto')
    vrCompraProducto = models.IntegerField(verbose_name = 'Valor de Compra')
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
    nombreSubProducto = models.CharField(verbose_name = 'Nombre Sub Producto',max_length=50)
    costoSubProducto = models.IntegerField(verbose_name = 'Costo Sub Producto')
    vrVentaSubProducto = models.IntegerField(verbose_name = 'Valor de Venta')
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

class Cargo(models.Model):
    nombreCargo = models.CharField(max_length=50, verbose_name='Cargo')
    horasDia = models.IntegerField(verbose_name='Horas al Dia')

class Cliente (models.Model):
    nombreCliente = models.CharField(max_length=50)
    telefonoCliente = models.CharField(max_length=10,verbose_name='Telefono')
    direccionCliente = models.CharField(max_length=50,verbose_name='Direccion')

class Empleado(models.Model):
    nombre = models.CharField(max_length= 50, verbose_name='Nombre')
    apellido = models.CharField(max_length= 50, verbose_name='Apellido')
    direccion = models.CharField(max_length=100,verbose_name='Direccion')
    telefono = models.CharField(max_length=10,verbose_name='Telefono')
    cargo = models.ForeignKey(Cargo)

class Venta(models.Model):
    numeroVenta = models.CharField(max_length=9,unique=True, verbose_name='Numero Factura')
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

class Traslado(models.Model):

    OpEstTraslado = (
    ('ENV', 'Enviado'),
    ('REC', 'Recibido'),
    )

    bodegaActual = models.ForeignKey(Bodega)
    bodegaDestino = models.ForeignKey(Bodega)
    empleado = models.ForeignKey(Empleado)
    fechaTraslado = models.DateTimeField(verbose_name='Fecha',auto_now=True)
    estadoTraslado = models.CharField(verbose_name='Estado',choices=OpEstTraslado)
    descripcionTraslado = models.TextField(verbose_name='Descriopcion', max_length=200)
    encargadoTransporte = models.ForeignKey(Empleado)
    encargadoRecepcion = models.ForeignKey(Empleado)

class DetalleTraslado (models.Model):
    traslado = models.ForeignKey(Traslado)
    producto = models.ForeignKey(Producto,null=True)
    SubProducto = models.ForeignKey(SubProducto,null=True)
    cantPiezas = models.IntegerField(verbose_name='Cant. Piezas')
    pesoPiezasTraslado = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Piezas (grs)',default=0,null=True)
    unidadesTraslado = models.IntegerField(verbose_name='Unidades', default=0,null=True)
    pesoEnvio = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Envio (grs)')
    pesoLlegada = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Llegada (grs)', null=True)

class Proveedor (models.Model):
    nombreProv= models.CharField(max_length=50,verbose_name='Nombre')
    direccionProv = models.CharField(max_length=50, verbose_name='Direccion')
    telefonoProv = models.CharField(max_length=10,verbose_name='Telefono')
    email = models.EmailField(verbose_name='E-Mail')
    contacto = models.CharField(verbose_name='Contacto', max_length=50)
    ciudad = models.CharField(verbose_name='Ciudad')
    municipio = models.CharField ()

    def __unicode__(self):
        return self.nombreProv

class Compra(models.Model):
    encargado = models.ForeignKey(Empleado)
    proveedor = models.ForeignKey(Proveedor)
    fechaCompra = models.DateTimeField(verbose_name='Fecha', auto_now=True)
    vrCompra = models.IntegerField(verbose_name='Valor Compra')

class Ganado(models.Model):
    OpGenero = (
        ('M','Macho'),
        ('H' , 'Hembra'),
    )
    lote = models.CharField(max_length=6)
    genero = models.CharField(verbose_name='Genero', choices=OpGenero, max_length=7)
    pesoEnPie = models.DecimalField(verbose_name = 'Peso en Pie (grs)',max_digits=9, decimal_places=3)
    precioKiloEnPie = models.IntegerField()
    precioTotal = models.IntegerField()
    difPieCanal = models.DecimalField(verbose_name='Diferencia de pie A canal',max_digits=9, decimal_places=3)

    def __unicode__(self):
        return self.lote

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra)
    producto = models.ForeignKey(Producto, null=True)
    ganado = models.ForeignKey(Ganado, null=True)
    pesoProducto = models.DecimalField(verbose_name = 'Peso Producto (grs)',max_digits=9, decimal_places=3,null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades', null= True,default=0)

class Canal (models.Model):
    numeroCanal = models.CharField(max_length=9, unique=True)
    ganado = models.ForeignKey(Ganado)
    pesoPiernas = models.DecimalField(verbose_name = 'Peso Piernas (grs)',max_digits=9, decimal_places=3)
    pesoBrazos = models.DecimalField(verbose_name = 'Peso Brazos (grs)',max_digits=9, decimal_places=3)
    peosTotalCanal = models.DecimalField(verbose_name = 'Peso Total (grs)',max_digits=9, decimal_places=3)

    def __unicode__(self):
        return self.numeroCanal


class PlanillaDesposte(models.Model):
    nuemroPlanilla = models.CharField(max_length=9,unique=True)
    canal = models.ForeignKey(Canal)
    fechaDesposte = models.DateTimeField(verbose_name='Fecha de Desposte', auto_now=True)
    resesADespostar = models.IntegerField(verbose_name='Reses A Despostar')
    totalDespostado = models.DecimalField(verbose_name='TotalDespostado',max_digits=9, decimal_places=3)
    difCanalADespostado = models.DecimalField(verbose_name='Diferencia de Canal A Despostado',max_digits=9, decimal_places=3)

    def __unicode__(self):
        return self.nuemroPlanilla

class DesposteCanal(models.Model):
    canal = models.ForeignKey(Canal)
    planillaDesposte = models.ForeignKey(PlanillaDesposte)

class DetallePlanilla (models.Model):
    planilla = models.ForeignKey(PlanillaDesposte)
    producto = models.ForeignKey(Producto)
    CantPiezas = models.IntegerField(verbose_name='Cantidad Piezas')
    PesoProducto = models.DecimalField(max_length=9,max_digits=3, verbose_name='Peso Producto')







