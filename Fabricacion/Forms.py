from datetime import *

from django import forms
from django.forms import ModelForm

from Fabricacion.models import *
from Inventario.models import *

class SacrificioForm(ModelForm):
    class Meta:
        model = Sacrificio
        exclude = ("compra","cantReses","piel","vrMenudo","vrDeguello","vrTransporte")

class EnsalinadoForm(ModelForm):
    class Meta:
        model = Ensalinado
        exclude = ("costoKilo" ,  "costoTotal",)

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
        self.fields['producto'].queryset = Producto.objects.filter(grupo__range = (6,7))

    class Meta:
        model = DetalleCondimento
        exclude = ('costoProducto','costoTotalProducto',)

class CondTajadoForm(ModelForm):
    class Meta:
        model = CondimentadoTajado

class MigaForm(ModelForm):
    class Meta:
        model = Miga
class DetalleMigaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetalleMigaForm,self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(grupo = 5)
    class Meta:
        model = DetalleMiga

class ApanadoForm(ModelForm):
    class Meta:
        model = Apanado

class CondTajPechugasForm(ModelForm):
    fechainicio = date.today() - timedelta(days=3)
    fechafin = date.today()
    compra = forms.ModelChoiceField(queryset=Compra.objects.filter(fechaCompra__range =(fechainicio,fechafin)).filter(tipo = 10)) # muestra los registros de compras de 3 dias de antiguedad
    class Meta:
        model = CondimentadoTajadoPechuga

class DesposteForm(ModelForm):
    class Meta:
        model = PlanillaDesposte
        exclude = ("resesADespostar","totalDespostado","difCanalADespostado","totalCanal",)

class CanalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CanalForm,self).__init__(*args, **kwargs)

        if (PlanillaDesposte.objects.all()):
            #self.fields['planilla'].queryset = PlanillaDesposte.objects.all()
            self.fields['planilla'].queryset = PlanillaDesposte.objects.filter(fechaDesposte = datetime.today())

    class Meta:
        model=Canal
        exclude = ("vrKiloCanal","vrArrobaCanal")

class DetalleDesposteForm(ModelForm):
    class Meta:
        model = DetallePlanilla