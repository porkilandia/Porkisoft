
from django.forms import ModelForm
from django.db.models import F

from  Nomina.models import *


class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado

class CargoForm(ModelForm):
    class Meta:
        model = Cargo