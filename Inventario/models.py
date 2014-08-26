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
    SubGrupo = (
    ('Calidad 1', 'Calidad 1'),
    ('Calidad 2', 'Calidad 2'),
    ('Calidad 3', 'Calidad 3'),
    )
    codigoProducto = models.AutoField(primary_key=True, verbose_name='Codigo Producto')
    grupo = models.ForeignKey(Grupo)
    subGrupo = models.CharField(verbose_name='SubGrupo',max_length=20,choices=SubGrupo,default=0)
    nombreProducto = models.CharField(verbose_name = 'Nombre Producto',max_length=50)
    costoProducto = models.BigIntegerField(verbose_name = 'Costo Producto', default=0)
    vrVentaLorenzo = models.IntegerField(verbose_name = 'Vr. Lorenzo', default=0)
    vrVentaCentro = models.IntegerField(verbose_name = 'Vr. Centro', default=0)
    vrVentaPotrerillo = models.IntegerField(verbose_name = 'Vr. Potrerillo', default=0)
    vrVentaNorte = models.IntegerField(verbose_name = 'Vr.Norte', default=0)
    vrVentaContado = models.IntegerField(verbose_name = 'Vr. Contado', default=0)
    vrVentaCredito = models.IntegerField(verbose_name = 'Vr. Credito', default=0)
    precioSugerido = models.IntegerField(verbose_name='Precio Sugerido', default=0)
    gravado = models.BooleanField(verbose_name = 'Gravado', default=False)
    excento = models.BooleanField(verbose_name='Excento',default=False)
    excluido = models.BooleanField(verbose_name='Excluido',default=False)

    def __unicode__(self):
        cadena = '%d %s (%s)'%(self.codigoProducto,self.nombreProducto,self.grupo.nombreGrupo)
        return cadena
    class Meta:
        ordering = ['codigoProducto']



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
    bodegaDestino = models.CharField(max_length=20,verbose_name='Bodega Destino')
    empleado = models.ForeignKey(Empleado)
    fechaTraslado = models.DateField(verbose_name='Fecha')
    estadoTraslado = models.CharField(verbose_name='Estado',max_length=9,choices=OpEstTraslado)
    descripcionTraslado = models.TextField(verbose_name='Descriopcion', max_length=200)
    guardado = models.BooleanField(verbose_name='Guardado',default=False)

    def __unicode__(self):
        return self.codigoTraslado

    class Meta:
        ordering = ['-fechaTraslado']

class DetalleTraslado (models.Model):
    traslado = models.ForeignKey(Traslado)
    pesoTraslado = models.DecimalField(max_digits=9, decimal_places=3,verbose_name='Peso Traslado (grs)',default=0,null=True)
    productoTraslado = models.ForeignKey(Producto,null=True,blank=True)
    SubProducto = models.ForeignKey(SubProducto,null=True,blank=True)
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
    tipo = models.ForeignKey(Grupo)
    encargado = models.ForeignKey(Empleado)
    proveedor = models.ForeignKey(Proveedor)
    fechaCompra = models.DateField(verbose_name='Fecha',blank=True,null=True)
    vrCompra = models.IntegerField(verbose_name='Valor Compra', default=0)
    vrTransporte = models.IntegerField(verbose_name='Transporte',default= 0)

    def __unicode__(self):
        cadena = "%s -- $%d"%(str(self.fechaCompra),self.vrCompra)
        return cadena

class Ganado(models.Model):

    tipoPiel = (
        (25000,'Calentana'),
        (44000,'Friana'),
    )

    codigoGanado = models.AutoField(primary_key=True, verbose_name='Codigo Ganado')
    compra = models.ForeignKey(Compra,blank=True,null=True)
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
    pesoProducto = models.DecimalField(verbose_name = 'Peso(grs)',max_digits=15   , decimal_places=3,null= True,default=0)
    unidades = models.IntegerField(verbose_name='Unidades', null= True,default=0)
    subtotal = models.BigIntegerField(verbose_name='Vr.Factura',default=0)
    vrCompraProducto = models.BigIntegerField(verbose_name = 'Costo Kilo/Unidad',default= 0)
    pesoDescongelado = models.DecimalField(verbose_name = 'Peso Desc(grs)',max_digits=15   , decimal_places=3,null= True,default=0)
    vrKiloDescongelado = models.BigIntegerField(verbose_name = 'Costo Kilo/Desc.',default= 0)
    estado = models.BooleanField()

    def __unicode__(self):
        return self.id


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
    fechaRecepcion = models.DateField(verbose_name='fechaRecepcion')
    cantCabezas = models.IntegerField(verbose_name='# Cabezas', default=0)
    provedor = models.ForeignKey(Proveedor)
    vrTransporte = models.IntegerField(verbose_name='Vr.Transporte',default=0)
    transporte = models.CharField(verbose_name='Transporte', choices=trans, max_length=11)
    difPieCanal = models.DecimalField(verbose_name='Diferencia de pie A canal',default=0,max_digits=9, decimal_places=3)
    pesoCanales = models.DecimalField(verbose_name='Peso Canales',default=0,max_digits=9, decimal_places=3)
    vrKiloCanal = models.IntegerField(verbose_name='Vr. Kilo Canal',default=0)


    def __unicode__(self):
        return self.codigoRecepcion

class ListadoPrecios(models.Model):
    nombreLista = models.CharField(verbose_name='Nombre',max_length=50)
