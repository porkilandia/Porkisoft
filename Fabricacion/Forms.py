from datetime import *

from django import forms
from django.forms import ModelForm

from Fabricacion.models import *
from Inventario.models import *

class SacrificioForm(ModelForm):
    class Meta:
        model = Sacrificio
        exclude = ("compra","cantReses","piel","vrMenudo","vrDeguello",)

class EnsalinadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnsalinadoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(nombreProducto__contains = 'Filete de Cerda')
        q2 = Producto.objects.filter(nombreProducto__contains = 'Pierna de Cerda')
        q3 = Producto.objects.filter(nombreProducto__contains = 'Bola')
        self.fields['productoEnsalinado'].queryset = q1 |q2 | q3
    class Meta:
        model = Ensalinado
        exclude = ("costoKilo" , "costoTotal","guardado","estado",)

class LimpiezaVerdurasForm(ModelForm):
     def __init__(self, *args, **kwargs):
        super(LimpiezaVerdurasForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo = 'Verduras')
        q2 = Compra.objects.filter(tipo__nombreGrupo = 'Verduras').order_by('-fechaCompra')
        self.fields['productoLimpiar'].queryset = q1
        self.fields['compra'].queryset = q2

     class Meta:
        model = LimpiezaVerduras
        exclude = ('vrKilo',)

class CondimentoForm(ModelForm):
    class Meta:
        model = Condimento
        exclude = ('costoCondimento','costoLitroCondimento',)

class DetalleCondimentoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DetalleCondimentoForm,self).__init__(*args, **kwargs)
        self.fields['productoCondimento'].queryset = Producto.objects.filter(grupo__range = (6,7))

    class Meta:
        model = DetalleCondimento
        exclude = ('costoProducto','costoTotalProducto',)

class TajadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TajadoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo ='Cerdos')
        q2 = Producto.objects.filter(grupo__nombreGrupo ='Cerdas')
        q3 = Producto.objects.filter(grupo__nombreGrupo ='Pollos')

        fechainicio = date.today() - timedelta(days=20)
        fechafin = date.today()

        planilla = PlanillaDesposte.objects.all().order_by('-fechaDesposte')
        compra = Compra.objects.filter(tipo__nombreGrupo = 'Pollos').order_by('-fechaCompra')

        self.fields['producto'].queryset = q1 | q2 | q3
        self.fields['desposteHistorico'].queryset = planilla.filter(fechaDesposte__range = (fechainicio,fechafin))
        self.fields['polloHistorico'].queryset = compra.filter(fechaCompra__range = (fechainicio,fechafin))

    class Meta:
        model = Tajado
        exclude = ("totalTajado",)

class DetalleTajadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetalleTajadoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo ='Cerdos')
        q2 = Producto.objects.filter(grupo__nombreGrupo ='Cerdas')
        q3 = Producto.objects.filter(grupo__nombreGrupo ='Pollos')
        self.fields['producto'].queryset = q1 | q2 | q3
    class Meta:
        model = DetalleTajado
        exclude = ("costoKilo",)

class MigaForm(ModelForm):
    class Meta:
        model = Miga
        exclude = ("costoFormulaMiga","costoKiloMigaProcesada",)

class DetalleMigaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetalleMigaForm,self).__init__(*args, **kwargs)
        self.fields['productoMiga'].queryset = Producto.objects.filter(grupo = 6)
    class Meta:
        model = DetalleMiga
        exclude = ("costoProducto","costoTotalProducto",)

class ApanadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApanadoForm,self).__init__(*args, **kwargs)
        self.fields['productoApanado'].queryset = Producto.objects.filter(nombreProducto__contains = 'Condimentado').filter(nombreProducto__contains = 'Filete')
    class Meta:
        model = ProcesoApanado
        exclude = ("guardado","costoKiloApanado",)

class CondimentadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondimentadoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo ='Cerdos').filter(nombreProducto__contains = 'Filete de')
        q2 = Producto.objects.filter(grupo__nombreGrupo ='Cerdas').filter(nombreProducto__contains = 'Filete de')
        q3 = Producto.objects.filter(grupo__nombreGrupo ='Pollos').filter(nombreProducto__contains = 'Filete de')
        q4 = Producto.objects.filter(grupo__nombreGrupo ='Cerdas').filter(nombreProducto__contains = 'Ensalinada')
        q5 = Producto.objects.filter(grupo__nombreGrupo ='Cerdas').filter(nombreProducto__contains = 'Lomo')
        self.fields['producto'].queryset = q1 | q2 | q3 | q4 |q5
    class Meta:
        model = Condimentado

class DesposteForm(ModelForm):
    class Meta:
        model = PlanillaDesposte
        exclude = ("resesADespostar","totalDespostado","difCanalADespostado","totalCanal","guardado",)

class CanalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CanalForm,self).__init__(*args, **kwargs)

        if (PlanillaDesposte.objects.all()):
            #self.fields['planilla'].queryset = PlanillaDesposte.objects.all()
            self.fields['planilla'].queryset = PlanillaDesposte.objects.filter(tipoDesposte = '')

    class Meta:
        model=Canal
        exclude = ("vrKiloCanal","vrArrobaCanal")

