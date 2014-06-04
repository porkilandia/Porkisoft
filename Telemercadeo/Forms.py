from datetime import *

from django import forms
from django.forms import ModelForm
from django.db.models import F

from Telemercadeo.models import *


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente

