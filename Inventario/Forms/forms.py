from datetime import *

from django import forms
from django.forms import ModelForm

from Fabricacion.models import *
from Inventario.models import *
from  Nomina.models import *


class ProvedorForm(ModelForm):
    class Meta:
        model= Proveedor

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        exclude = ("costoProducto","vrVentaProducto","utilidadProducto","rentabilidadProducto")

class SubProductoForm(ModelForm):
    class Meta:
        model = SubProducto

class DetSubProductoForm(ModelForm):

    class Meta:
        model = DetalleSubProducto

class BodegaForm(ModelForm):
    class Meta:
        model = Bodega

class ProductoBodegaForm(ModelForm):
    class Meta:
        model = ProductoBodega

class GanadoForm(ModelForm):
    class Meta:
        model = Ganado

class CompraForm(ModelForm):
    tipo = forms.ModelChoiceField(queryset = Grupo.objects.all())
    class Meta:
        model = Compra
        exclude = ("vrCompra",)

class DetalleCompraForm(ModelForm):

    def __init__(self,idcompra,*args,**kwargs):
        super(DetalleCompraForm,self).__init__(*args,**kwargs)
        compra = Compra.objects.get(pk = idcompra)

        if compra.tipo.nombreGrupo == 'Insumos':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 5)
        elif compra.tipo.nombreGrupo == 'Verduras':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 6)
        elif compra.tipo.nombreGrupo == 'Compra / Venta':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 7)



    class Meta:
        model = DetalleCompra
        exclude = ("ganado",)

class DesposteForm(ModelForm):
    class Meta:
        model = PlanillaDesposte
        exclude = ("resesADespostar","totalDespostado","difCanalADespostado","totalCanal",)

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


class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado

class CargoForm(ModelForm):
    class Meta:
        model = Cargo

class TrasladoForm(ModelForm):
    bodegaDestino = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=True)
    class Meta:
        model = Traslado

class DetalleTrasladoForm(ModelForm):
    class Meta:
        model = DetalleTraslado

class SacrificioForm(ModelForm):
    class Meta:
        model = Sacrificio
        exclude = ("compra","cantReses","piel","vrMenudo","vrDeguello","vrTransporte")

class PlanillaRecepcionForm(ModelForm):
    class Meta:
        model = PlanillaRecepcion
        exclude = ("difPieCanal","cantCabezas",)

class EnsalinadoForm(ModelForm):
    class Meta:
        model = Ensalinado
        exclude = ("costoKilo" ,  "costoTotal",)

class LimpiezaVerdurasForm(ModelForm):
    class Meta:
        model = LimpiezaVerduras

class CondimentoForm(ModelForm):
    class Meta:
        model = Condimento
        exclude = ('costoCondimento','costoLitroCondimento',)

class DetalleCondimentoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DetalleCondimentoForm,self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(grupo__range = (5,6))

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