class DetalleDesposteForm(ModelForm):
    def __init__(self,idplanilla, *args, **kwargs):
        super(DetalleDesposteForm,self).__init__(*args, **kwargs)

        if (PlanillaDesposte.objects.get(pk = int(idplanilla)).tipoDesposte != '' ):
            q1 = Producto.objects.filter(grupo__nombreGrupo = PlanillaDesposte.objects.get(pk = int(idplanilla)).tipoDesposte)
            q2 = Producto.objects.filter(grupo__nombreGrupo ='Desechos')
            #q = Producto.objects.all()
            self.fields['producto'].queryset = q1|q2

        else:
            self.fields['producto'].queryset = Producto.objects.all()
    class Meta:
        model = DetallePlanilla
        exclude = ("vrKiloCostilla","costoProducto","costoAdtvo","vrKiloCarnes","vrKiloCarnes3","vrKiloCarnes4",
                   "vrKiloHuesos","vrKiloSubProd","pesoCostilla","vrKiloDesecho","pesoCarne","pesoHueso","pesoSubProd","pesoDesecho","vrKiloCarnes2",)

class costoForm(ModelForm):
    class Meta:
        model = ValoresCostos
        exclude = ("valorCif","valorMod",)

class DescarneForm(ModelForm):
    class Meta:
        model = DescarneCabeza
        exclude = ("guardado","vrKiloRecorte","vrKiloLengua","vrKiloCareta","vrKiloProceso",)

class MolidoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MolidoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo ='Cerdos').filter(nombreProducto = 'Pierna de Cerdo')
        q2 = Producto.objects.filter(grupo__nombreGrupo ='Reses').filter(nombreProducto = 'Procesos de Res')
        q3 = Producto.objects.filter(grupo__nombreGrupo ='Reses').filter(nombreProducto = 'Lagartos')
        q4 = Producto.objects.filter(grupo__nombreGrupo ='Reses').filter(nombreProducto = 'Cogotes')
        q5 = Producto.objects.filter(grupo__nombreGrupo ='Reses').filter(nombreProducto = 'Bola')

        self.fields['productoMolido'].queryset = q1 | q2 | q3 | q4 | q5
    class Meta:
        model = Molida
        exclude = ("costoKiloMolido","guardado","costoKilo",)

class EmpacadoApanadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmpacadoApanadoForm,self).__init__(*args, **kwargs)

        fechainicio = date.today() - timedelta(days=20)
        fechafin = date.today()

        self.fields['produccion'].queryset = ProcesoApanado.objects.all().filter(fechaApanado__range = (fechainicio,fechafin)).order_by('-fechaApanado')
        self.fields['productoAEmpacar'].queryset = Producto.objects.filter(nombreProducto__contains = 'Filete Apanado')
    class Meta:
        model = EmpacadoApanados
        exclude = ("costobandeja","pesoBandeja",)

class MenudoForm(ModelForm):
    class Meta:
        model = Menudos
        exclude = ("costoKiloPicadillo","guardado",)

class FritoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FritoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdos')
        q2 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdas')
        self.fields['productoFrito'].queryset = q1 | q2

    class Meta:
        model = TallerFrito
        exclude = ("pesoTotalFrito","costoKiloFrito",)
class CarneCondForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarneCondForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo = 'Reses')
        q2 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdos')
        self.fields['productoCond'].queryset = q1 | q2

    class Meta:
        model = TallerCarneCondimentada
        exclude = ("pesoTotalCond","costoKiloCond","guardado",)

class CroquetaFrom(ModelForm):
    class Meta:
        model = TallerCroquetas
        exclude = ("pesoTotalCond","costoKiloCond","guardado","pesoTotalCroqueta","costoKiloCroqueta",)

class ReapanadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReapanadoForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(nombreProducto__contains = 'Filete Apanado')
        q2 = Producto.objects.filter(nombreProducto__contains = 'Condimentado')
        q3 = Producto.objects.filter(nombreProducto__contains = 'Condimentada')
        self.fields['chuelta'].queryset = q1 | q2 | q3
    class Meta:
        model = TallerReapanado
        exclude = ("pesoTotalReApanado","guardado",)

class ConversionesForm(ModelForm):

    productoUno = forms.ModelChoiceField(queryset = Producto.objects.none(),required=True)
    productoDos = forms.ModelChoiceField(queryset = Producto.objects.none(),required=True)

    def __init__(self, *args, **kwargs):
        super(ConversionesForm,self).__init__(*args, **kwargs)

        q1 = Producto.objects.filter(grupo__nombreGrupo = 'Reses')
        q2 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdos')
        q3 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdas')
        q4 = Producto.objects.filter(grupo__nombreGrupo = 'Compra/Venta')
        q5 = Producto.objects.filter(grupo__nombreGrupo = 'Desechos')
        q6 = Producto.objects.filter(grupo__nombreGrupo = 'Pollos')
        q7 = Producto.objects.filter(grupo__nombreGrupo = 'Insumos')

        self.fields['productoUno'].queryset = q1 | q2 | q3 | q4 | q5 | q6 | q7
        self.fields['productoDos'].queryset = q1 | q2 | q3 | q4 | q5 | q6 | q7


    class Meta:
        model = Conversiones
        exclude = ("costoP1","costoP2","guardado",)

class EnsBolaForm(ModelForm):
    class Meta:
        model = TallerBolaEnsalinada
        exclude = ("pesoTotal","costoKiloEns","guardado",)

class ChicharronForm(ModelForm):
    class Meta:
        model = TallerChicharron
        exclude = ("costoUndChicharron","costoUndGrasa","guardado",)