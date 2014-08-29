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
        self.fields['productoEnsalinado'].queryset = Producto.objects.filter(grupo = 3)
    class Meta:
        model = Ensalinado
        exclude = ("costoKilo" , "costoTotal","guardado","estado","mod",)

class LimpiezaVerdurasForm(ModelForm):
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
        self.fields['polloHistorico'].queryset = Compra.objects.filter(tipo__nombreGrupo = 'Pollos')

    class Meta:
        model = Tajado
        exclude = ("totalTajado","cif","mod",)

class DetalleTajadoForm(ModelForm):
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
    class Meta:
        model = ProcesoApanado
        exclude = ("guardado","costoKiloApanado","mod","cif",)

class CondimentadoForm(ModelForm):
    class Meta:
        model = Condimentado

class DesposteForm(ModelForm):
    class Meta:
        model = PlanillaDesposte
        exclude = ("resesADespostar","totalDespostado","difCanalADespostado","totalCanal","cif","mod","tipoDesposte",)

class CanalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CanalForm,self).__init__(*args, **kwargs)

        if (PlanillaDesposte.objects.all()):
            self.fields['planilla'].queryset = PlanillaDesposte.objects.all()
            #self.fields['planilla'].queryset = PlanillaDesposte.objects.filter(fechaDesposte = datetime.today())

    class Meta:
        model=Canal
        exclude = ("vrKiloCanal","vrArrobaCanal")

class DetalleDesposteForm(ModelForm):
    class Meta:
        model = DetallePlanilla
        exclude = ("vrKiloCostilla","costoProducto","costoAdtvo","vrKiloCarnes","vrKiloCarnes3","vrKiloCarnes4",
                   "vrKiloHuesos","vrKiloSubProd","pesoCostilla","vrKiloDesecho","pesoCarne","pesoHueso","pesoSubProd","pesoDesecho","vrKiloCarnes2",)

class costoForm(ModelForm):
    class Meta:
        model = ValoresCostos

class DescarneForm(ModelForm):
    class Meta:
        model = DescarneCabeza
        exclude = ("mod","cif","vrKiloRecorte","vrKiloLengua","vrKiloCareta","vrKiloProceso",)

class MolidoForm(ModelForm):
    class Meta:
        model = Molida
        exclude = ("mod","cif","costoKiloMolido","guardado","costoKilo",)