from django.db import models
# Create your models here.

class Producto(models.Model):
    nombreProducto = models.CharField(verbose_name = 'Nombre Producto',max_length=50)
    pesoProducto = models.DecimalField(verbose_name = 'Peso Producto (grs)',max_digits=9, decimal_places=3)
    costoProducto = models.IntegerField(verbose_name = 'Costo Producto')
    vrCompraProducto = models.IntegerField(verbose_name = 'Valor de Compra')
    gravado = models.BooleanField(verbose_name = 'Gravado')
    utilidadProducto = models.IntegerField(verbose_name = 'Ulilidad')
    rentabilidadProducto = models.IntegerField(verbose_name = 'Rentabilidad')
    refrigerado = models.BooleanField(verbose_name = 'Refrigerado')
    congelado = models.BooleanField(verbose_name = 'Congelado')
    
    def __unicode__(self):
        return self.nombreProducto
        



