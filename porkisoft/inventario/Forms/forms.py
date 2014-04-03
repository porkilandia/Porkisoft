from django.forms import ModelForm

from inventario.models import *


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
