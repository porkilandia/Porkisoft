from datetime import date
from Inventario.models import *
from Nomina.models import *

class Ensalinado(models.Model):
    codigoEnsalinado = models.AutoField(primary_key=True)
    fechaEnsalinado = models.DateField(verbose_name='Fecha')
    pesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3)
    productoEnsalinado = models.ForeignKey(Producto)
    pesoSal = models.DecimalField(verbose_name='Peso Sal', max_digits=9, decimal_places=3)
    pesoPapaina = models.DecimalField(verbose_name='Peso Papaina', max_digits=9, decimal_places=3)
    pesoProductoAntes = models.DecimalField(verbose_name='Peso pre', max_digits=9, decimal_places=3, default=0)
    mod = models.IntegerField(verbose_name='MOD',default=0)
    pesoProductoDespues = models.DecimalField(verbose_name='Peso pos', max_digits=9, decimal_places=3, default=0)
    costoKilo = models.IntegerField(verbose_name='Costo Kilo', default=0)
    costoTotal = models.IntegerField(verbose_name='Costo Total', default=0)
    guardado = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)


class LimpiezaVerduras(models.Model):
    hoy = date.today()
    fechaLimpieza = models.DateField(verbose_name='Fecha',default=hoy)
    productoLimpiar = models.ForeignKey(Producto)
    pesoProducto = models.DecimalField(verbose_name='Peso Antes', max_digits=9, decimal_places=3, default=0)
    pesoDespues = models.DecimalField(verbose_name='Peso Despues', max_digits=9, decimal_places=3, default=0)
    compra = models.ForeignKey(Compra,verbose_name='Compra')
    valorProducto = models.IntegerField(verbose_name='Valor Producto')
    valorTransporte = models.IntegerField(verbose_name='Valor Transporte')
    cif = models.DecimalField(verbose_name='CIF', max_digits=9, decimal_places=3, default=0)
    mod = models.DecimalField(verbose_name='MOD', max_digits=9, decimal_places=3, default=0)
    vrKilo = models.IntegerField(verbose_name='Vr. Kilo',default=0)
    guardado = models.BooleanField(default=False)

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

class PlanillaDesposte(models.Model):
    codigoPlanilla = models.AutoField(primary_key=True)
    fechaDesposte = models.DateField(verbose_name='Fecha de Desposte')
    resesADespostar = models.IntegerField(verbose_name='Reses A Despostar', default=0)
    totalDespostado = models.DecimalField(verbose_name='Total Despostado',max_digits=13, decimal_places=3, default=0)
    totalCanal = models.DecimalField(verbose_name='Total Canal',max_digits=11, decimal_places=3, default=0)
    difCanalADespostado = models.DecimalField(verbose_name='Diferencia de Canal/Desposte',max_digits=11,
                                              decimal_places=3, default=0)
    guardado = models.BooleanField(default=False)
    tipoDesposte = models.CharField(verbose_name='Tipos Desposte',blank=True,null=True,max_length=15)
    cif = models.IntegerField(verbose_name='CIf',default=0)
    mod = models.IntegerField(verbose_name='MOD',default=0)

    def __unicode__(self):

        cadena = '%s %s'%(self.fechaDesposte,self.tipoDesposte)
        return cadena

