from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext

from Telemercadeo.Forms import *
from Ventas.models import *


def GestionCliente(request):

    clientes = Cliente.objects.all()
    usuario = request.user
    if usuario.is_staff:
        plantilla = 'base.html'

    else:
        plantilla = 'PuntoVentaNorte.html'
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/telemercadeo/cliente')
    else:
        formulario = ClienteForm()
    return render_to_response('Telemercadeo/GestionCliente.html',{'plantilla':plantilla,'formulario':formulario,'clientes':clientes},
                              context_instance = RequestContext(request) )

def EditaCliente(request,idCliente):
    cliente = Cliente.objects.select_related().get(pk = idCliente)
    clientes = Cliente.objects.all()
    usuario = request.user
    if usuario.is_staff:
        plantilla = 'base.html'
    else:
        plantilla = 'PuntoVentaNorte.html'

    if request.method == 'POST':
        formulario = ClienteForm(request.POST,instance=cliente)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/telemercadeo/cliente')
    else:
        formulario = ClienteForm(instance=cliente)
    return render_to_response('Telemercadeo/GestionCliente.html',{'plantilla':plantilla,'formulario':formulario,'clientes':clientes},
                              context_instance = RequestContext(request) )



