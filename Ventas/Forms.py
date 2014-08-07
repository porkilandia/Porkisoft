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
        exclude = ('TotalVenta',)

class VentaDetalleForm(ModelForm):
    class Meta:
        model = DetalleVenta