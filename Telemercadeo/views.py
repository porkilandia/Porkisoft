from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext

from Telemercadeo.Forms import *
from Ventas.models import *


def GestionCliente(request):

    pedidos = Pedido.objects.all()

    for pedido in pedidos:

        pedido.NombreCliente = pedido.cliente.nombreCliente
        pedido.save()

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

