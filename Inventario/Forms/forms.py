from django.forms import ModelForm

from Inventario.models import *

class ProvedorForm(ModelForm):
    class Meta:
        model= Proveedor

class ProductoForm(ModelForm):
    class Meta:
        model = Producto

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
    class Meta:
        model = Compra

class DetalleCompraForm(ModelForm):
    class Meta:
        model = DetalleCompra