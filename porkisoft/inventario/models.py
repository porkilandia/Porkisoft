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
    pesoUnitProducto = models.DecimalField(verbose_name = 'Peso Producto (grs)',max_digits=9, decimal_places=3,null= False)
    unidades = models.IntegerField(verbose_name='Unidades', null= False)



class ProductoBodega(models.Model):
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    pesoProductoStock = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Peso en  Stock')
    unidadesStock = models.IntegerField(verbose_name='Unidades en Stock')



class SubProductoBodega(models.Model):
    subProducto = models.ForeignKey(SubProducto)
    bodega = models.ForeignKey(Bodega)
    pesoSubProductoStock = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Peso en  Stock')





