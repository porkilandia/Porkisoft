from Inventario.models import *

class Ensalinado(models.Model):
    codigoEnsalinado = models.AutoField(primary_key=True)
    fechaEnsalinado = models.DateField(verbose_name='Fecha',auto_now=True)
    producto = models.ForeignKey(Producto)
    pesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3)
    pesoSal = models.DecimalField(verbose_name='Peso Sal', max_digits=9, decimal_places=3)
    pesoPapaina = models.DecimalField(verbose_name='Peso Papaina', max_digits=9, decimal_places=3)
    pesoProductoAntes = models.DecimalField(verbose_name='Peso pre', max_digits=9, decimal_places=3, default=0)
    pesoProductoDespues = models.DecimalField(verbose_name='Peso pos', max_digits=9, decimal_places=3, default=0)
    costoKilo = models.IntegerField(verbose_name='Costo Kilo', default=0)
    costoTotal = models.IntegerField(verbose_name='Costo Total', default=0)

class LimpiezaVerduras(models.Model):
    compra = models.ForeignKey(DetalleCompra)
    producto = models.ForeignKey(Producto)
    cif = models.DecimalField(verbose_name='CIF', max_digits=9, decimal_places=3, default=0)
    mod = models.DecimalField(verbose_name='MOD', max_digits=9, decimal_places=3, default=0)
    pesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3, default=0)
    vrKilo = models.IntegerField(verbose_name='Vr. Kilo',default=0)

class Enlagunado(models.Model):
    codigoEnlagunado = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto)
    pesoAntesLaguna = models.DecimalField(verbose_name='Peso antes de enlagunado', max_digits=9, decimal_places=3)
    fechaEnlagunado = models.DateTimeField(verbose_name='Fecha Proceso', auto_now=True)
    costoEnlagunado = models.IntegerField(verbose_name='Costo Enlagunado')

    def __int__(self):
        return self.codigoEnlagunado

class DetalleEnlagunado(models.Model):
    enlagunado = models.ForeignKey(Enlagunado)
    producto = models.ForeignKey(Producto)
    pesoPorducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3)
    costoProducto = models.IntegerField()

class CondimentadoTajado(models.Model):
    codigoTajado = models.AutoField(primary_key=True)
    producto  = models.ForeignKey(Producto)
    pesoProductoEnsalinado =models.DecimalField(verbose_name='Peso', max_digits=9, decimal_places=3)
    condimento = models.DecimalField(verbose_name='Condimento', max_digits=9, decimal_places=3)
    filete = models.DecimalField(verbose_name='Filete', max_digits=9, decimal_places=3)
    recortes = models.DecimalField(verbose_name='Recortes', max_digits=9, decimal_places=3)
    procesos = models.DecimalField(verbose_name='Procesos', max_digits=9, decimal_places=3)

    def __int__(self):
        return self.codigoTajado

class PlanillaDesposte(models.Model):
    codigoPlanilla = models.AutoField(primary_key=True)
    fechaDesposte = models.DateField(verbose_name='Fecha de Desposte', auto_now=True)
    resesADespostar = models.IntegerField(verbose_name='Reses A Despostar', default=0)
    totalDespostado = models.DecimalField(verbose_name='Total Despostado',max_digits=9, decimal_places=3, default=0)
    totalCanal = models.DecimalField(verbose_name='Total Canal',max_digits=11, decimal_places=3, default=0)
    difCanalADespostado = models.DecimalField(verbose_name='Diferencia de Canal/Desposte',max_digits=11,
                                              decimal_places=3, default=0)
    costoProduccionTotal = models.IntegerField(verbose_name='Costo Produccion Total',default=0)

    def __unicode__(self):
        return self.codigoPlanilla

class Canal (models.Model):

    OpGenero = (
        ('Macho','Macho'),
        ('Hembra' , 'Hembra'),
    )

    recepcion = models.ForeignKey(PlanillaRecepcion)
    codigoCanal = models.AutoField(primary_key=True)
    planilla = models.ForeignKey(PlanillaDesposte,null=True, blank=True)
    pesoFrigovito = models.DecimalField(verbose_name = 'Peso Frigovito',max_digits=9, decimal_places=3,null= True,default=0)
    pesoPorkilandia = models.DecimalField(verbose_name = 'Peso Porkilandia',max_digits=9, decimal_places=3,null= True,default=0)
    difPesos = models.DecimalField(verbose_name='Dif. Frig/Pork',default=0,max_digits=9, decimal_places=3)
    vrKiloCanal = models.IntegerField(verbose_name='Vr. Kilo Canal',default=0)
    vrArrobaCanal = models.IntegerField(verbose_name='Vr. Arroba Canal',default=0)
    genero = models.CharField(verbose_name='Genero', choices=OpGenero,default='Macho', max_length=7)
    estado = models.BooleanField(verbose_name='A desposte', default = False)


    def __unicode__(self):
        return self.numeroCanal


class DetallePlanilla (models.Model):
    planilla = models.ForeignKey(PlanillaDesposte)
    producto = models.ForeignKey(Producto)
    PesoProducto = models.DecimalField(max_digits=9,decimal_places=3, verbose_name='Peso Producto')

class Formula(models.Model):
    codigoFormula = models.AutoField(primary_key=True)
    responsable = models.ForeignKey(Empleado)
    pesoFormula = models.DecimalField(verbose_name='Peso Formula', max_digits=9, decimal_places=3)
    cantidadFormulas = models.IntegerField(verbose_name='Cantidad Formulas')
    costoFormulas = models.IntegerField(verbose_name='Costo Formulas')
    fechaElaboracion = models.DateTimeField(verbose_name='Fecha de Elaboracion', auto_now=True)
    fechaCaducidad = models.DateTimeField(verbose_name='Fecha de Caducidad')

    def __int__(self):
        return self.codigoFormula

class DetalleFormula(models.Model):
    formula = models.ForeignKey(Formula)
    producto = models.ForeignKey(Producto)
    pesoUnitProducto = models.DecimalField(verbose_name='Peso Unitario Producto', max_digits=9, decimal_places=3)

class Condimentado (models.Model):
    codigoCondimentado = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto)
    formula = models.ForeignKey(Formula)
    pesoProductoACondimentar = models.DecimalField(verbose_name='Peso Producto A Condimentar', max_digits=9, decimal_places=3)
    pesoFormulaUsada = models.DecimalField(verbose_name='Peso Formula',max_digits=9, decimal_places=3)
    pesoProductoCondimentado = models.DecimalField(verbose_name='Peso Producto Condimentado', max_digits=9, decimal_places=3)

    def __int__(self):
        return self.codigoCondimentado

class Miga(models.Model):
    codigoMiga = models.AutoField(primary_key=True)
    cantidadFormulas = models.DecimalField(verbose_name='Formulas', max_digits=9, decimal_places=3,default=0)
    fechaFabricacion = models.DateTimeField(verbose_name='Fecha De Fabricacion',auto_now=True)
    PesoFormulaMiga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3)
    costoFormulaMiga = models.IntegerField(verbose_name='Costo Formula',default=0)
    costoKiloMigaProcesada = models.IntegerField(verbose_name='Costo Kilo',default=0)

    def __unicode__(self):
        return self.codigoMiga

class DetalleMiga(models.Model):

    miga= models.ForeignKey(Miga)
    producto = models.ForeignKey(Producto)
    PesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3)
    costoProducto = models.IntegerField(verbose_name='Costo' , default=0)
    costoTotalProducto = models.IntegerField(verbose_name='Costo Total',default= 0 )


class Apanado(models.Model):
    codigoApanado = models.AutoField(primary_key=True)
    miga = models.ForeignKey(Miga)
    producto = models.ForeignKey(Producto)
    PesoProducto = models.DecimalField(verbose_name='Peso Producto',help_text='Peso del producto a apanar', max_digits=9, decimal_places=3)
    PesoMiga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3)
    undProducto =models.IntegerField(verbose_name='Unidades')
    PesoPosApanado = models.DecimalField(verbose_name='Peso producto Pos-Apanado', max_digits=9, decimal_places=3)
    costoPosApanado = models.IntegerField(verbose_name='Costo Pos-Apanado')

    def __int__(self):
        return self.codigoApanado

class Condimento(models.Model):
    codigoCondimento = models.AutoField(primary_key= True)
    fecha = models.DateField(verbose_name='Fecha', auto_now= True)
    cantFormulas = models.IntegerField(verbose_name='Cantidad de formulas',default=0)
    pesoCondimento = models.DecimalField(verbose_name='Peso grs.',default=0, max_digits=9, decimal_places=3)
    costoCondimento = models.IntegerField(verbose_name='Costo Condimento',default=0)
    costoLitroCondimento = models.IntegerField(verbose_name='Costo litro',default=0)

    def __unicode__(self):
        return  self.codigoCondimento

class DetalleCondimento(models.Model):
    condimento = models.ForeignKey(Condimento)
    producto = models.ForeignKey(Producto)
    pesoProducto = models.DecimalField(verbose_name='Peso grs.', max_digits=9, decimal_places=3)
    costoProducto = models.IntegerField(verbose_name='Costo' , default=0)
    costoTotalProducto = models.IntegerField(verbose_name='Costo Total',default= 0 )