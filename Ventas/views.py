# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from Ventas.Forms import *
#Imports necesarios para el uso de Pisa PDF
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from datetime import *
from decimal import Decimal

import json
from django.template.loader import render_to_string
from django.http import HttpResponse


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

def GestionVentas(request):

    ventas = Venta.objects.all()

    if request.method =='POST':
        formulario = VentaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/ventas/')
    else:
        formulario = VentaForm()

    return render_to_response('Ventas/GestionVentas.html',{'formulario':formulario,'ventas':ventas},
                              context_instance = RequestContext(request))

def GestionDetalleVentas(request,idVenta):

    venta = Venta.objects.get(pk = idVenta)
    detalles = DetalleVenta.objects.filter(venta = idVenta)


    if request.method =='POST':
        formulario = VentaDetalleForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            #sumamos los valores de la venta
            vrTotalContado = 0
            vrTotalCredito = 0
            vrTotal = 0
            detalles = DetalleVenta.objects.filter(venta = idVenta)
            for det in detalles:
                if det.contado == True:
                    vrTotalContado += det.vrTotal
                elif det.credito == True:
                    vrTotalCredito += det.vrTotal
                vrTotal += det.vrTotal

            venta.residuo = venta.efectivo - venta.TotalRegistradora
            venta.descuadre = venta.TotalRegistradora - vrTotal
            venta.TotalVenta = vrTotal
            venta.TotalCredito = vrTotalCredito
            venta.TotalContado = vrTotalContado
            venta.save()

            return HttpResponseRedirect('/ventas/detalleVentas/'+idVenta)
    else:
        formulario = VentaDetalleForm(initial={'venta':idVenta})

    return render_to_response('Ventas/GestionDetalleVentas.html',{'formulario':formulario,'venta':venta,'detalles':detalles},
                              context_instance = RequestContext(request))

def EditaDetalleVentas(request,idDetVenta):
    detalle =  DetalleVenta.objects.get(pk = idDetVenta)
    detalles = DetalleVenta.objects.filter(venta = detalle.venta.numeroVenta )
    venta = Venta.objects.get(pk = detalle.venta.numeroVenta)


    if request.method =='POST':
        formulario = VentaDetalleForm(request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            #sumamos los valores de la venta
            vrTotalContado = 0
            vrTotalCredito = 0
            vrTotal = 0

            detalles = DetalleVenta.objects.filter(venta = detalle.venta.numeroVenta )
            for det in detalles:
                if det.contado == True:
                    vrTotalContado += det.vrTotal
                elif det.credito == True:
                    vrTotalCredito += det.vrTotal
                vrTotal += det.vrTotal

            venta.residuo = venta.efectivo - venta.TotalRegistradora
            venta.descuadre = venta.TotalRegistradora - vrTotal
            venta.TotalVenta = vrTotal
            venta.TotalCredito = vrTotalCredito
            venta.TotalContado = vrTotalContado
            venta.save()

            return HttpResponseRedirect('/ventas/detalleVentas/'+ str(venta.numeroVenta))
    else:
        formulario = VentaDetalleForm(initial={'venta':venta.numeroVenta},instance=detalle)

    return render_to_response('Ventas/GestionDetalleVentas.html',{'formulario':formulario,'venta':venta,'detalles':detalles},
                              context_instance = RequestContext(request))


def consultaValorProducto(request):
    idProducto = request.GET.get('idProducto')
    idVenta = request.GET.get('idVenta')
    peso = request.GET.get('peso')
    lista = request.GET.get('lista')
    unidades = request.GET.get('unidades')
    venta = Venta.objects.get(pk = int(idVenta))
    producto = Producto.objects.get(pk = int(idProducto))
    precio = 0
    listaPrecios = DetalleLista.objects.filter(lista = int(lista))

    for detalles in listaPrecios:
        if producto.codigoProducto == detalles.productoLista.codigoProducto:
            precio = detalles.precioVenta


    #verificamos si el producto cuenta con esa cantidad en bodega
    bodega = ProductoBodega.objects.get(bodega = venta.bodega.codigoBodega,producto =producto.codigoProducto )

    if int(peso) <= bodega.pesoProductoStock and int(unidades) == 0 :
        exito = precio
    elif int(unidades) <= bodega.unidadesStock and int(peso) == 0 :
        exito = precio
    else:
        exito = 'No hay existencias en almacen'

    respuesta = json.dumps(exito)
    return HttpResponse(respuesta,mimetype='application/json')

def GuardarVenta(request):

    #Tomo los datos necesarios del request como son el id de la venta para obtener los registros que quiero guardar
    idVenta = request.GET.get('idVenta')
    peso = request.GET.get('peso')
    venta = Venta.objects.get(pk = int(idVenta))
    ventas = DetalleVenta.objects.filter(venta = int(idVenta))
    registros = ventas.count()

    #voy por todos los productos de esa venta para guardar restar cantidades uno a uno

    for vnt in ventas :
        bodega = ProductoBodega.objects.get(bodega = venta.bodega.codigoBodega,producto = vnt.productoVenta.codigoProducto)
        bodega.pesoProductoStock -= vnt.peso
        bodega.unidadesStock -= vnt.unidades
        bodega.save()

        movimiento = Movimientos()
        movimiento.tipo = 'VNT%d'%(venta.numeroVenta)
        movimiento.fechaMov = venta.fechaVenta
        movimiento.productoMov = vnt.productoVenta
        if vnt.peso == 0:
            movimiento.salida = vnt.unidades
        else:
            movimiento.salida = vnt.peso
        movimiento.save()

    msj = 'Se guardaron %d registros exitosamente'%registros
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionLista(request):
    listas = ListaDePrecios.objects.all()

    if request.method =='POST':
        formulario = ListaDePreciosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/listaPrecios/')
    else:
        formulario = ListaDePreciosForm()

    return render_to_response('Ventas/GestionLista.html',{'formulario':formulario,'listas':listas},
                              context_instance = RequestContext(request))

def GestionDetalleLista(request,idLista):
    lista = ListaDePrecios.objects.get(pk= idLista)
    detalleListas = DetalleLista.objects.filter(lista = lista.codigoLista)

    if request.method =='POST':
        formulario = DetalleListaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/detalleLista/'+idLista)
    else:
        formulario = DetalleListaForm(initial={'lista':idLista})

    return render_to_response('Ventas/GestionDetalleListas.html',{'formulario':formulario,'lista':lista,'detalleListas':detalleListas},
                              context_instance = RequestContext(request))

def consultaCostoProducto(request):
    idProducto = request.GET.get('producto')
    producto = Producto.objects.get(pk = int(idProducto)).costoProducto
    respuesta = json.dumps(producto)
    return HttpResponse(respuesta,mimetype='application/json')


def EditaListas(request,idDetLista):

    detalleLista = DetalleLista.objects.get(pk = idDetLista)
    lista = ListaDePrecios.objects.get(pk= detalleLista.lista.codigoLista)
    detalleListas = DetalleLista.objects.filter(lista = lista.codigoLista)

    if request.method =='POST':
        formulario = DetalleListaForm(request.POST,instance=detalleLista)
        if formulario.is_valid():
            formulario.save()
            lista.fecha = datetime.today()
            lista.save()
            return HttpResponseRedirect('/ventas/detalleLista/'+str(lista.codigoLista))
    else:
        formulario = DetalleListaForm(initial={'lista':lista.codigoLista},instance=detalleLista)

    return render_to_response('Ventas/GestionDetalleListas.html',{'formulario':formulario,'lista':lista,'detalleListas':detalleListas},
                              context_instance = RequestContext(request))

