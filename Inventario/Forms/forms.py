from datetime import *

from django import forms
from django.forms import ModelForm
from django.db.models import F

from Fabricacion.models import *
from Inventario.models import *
from  Nomina.models import *


class ProvedorForm(ModelForm):
    class Meta:
        model= Proveedor

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        exclude = ("costoProducto","precioSugerido","utilidadProducto","rentabilidadProducto")

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
        exclude = ('TotalpesoEnPie',)

class CompraForm(ModelForm):
    tipo = forms.ModelChoiceField(queryset = Grupo.objects.all())

    def __init__(self,tipoCompra,*args,**kwargs):
        super(CompraForm,self).__init__(*args,**kwargs)
        print tipoCompra
        if tipoCompra == '1':
            self.fields['bodegaCompra'].queryset = Bodega.objects.filter(pk = 5)
        elif tipoCompra == '2' :
            q1 = Bodega.objects.filter(pk = 1)
            q2 = Bodega.objects.filter(pk = 2)
            q3 = Bodega.objects.filter(pk = 3)
            q4 = Bodega.objects.filter(pk = 4)
            q5 = Bodega.objects.filter(pk = 6)

            self.fields['bodegaCompra'].queryset = q1|q2|q3|q4|q5


    class Meta:
        model = Compra
        exclude = ("vrCompra","cantCabezas","vrTransporte","guardado",)

class DetalleCompraForm(ModelForm):

    def __init__(self,idcompra,*args,**kwargs):
        super(DetalleCompraForm,self).__init__(*args,**kwargs)
        compra = Compra.objects.get(pk = idcompra)

        if compra.tipo.nombreGrupo == 'Insumos':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 6)
        elif compra.tipo.nombreGrupo == 'Reses':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 1)
        elif compra.tipo.nombreGrupo == 'Cerdos':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 2)
        elif compra.tipo.nombreGrupo == 'Cerdas':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 3)
        elif compra.tipo.nombreGrupo == 'Verduras':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 7)
        elif compra.tipo.nombreGrupo == 'Compra/Venta':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 9)
        elif compra.tipo.nombreGrupo == 'Basicos Procesados':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 8)
        elif compra.tipo.nombreGrupo == 'Pollos':
            self.fields['producto'].queryset = Producto.objects.filter(grupo = 11)

    class Meta:
        model = DetalleCompra
        exclude = ("ganado",)


class TrasladoForm(ModelForm):
    bodegaDestino = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=True)
    class Meta:
        model = Traslado

class DetalleTrasladoForm(ModelForm):
    class Meta:
        model = DetalleTraslado
        exclude = ("SubProducto","pesoLlegada",)


class PlanillaRecepcionForm(ModelForm):
    class Meta:
        model = PlanillaRecepcion
        exclude = ("difPieCanal","pesoCanales","vrKiloCanal",)



class GrupoForm(ModelForm):
    class Meta:
        model = Grupo

class AjustesForm(ModelForm):
    class Meta:
        model = Ajustes
        exclude = ("guardado",)

class FaltanteForm(ModelForm):
    class Meta:
        model = Faltantes
        exclude = ("guardado",)
class DetalleFaltanteForm(ModelForm):
    class Meta:
        model = DetalleFaltantes

