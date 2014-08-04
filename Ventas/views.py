# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from Ventas.Forms import *
#Imports necesarios para el uso de Pisa PDF
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.http import HttpResponse

def GestionVentas(request):
    return render_to_response('Ventas/GestionVentas.html',{},context_instance = RequestContext(request))

def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def ReportePedido(request,idpedido):
   # vista de ejemplo con un hipotético modelo Libro
    detallePedido = DetallePedido.objects.filter(pedido = idpedido)
    pedido = Pedido.objects.get(pk = idpedido)

    html = render_to_string('Ventas/Pedido_pdf.html', {'pagesize':'A4', 'detallePedido':detallePedido,'pedido':pedido},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


def GestionPedidos(request,idcliente):
    pedidos = Pedido.objects.filter(cliente = idcliente)
    cliente = Cliente.objects.get(pk = idcliente)
    if request.method =='POST':
        formulario = PedidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/pedido/'+idcliente)
    else:
        formulario = PedidoForm(initial={'cliente':cliente})

    return render_to_response('Ventas/GestionPedido.html',{'formulario':formulario,'pedidos':pedidos,'cliente':cliente},
                              context_instance = RequestContext(request))

def GestionDetallePedido(request,idpedido):
    pedido = Pedido.objects.get(pk = idpedido)
    detPedido = DetallePedido.objects.filter(pedido = idpedido)
    vrPedido = 0

    for det in detPedido:
        vrPedido += det.vrTotal

    if request.method =='POST':
        formulario = DetallePedidoForm(request.POST)
        if formulario.is_valid():
            detalle = formulario.save()

            pedido.TotalVenta = vrPedido + detalle.vrTotal
            pedido.save()

            return HttpResponseRedirect('/ventas/detallePedido/'+idpedido)
    else:
        formulario = DetallePedidoForm(initial={'pedido':idpedido})

    return render_to_response('Ventas/GestionDetallePedido.html',{'idPedido':idpedido,'formulario':formulario,'pedido':pedido,
                                                                  'detPedido':detPedido,'vrPedido':vrPedido},
                              context_instance = RequestContext(request))

