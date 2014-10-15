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
    class Meta:
        model = DetalleVenta

class ListaDePreciosForm(ModelForm):
    class Meta:
        model = ListaDePrecios

class DetalleListaForm(ModelForm):
    class Meta:
        model = DetalleLista