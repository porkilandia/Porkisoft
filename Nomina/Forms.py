
from django.forms import ModelForm
from django.db.models import F
from django import forms
from Nomina.models import *


class UsuarioForm(forms.Form):
    empleados =Empleado.objects.all()
    empleado = forms.ModelChoiceField(queryset =empleados,required=True)
    usuario = forms.CharField(label='Nombre de Ususario')
    clave = forms.CharField(label='Contrasena',widget=forms.PasswordInput())


class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado

class CargoForm(ModelForm):
    class Meta:
        model = Cargo
