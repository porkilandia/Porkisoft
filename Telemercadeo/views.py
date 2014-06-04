from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext

from Telemercadeo.models import Cliente
from Telemercadeo.Forms import *


def GestionCliente(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/cliente')
    else:
        formulario = ClienteForm()
    return render_to_response('Telemercadeo/GestionCliente.html',{'formulario':formulario,'clientes':clientes},
                              context_instance = RequestContext(request) )