class Tajado(models.Model):
    codigoTajado = models.AutoField(primary_key=True)
    fechaTajado = models.DateField(verbose_name='Fecha de Tajado')
    responsable = models.ForeignKey(Empleado)
    producto  = models.ForeignKey(Producto)
    desposteHistorico = models.ForeignKey(PlanillaDesposte,verbose_name='Desposte',blank= True, null=True)
    polloHistorico = models.ForeignKey(Compra,verbose_name='Compras',blank= True, null=True)
    pesoProducto =models.DecimalField(verbose_name='Peso', max_digits=9, decimal_places=3)
    totalTajado = models.DecimalField(verbose_name='Total Tajado', max_digits=9, decimal_places=3,default=0)
    costoKiloFilete = models.IntegerField(verbose_name='Costo Kilo',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    guardado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.codigoTajado

class DetalleTajado(models.Model):
    tajado = models.ForeignKey(Tajado)
    producto  = models.ForeignKey(Producto)
    unidades = models.IntegerField(verbose_name='Unds',default=0)
    costoKilo = models.IntegerField(verbose_name='Costo Kilo',default=0)
    pesoProducto =models.DecimalField(verbose_name='Peso', max_digits=9, decimal_places=3)



class Canal (models.Model):

    OpGenero = (
        ('Macho','Macho'),
        ('Hembra' , 'Hembra'),
    )

    recepcion = models.ForeignKey(PlanillaRecepcion)
    codigoCanal = models.AutoField(primary_key=True)
    planilla = models.ForeignKey(PlanillaDesposte, null=True, blank=True)
    nroCanal = models.IntegerField(verbose_name='Numero',default=0)
    pesoFrigovito = models.DecimalField(verbose_name = 'Peso Frigovito',max_digits=9, decimal_places=3,null= True,default=0)
    pesoPorkilandia = models.DecimalField(verbose_name = 'Peso Porkilandia',max_digits=9, decimal_places=3,null= True,default=0)
    difPesos = models.DecimalField(verbose_name='Dif. Frig/Pork',default=0,max_digits=9, decimal_places=3)
    vrKiloCanal = models.IntegerField(verbose_name='Vr. Kilo Canal',default=0)
    vrArrobaCanal = models.IntegerField(verbose_name='Vr. Arroba Canal',default=0)
    genero = models.CharField(verbose_name='Genero', choices=OpGenero,default='Macho', max_length=7)
    estado = models.BooleanField(verbose_name='A desposte', default = False)


    def __unicode__(self):
        return self.numeroCanal

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
    ubre = models.DecimalField(verbose_name = 'Ubre',max_digits=9, decimal_places=3,null= True,default=0)
    desecho = models.DecimalField(verbose_name = 'Peso Desecho',max_digits=9, decimal_places=3,null= True,default=0)
    fechaSacrificio = models.DateField(verbose_name='Fecha Sacrificio',blank=True,null=True)


    def __unicode__(self):
        return self.id


class DetallePlanilla (models.Model):
    pesoPromedio = 0
    OpGrupo = (
        ('Grupo Carnes','Grupo Carnes'),
        ('Grupo Carnes 2','Grupo Carnes 2'),
        ('Grupo Carnes 3','Grupo Carnes 3'),
        ('Grupo Carnes 4','Grupo Carnes 4'),
        ('Grupo Costillas','Grupo Costillas'),
        ('Grupo Huesos' , 'Grupo Huesos'),
        ('Grupo SubProductos' , 'Grupo SubProductos'),
        ('Grupo Desechos' , 'Grupo Desechos')
    )

    planilla = models.ForeignKey(PlanillaDesposte)
    producto = models.ForeignKey(Producto)
    unidades = models.IntegerField(verbose_name='Unidades',default=0)
    PesoProducto = models.DecimalField(max_digits=9,decimal_places=3, verbose_name='Peso Producto')
    costoProducto = models.BigIntegerField(verbose_name = 'Costo Primario', default=0)
    costoAdtvo = models.BigIntegerField(verbose_name = 'Costo Admin', default=0)
    grupo = models.CharField(verbose_name='Grupo', choices=OpGrupo,default='Grupo Carnes', max_length=20)
    vrKiloCarnes = models.IntegerField(verbose_name='Vr.Carnes 1', default=0)
    vrKiloCarnes2 = models.IntegerField(verbose_name='Vr.Carnes 2', default=0)
    vrKiloCarnes3 = models.IntegerField(verbose_name='Vr.Carnes 3', default=0)
    vrKiloCarnes4 = models.IntegerField(verbose_name='Vr.Carnes 4', default=0)
    vrKiloCostilla = models.IntegerField(verbose_name='Vr.Costilla', default=0)
    vrKiloHuesos = models.IntegerField(verbose_name='Vr.Hueso', default=0)
    vrKiloSubProd = models.IntegerField(verbose_name='Vr.Sub Prod', default=0)
    vrKiloDesecho = models.IntegerField(verbose_name='Vr.Desecho', default=0)
    pesoCarne = models.DecimalField(verbose_name = 'Peso Carne',max_digits=15, decimal_places=3,default=0)
    pesoCostilla = models.DecimalField(verbose_name = 'Peso Costillas',max_digits=15, decimal_places=3,default=0)
    pesoHueso = models.DecimalField(verbose_name = 'Peso Hueso',max_digits=15, decimal_places=3,default=0)
    pesoSubProd = models.DecimalField(verbose_name = 'Peso Sub Porducto',max_digits=15, decimal_places=3,default=0)
    pesoDesecho = models.DecimalField(verbose_name = 'Peso Desecho',max_digits=15, decimal_places=3,default=0)


class Miga(models.Model):
    codigoMiga = models.AutoField(primary_key=True)
    cantidadFormulas = models.DecimalField(verbose_name='Formulas', max_digits=9, decimal_places=3,default=0)
    fechaFabricacion = models.DateField(verbose_name='Fecha De Fabricacion')
    PesoFormulaMiga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3)
    costoFormulaMiga = models.IntegerField(verbose_name='Costo Formula',default=0)
    costoKiloMigaProcesada = models.IntegerField(verbose_name='Costo Kilo',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)

    def __unicode__(self):
        return self.codigoMiga

class DetalleMiga(models.Model):

    miga= models.ForeignKey(Miga)
    PesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3)
    productoMiga = models.ForeignKey(Producto,verbose_name='Producto')
    costoProducto = models.IntegerField(verbose_name='Costo' , default=0)
    costoTotalProducto = models.IntegerField(verbose_name='Costo Total',default= 0 )


'''class Apanado(models.Model):
    codigoApanado = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto)
    huevos = models.IntegerField(verbose_name='Huevos',default=0)
    miga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3,default=0)
    pesoFilete = models.DecimalField(verbose_name='Peso Filete', max_digits=9, decimal_places=3,default=0)
    totalApanado= models.DecimalField(verbose_name='Total Apanado', max_digits=9, decimal_places=3,default=0)
    costoKiloApanado = models.IntegerField(verbose_name='Costo Kilo',default=0)

    def __unicode__(self):
        return self.codigoApanado'''

class Condimento(models.Model):
    codigoCondimento = models.AutoField(primary_key= True)
    fecha = models.DateField(verbose_name='Fecha')
    cantFormulas = models.IntegerField(verbose_name='Cantidad de formulas',default=0)
    pesoCondimento = models.DecimalField(verbose_name='Peso grs.',default=0, max_digits=9, decimal_places=3)
    costoCondimento = models.IntegerField(verbose_name='Costo Condimento',default=0)
    costoLitroCondimento = models.IntegerField(verbose_name='Costo litro',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)

    def __unicode__(self):
        return  self.codigoCondimento

class DetalleCondimento(models.Model):
    condimento = models.ForeignKey(Condimento)
    pesoProducto = models.DecimalField(verbose_name='Peso grs.', max_digits=9, decimal_places=3)
    productoCondimento = models.ForeignKey(Producto,verbose_name='Producto')
    costoProducto = models.IntegerField(verbose_name='Costo' , default=0)
    costoTotalProducto = models.IntegerField(verbose_name='Costo Total',default= 0 )

class Condimentado(models.Model):
    codigo = models.AutoField(primary_key= True)
    fecha = models.DateField(verbose_name='Fecha')
    producto = models.ForeignKey(Producto)
    pesoACondimentar = models.DecimalField(verbose_name='Filete a Cond.', max_digits=9, decimal_places=3,default=0)
    condimento = models.DecimalField(verbose_name='Condimento', max_digits=9, decimal_places=3,default=0)
    costoFilete = models.IntegerField(verbose_name='Costo Filete',default=0)
    costoCondimento = models.IntegerField(verbose_name='Costo Cond.',default=0)
    pesoFileteCond = models.DecimalField(verbose_name='Peso Condimentado', max_digits=9, decimal_places=3,default=0)
    costoFileteCond = models.IntegerField(verbose_name='Costo Condimentado',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)
    guardado = models.BooleanField(default=False)


class ValoresCostos(models.Model):
    jornadas = (
    ('AM', 'AM'),
    ('PM', 'PM'),
    )
    codigoCosto = models.AutoField(primary_key= True)
    nombreCosto = models.CharField(max_length=50,verbose_name='Nombre')
    valorCif = models.IntegerField(verbose_name='Valor Cif',default=0)
    valorMod = models.DecimalField(verbose_name='Incremento', max_digits=9, decimal_places=3,default=0)
    valorKiloPie = models.IntegerField(verbose_name='Valor Kilo en Pie',default=0)
    fecha = models.DateField(verbose_name='Fecha Actualizacion', auto_now=True)

    def __unicode__(self):
        return self.codigoCosto

class DescarneCabeza(models.Model):

    tipo = (
        ('Cerdas','Cerdas'),
        ('Cerdos','Cerdos')
    )

    fecha = models.DateField(verbose_name='Fecha')
    tipo = models.CharField(max_length=10,choices=tipo,verbose_name='Tipo')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    pesoCabezas = models.DecimalField(verbose_name='Peso Cab', max_digits=9, decimal_places=3,default=0)
    cantRecosrtes = models.IntegerField(verbose_name='Cant Rctes',default=0)
    recortes = models.DecimalField(verbose_name='Recortes', max_digits=9, decimal_places=3,default=0)
    caretas = models.DecimalField(verbose_name='Caretas', max_digits=9, decimal_places=3,default=0)
    lenguas = models.DecimalField(verbose_name='Lenguas', max_digits=9, decimal_places=3,default=0)
    procesos = models.DecimalField(verbose_name='Procesos', max_digits=9, decimal_places=3,default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)
    vrKiloRecorte = models.IntegerField(default=0)
    vrKiloLengua = models.IntegerField(default=0)
    vrKiloCareta = models.IntegerField(default=0)
    vrKiloProceso = models.IntegerField(default=0)
    guardado = models.BooleanField(default=False)

