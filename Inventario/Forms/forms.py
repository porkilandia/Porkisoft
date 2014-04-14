from django.forms import ModelForm

from Inventario.models import *


class ProductoForm(ModelForm):
    class Meta:
        model = Producto

class SubProductoForm(ModelForm):
    class Meta:
        model = SubProducto

class DetSubProductoForm(ModelForm):

    class Meta:
        model = DetalleSubProducto


