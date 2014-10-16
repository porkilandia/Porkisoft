from datetime import *

from django import forms
from django.forms import ModelForm
from django.db.models import F

from Ventas.models import *

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ('TotalVenta','descuento',)

class DetallePedidoForm(ModelForm):
    class Meta:
        model = DetallePedido
        exclude = ('subproducto',)

class VentaForm(ModelForm):
    class Meta:
        model = Venta
        exclude = ('TotalVenta',"TotalCredito","TotalContado","descuadre","residuo","guardado",)

class VentaDetalleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VentaDetalleForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo = 'Reses')
        q2 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdos')
        q3 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdas')
        q4 = Producto.objects.filter(grupo__nombreGrupo = 'Compra/Venta')
        q5 = Producto.objects.filter(grupo__nombreGrupo = 'Pollos')

        self.fields['productoVenta'].queryset = q1 | q2 | q3 | q4 | q5

    class Meta:
        model = DetalleVenta

class ListaDePreciosForm(ModelForm):
    class Meta:
        model = ListaDePrecios

class DetalleListaForm(ModelForm):
    class Meta:
        model = DetalleLista