class ProcesoApanado(models.Model):
    fechaApanado = models.DateField(verbose_name='Fecha')
    pesoFilete = models.DecimalField(verbose_name='Peso Filete', max_digits=9, decimal_places=3,default=0)
    productoApanado = models.ForeignKey(Producto,verbose_name='Producto')
    huevos = models.IntegerField(verbose_name='Huevos',default=0)
    miga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3,default=0)
    totalApanado= models.DecimalField(verbose_name='Total Apanado', max_digits=9, decimal_places=3,default=0)
    costoKiloApanado = models.IntegerField(verbose_name='Costo Kilo',default=0)
    guardado = models.BooleanField(default=False)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)

    def __unicode__(self):
        cadena  = '%s | %s'%(self.fechaApanado,self.productoApanado.grupo.nombreGrupo)
        return cadena

class Molida(models.Model):
    fechaMolido = models.DateField(verbose_name='Fecha')
    pesoAmoler= models.DecimalField(verbose_name='Peso a Moler', max_digits=9, decimal_places=3,default=0)
    productoMolido = models.ForeignKey(Producto,verbose_name='Producto')
    costoKilo = models.IntegerField(verbose_name='Costo Kilo',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)
    totalMolido = models.DecimalField(verbose_name='Total Molido', max_digits=9, decimal_places=3,default=0)
    costoKiloMolido = models.IntegerField(verbose_name='Costo Kilo',default=0)
    guardado = models.BooleanField(default=False)

class EmpacadoApanados(models.Model):
    fechaEmpacado = models.DateField(verbose_name='Fecha')
    pesoChuelta = models.DecimalField(verbose_name='Peso a Empacar', max_digits=9, decimal_places=3,default=0)
    productoAEmpacar = models.ForeignKey(Producto,verbose_name='Producto')
    produccion = models.ForeignKey(ProcesoApanado,verbose_name='Produccion',blank= True, null=True)
    costoKiloChuleta = models.IntegerField(verbose_name='Costo Kilo',default=0)
    cantBandejas = models.IntegerField(verbose_name='Bandejas')
    stikers = models.IntegerField(verbose_name='Stikers')
    costobandeja = models.IntegerField(verbose_name='Costo Bandeja',default=0)
    pesoBandeja = models.DecimalField(verbose_name='Peso Bandeja', max_digits=9, decimal_places=3,default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    guardado = models.BooleanField(default=False)

class auxiliarPromedios(models.Model):
    nombreProducto = models.CharField(max_length=50)
    costo = models.IntegerField()


class Menudos(models.Model):
    fechaMenudo = models.DateField(verbose_name='Fecha')
    cantMenudos= models.DecimalField(verbose_name='Menudos', max_digits=9, decimal_places=3,default=0)
    costoMenudo = models.IntegerField(verbose_name='Costo Menudo',default=0)
    costoEscaldado = models.IntegerField(verbose_name='Costo Escaldado',default=0)
    pesoPicadillo = models.DecimalField(verbose_name='Peso Picadillo', max_digits=9, decimal_places=3,default=0)
    costoKiloPicadillo = models.IntegerField(verbose_name='Costo Kilo',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)
    guardado = models.BooleanField(default=False)


class TallerFrito(models.Model):
    fechaFrito = models.DateField(verbose_name='Fecha')
    pesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3,default=0)
    condimento = models.DecimalField(verbose_name='Peso Condimento', max_digits=9, decimal_places=3,default=0)
    punto = models.ForeignKey(Bodega)
    productoFrito = models.ForeignKey(Producto)
    pesoTotalFrito = models.DecimalField(verbose_name='Peso Total', max_digits=9, decimal_places=3,default=0)
    costoKiloFrito = models.IntegerField(verbose_name='Costo Kilo Frito',default=0)
    guardado = models.BooleanField(default=False)

class TallerCarneCondimentada(models.Model):
    fechaCarCond = models.DateField(verbose_name='Fecha')
    pesoProducto = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3,default=0)
    condimento = models.DecimalField(verbose_name='Peso Condimento', max_digits=9, decimal_places=3,default=0)
    puntoCond = models.ForeignKey(Bodega)
    productoCond = models.ForeignKey(Producto)
    pesoTotalCond = models.DecimalField(verbose_name='Peso Total', max_digits=9, decimal_places=3,default=0)
    costoKiloCond = models.IntegerField(verbose_name='Costo Kilo',default=0)
    guardado = models.BooleanField(default=False)

class TallerCroquetas(models.Model):
    fechaCroqueta = models.DateField(verbose_name='Fecha')
    croqueta = models.DecimalField(verbose_name='Peso Croqueta', max_digits=9, decimal_places=3,default=0)
    condimento = models.DecimalField(verbose_name='Peso Condimento', max_digits=9, decimal_places=3,default=0)
    pesoTotalCroqueta = models.DecimalField(verbose_name='Peso Total', max_digits=9, decimal_places=3,default=0)
    miga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3,default=0)
    puntoCroq = models.ForeignKey(Bodega)
    costoKiloCroqueta = models.IntegerField(verbose_name='Costo Kilo',default=0)
    guardado = models.BooleanField(default=False)


class TallerReapanado(models.Model):
    fechaReApanado = models.DateField(verbose_name='Fecha')
    pesoChuleta = models.DecimalField(verbose_name='Peso Chuleta', max_digits=9, decimal_places=3,default=0)
    pesoTotalReApanado = models.DecimalField(verbose_name='Peso ReApanado', max_digits=9, decimal_places=3,default=0)
    miga = models.DecimalField(verbose_name='Peso Miga', max_digits=9, decimal_places=3,default=0)
    chuelta = models.ForeignKey(Producto,verbose_name='Producto')
    puntoReApanado = models.ForeignKey(Bodega)
    guardado = models.BooleanField(default=False)

class Conversiones(models.Model):
    fechaConversion = models.DateField(verbose_name='Fecha')
    pesoConversion = models.DecimalField(verbose_name='Peso', max_digits=9, decimal_places=3,default=0)
    unidades = models.IntegerField(verbose_name='unidades',default=0)
    productoUno = models.CharField(verbose_name='Producto 1', max_length=50)
    productoDos = models.CharField(verbose_name='Producto 2', max_length=50)
    puntoConversion =  models.ForeignKey(Bodega)
    costoP1 = models.IntegerField(verbose_name='Costo Producto 1',default=0)
    costoP2 = models.IntegerField(verbose_name='Costo Producto 2',default=0)
    guardado = models.BooleanField(default=False)

class TallerBolaEnsalinada(models.Model):
    fechaBolaCondimentada = models.DateField(verbose_name='Fecha')
    pesoBola = models.DecimalField(verbose_name='Peso Producto', max_digits=9, decimal_places=3,default=0)
    sal = models.DecimalField(verbose_name='Peso Sal', max_digits=9, decimal_places=3,default=0)
    papaina = models.DecimalField(verbose_name='Peso Papaina', max_digits=9, decimal_places=3,default=0)
    pesoTotal = models.DecimalField(verbose_name='Peso Total', max_digits=9, decimal_places=3,default=0)
    costoKiloEns = models.IntegerField(verbose_name='Costo Kilo',default=0)
    pesoDespues = models.DecimalField(verbose_name='Peso Despues', max_digits=9, decimal_places=3,default=0)
    puntoBodega = models.ForeignKey(Bodega,verbose_name='Punto')
    guardado = models.BooleanField(default=False)

class TallerChicharron(models.Model):
    fechaChicharron = models.DateField(verbose_name='Fecha')
    productoCh = models.ForeignKey(Producto,verbose_name='Producto')
    Tocino = models.DecimalField(verbose_name='Peso Tocino', max_digits=9, decimal_places=3,default=0)
    Sal = models.DecimalField(verbose_name='Peso Sal', max_digits=9, decimal_places=3,default=0)
    undGrasa = models.IntegerField(verbose_name='und. Grasa',default=0)
    undChicharron = models.IntegerField(verbose_name='und. Chicharron',default=0)
    chicharron = models.DecimalField(verbose_name='Peso Chicharron', max_digits=9, decimal_places=3,default=0)
    grasa = models.DecimalField(verbose_name='Peso Grasa', max_digits=9, decimal_places=3,default=0)
    costoUndChicharron = models.IntegerField(verbose_name='Costo Kilo',default=0)
    costoUndGrasa = models.IntegerField(verbose_name='Costo Kilo',default=0)
    mod = models.IntegerField(verbose_name='Mod',default=0)
    cif = models.IntegerField(verbose_name='Cif',default=0)
    guardado = models.BooleanField(default=False)


