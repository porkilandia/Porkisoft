# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from Ventas.Forms import *
from Fabricacion.models import *
from math import ceil
from datetime import *
from decimal import Decimal
from django.core import serializers
from django.db.models import Avg
import json
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def TemplateTipoPedido(request):

    clientes = Cliente.objects.all()
    bodegas = Bodega.objects.all()
    return render_to_response('Ventas/TemplateRepoPedidos.html',{'clientes':clientes,'bodegas':bodegas},
                              context_instance = RequestContext(request))

def ReporteTipoPedido(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    idCliente = request.GET.get('cliente')
    filtrpedido = request.GET.get('filtrpedido')
    bodega = request.GET.get('bodega')

    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()
    pedidos = ''

    if filtrpedido == 'fecha':
        pedidos = Pedido.objects.filter(fechaPedido__range = (finicio,ffin)).filter(bodega = int(bodega)).order_by('numeroFactura')
    elif filtrpedido == 'total':
        pedidos = Pedido.objects.filter(fechaPedido__range = (finicio,ffin)).filter(cliente = int(idCliente)).filter(bodega = int(bodega)).order_by('numeroFactura')

    respuesta = serializers.serialize('json',pedidos)
    return HttpResponse(respuesta,mimetype='application/json')


def GestionPedidos(request,idcliente):
    fechainicio = date.today() - timedelta(days=8)
    fechafin = date.today()
    usuario = request.user.username
    emp = Empleado.objects.get(usuario = usuario)
    pedidos = Pedido.objects.filter(cliente = idcliente).filter(fechaPedido__range =(fechainicio,fechafin)).filter(bodega = emp.punto.codigoBodega)
    #pedidos = Pedido.objects.filter(cliente = idcliente)
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

def BorrarPedidos(request,idpedido):
    pedido = Pedido.objects.get(pk = idpedido)
    pedido.delete()
    return HttpResponseRedirect('/ventas/pedido/'+str(pedido.cliente.codigoCliente))

def GestionDetallePedido(request,idpedido):
    pedido = Pedido.objects.get(pk = idpedido)
    detPedido = DetallePedido.objects.filter(pedido = idpedido)
    vrPedido = 0

    for det in detPedido:
        vrPedido += det.vrTotalPedido
    pedido.TotalVenta = vrPedido
    pedido.save()

    if request.method =='POST':
        formulario = DetallePedidoForm(request.POST)
        if formulario.is_valid():
            detalle = formulario.save()

            pedido.TotalVenta = vrPedido + detalle.vrTotalPedido
            pedido.save()

            return HttpResponseRedirect('/ventas/detallePedido/'+idpedido)
    else:
        formulario = DetallePedidoForm(initial={'pedido':idpedido})

    return render_to_response('Ventas/GestionDetallePedido.html',{'idPedido':idpedido,'formulario':formulario,'pedido':pedido,
                                                                  'detPedido':detPedido,'vrPedido':vrPedido},
                              context_instance = RequestContext(request))

def BorrarDetallePedido(request,idpedido):

    detPedido = DetallePedido.objects.get(pk = idpedido)

    pedido = Pedido.objects.get(pk = detPedido.pedido.numeroPedido)
    detPedido.delete()

    return HttpResponseRedirect('/ventas/detallePedido/'+ str(pedido.numeroPedido))


def GestionVentas(request):
    fechainicio = date.today() - timedelta(days=50)
    fechafin = date.today()
    ventas = Venta.objects.filter(fechaVenta__range =(fechainicio,fechafin))
    #ventas = Venta.objects.all()

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
        movimiento.desde = venta.bodega.nombreBodega
        if vnt.peso == 0:
            movimiento.salida = vnt.unidades
        else:
            movimiento.salida = vnt.peso
        movimiento.save()

    venta.guardado = True
    venta.save()

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

def EditaListaPrecios(request,idLista):
    listas = ListaDePrecios.objects.all()
    lista = ListaDePrecios.objects.get(pk = idLista)

    if request.method =='POST':
        formulario = ListaDePreciosForm(request.POST,instance=lista)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/listaPrecios/')
    else:
        formulario = ListaDePreciosForm(instance=lista)

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
@login_required()
def InicioVentas(request):
    return render_to_response('Ventas/TemplateVentaPunto.html',{},context_instance = RequestContext(request))

@login_required()
def PuntoVenta(request):
    usuario = request.user.username
    emp = Empleado.objects.get(usuario = usuario)
    valorInicial = ConfiguracionPuntos.objects.get(bodega = emp.punto.codigoBodega)
    punto = emp.punto.codigoBodega
    empleado = emp.codigoEmpleado
    jornada = valorInicial.jornada

    ventas = VentaPunto.objects.filter(fechaVenta = datetime.today()).filter(guardado = False).filter(puntoVenta = emp.punto.codigoBodega )
    consecutivo = ConfiguracionPuntos.objects.get(bodega = emp.punto.codigoBodega)

    if request.method =='POST':
        formulario = VentaPuntoForm(request.POST)
        if formulario.is_valid():
            if consecutivo.actual < consecutivo.finaliza:
                transaccion = formulario.save()
                numeroFactura = consecutivo.actual + 1
                consecutivo.actual = numeroFactura
                consecutivo.save()
                transaccion.factura = numeroFactura
                transaccion.save()


            return HttpResponseRedirect('/ventas/ventaPunto/')
    else:

        formulario = VentaPuntoForm(initial={'encargado':empleado,'jornada':jornada,'fechaVenta':datetime.today(),'puntoVenta':punto})
    return render_to_response('Ventas/TemplateVentaPunto.html',{'ventas':ventas,'formulario':formulario},
                              context_instance = RequestContext(request))
def TipoProducto(request):

    idProducto = request.GET.get('producto')
    producto = Producto.objects.get(pk = int(idProducto))

    if producto.pesables == True:
        msj = 'pesable'
    else:
        msj = 'no pesable'

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def DetallePuntoVenta(request,idVenta):
    detVentas =DetalleVentaPunto.objects.filter(venta = idVenta)
    venta = VentaPunto.objects.get(pk = idVenta)
    consecutivo = ValoresCostos.objects.get(nombreCosto = 'Facturacion')

    totalFactura = 0
    totalGravado = 0

    for detalle in detVentas:
        totalFactura += detalle.vrTotalPunto
        if detalle.productoVenta.gravado == True or detalle.productoVenta.gravado2 == True:
            totalGravado += detalle.vrTotalPunto

    totalGravado = (totalGravado /1.16) * 0.16
    venta.TotalVenta = totalFactura
    venta.save()

    Hora = datetime.now()

    if request.method =='POST':
        formulario = DetalleVentaPuntoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/ventas/detalleVentaPunto/'+ idVenta)
    else:

        formulario = DetalleVentaPuntoForm(initial={'venta':idVenta})
    return render_to_response('Ventas/TemplateDetalleVentaPunto.html',{'totalGravado':totalGravado,'Hora':Hora,
                                                                       'venta':venta,'formulario':formulario,
                                                                       'detVentas':detVentas,'consecutivo':consecutivo},
                              context_instance = RequestContext(request))

def EditaPuntoVenta(request,idDetVenta):
    detVenta = DetalleVentaPunto.objects.get(pk = idDetVenta)
    detVentas =DetalleVentaPunto.objects.filter(venta = detVenta.venta.numeroVenta)
    venta = VentaPunto.objects.get(pk = detVenta.venta.numeroVenta)

    totalFactura = 0

    for detalle in detVentas:
        totalFactura += detalle.vrTotalPunto

    venta.TotalVenta = totalFactura
    venta.save()

    if request.method =='POST':
        formulario = DetalleVentaPuntoForm(request.POST,instance=detVenta)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/ventas/detalleVentaPunto/'+ str(venta.numeroVenta))
    else:
        formulario = DetalleVentaPuntoForm(initial={'venta':venta.numeroVenta},instance=detVenta)
    return render_to_response('Ventas/TemplateDetalleVentaPunto.html',{'venta':venta,'formulario':formulario,'detVentas':detVentas},
                              context_instance = RequestContext(request))

def EliminaPuntoVenta(request,idDetVenta):
    detVenta = DetalleVentaPunto.objects.get(pk = idDetVenta)
    detVentas = DetalleVentaPunto.objects.filter(venta = detVenta.venta.numeroVenta)
    venta = VentaPunto.objects.get(pk = detVenta.venta.numeroVenta)
    detVenta.delete()

    totalFactura = 0

    for detalle in detVentas:
        totalFactura += detalle.vrTotalPunto

    venta.TotalVenta = totalFactura
    venta.save()

    return HttpResponseRedirect('/ventas/detalleVentaPunto/'+ str(venta.numeroVenta))

def CobrarVenta(request):

    idVenta = request.GET.get('venta')
    venta = VentaPunto.objects.get(pk = int(idVenta))
    detalleVenta = DetalleVentaPunto.objects.filter(venta = venta.numeroVenta)

    for detalle in detalleVenta:
        bodegaProducto = ProductoBodega.objects.get(bodega = venta.puntoVenta.codigoBodega,producto = detalle.productoVenta.codigoProducto)
        movimiento = Movimientos()
        movimiento.tipo = 'VNNOR%d'%(venta.numeroVenta)
        movimiento.fechaMov = venta.fechaVenta
        movimiento.productoMov = detalle.productoVenta
        movimiento.desde = bodegaProducto.bodega.nombreBodega

        if detalle.productoVenta.pesables == True:
            bodegaProducto.pesoProductoStock -= detalle.pesoVentaPunto
            movimiento.salida = detalle.pesoVentaPunto
        else:
            bodegaProducto.unidadesStock -= int(detalle.pesoVentaPunto)
            movimiento.salida = int(detalle.pesoVentaPunto)

        bodegaProducto.save()
        movimiento.save()

    venta.guardado = True
    venta.save()
    msj = 'Cobro exitoso, se han guardado %d registros'%(detalleVenta.count())
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')


def GestionCaja(request):
    fechainicio = date.today() - timedelta(days=5)
    fechafin = date.today()
    Cajas = Caja.objects.filter(fechaCaja__range =(fechainicio,fechafin))
    #Cajas = Caja.objects.all()

    if request.method =='POST':
        formulario = CajaForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/ventas/caja/')
    else:
        formulario = CajaForm()
    return render_to_response('Ventas/TemplateCaja.html',{'Cajas':Cajas,'formulario':formulario},
                              context_instance = RequestContext(request))

def EditaCaja(request,idCaja):
    caja = Caja.objects.get(pk = idCaja)
    fechainicio = date.today() - timedelta(days=5)
    fechafin = date.today()
    Cajas = Caja.objects.filter(fechaCaja__range =(fechainicio,fechafin))

    if request.method =='POST':
        formulario = CajaForm(request.POST,instance=caja)
        if formulario.is_valid():
            datos = formulario.save()

            facturas = VentaPunto.objects.filter(fechaVenta = caja.fechaCaja).filter(jornada = caja.jornada)
            retiros = Retiros.objects.filter(fechaRetiro = caja.fechaCaja).filter(guardado = True).filter(jornada = caja.jornada)
            restaurantes = VentaPunto.objects.filter(restaurante = True).filter(fechaVenta = caja.fechaCaja).filter(jornada = caja.jornada)

            ventaDia = 0
            retirosDia = 0
            restauranteDia = 0

            for restaurante in restaurantes:
                restauranteDia += restaurante.TotalVenta

            for retiro in retiros:
                retirosDia += retiro.cantidad

            for factura in facturas:
                if factura.anulado == False:
                    ventaDia += factura.TotalVenta
                #ventaDia += factura.TotalVenta

            caja.TotalRestaurante = restauranteDia
            caja.TotalVenta = ventaDia - restauranteDia
            caja.TotalRetiro = retirosDia
            caja.TotalResiduo = (caja.TotalEfectivo - retirosDia  ) - (caja.TotalVenta - retirosDia )
            caja.save()

            return HttpResponseRedirect('/ventas/caja/')
    else:
        formulario = CajaForm(instance=caja)
    return render_to_response('Ventas/TemplateCaja.html',{'Cajas':Cajas,'formulario':formulario},
                              context_instance = RequestContext(request))

def ValorProdVenta(request):
    idProducto = request.GET.get('idProducto')
    numVenta = request.GET.get('numVenta')
    venta = VentaPunto.objects.get(pk = int(numVenta))
    usuario = request.user.username
    emp = Empleado.objects.get(usuario = usuario)

    lista = ListaDePrecios.objects.get(tipoLista = 'Punto',bodega = emp.punto.codigoBodega)
    valor = DetalleLista.objects.filter(lista = lista.codigoLista).get(productoLista = int(idProducto)).precioVenta

    respuesta = json.dumps(valor)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionRetiros(request):

    retiros = Retiros.objects.all()

    if request.method =='POST':
        formulario = RetirosForm(request.POST)
        if formulario.is_valid():
            datos = formulario.save()
            cadena = '%s %s'%(datos.encargado.nombre, datos.encargado.apellido)
            datos.nombreEncargado = cadena
            datos.save()

            return HttpResponseRedirect('/ventas/retiro/')
    else:
        formulario = RetirosForm()

    return render_to_response('Ventas/TemplateRetiros.html',{'retiros':retiros,'formulario':formulario},
                              context_instance = RequestContext(request))

def ImprimirRetiro(request):
    idRetiro = request.GET.get('idRetiro')
    retiro = Retiros.objects.filter(pk = int(idRetiro))
    respuesta = serializers.serialize('json',retiro)
    for ret in retiro:
        ret.guardado = True
        ret.save()

    return HttpResponse(respuesta,mimetype='application/json')

def GestionarDevolucion(request):
    devoluciones = Devolucion.objects.filter(fechaDevolucion = datetime.today())

    if request.method =='POST':
        formulario = DevolucionesForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/devoluciones/')
    else:
        formulario = DevolucionesForm()

    return render_to_response('Ventas/TemplateDevoluciones.html',{'devoluciones':devoluciones,'formulario':formulario},
                              context_instance = RequestContext(request))

def GestionDetalleDevolucion(request,idDev):
    devolucion = Devolucion.objects.get(pk = idDev)
    detalles = DetalleDevolucion.objects.filter(devolucion = idDev)

    if request.method =='POST':
        formulario = DetalleDevolucionForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/detalleDevoluciones/'+ idDev)
    else:
        formulario = DetalleDevolucionForm(initial={'devolucion':idDev})

    return render_to_response('Ventas/TemplateDetalleDevolucion.html',{'detalles':detalles,'devolucion':devolucion,
                                                                       'formulario':formulario},
                              context_instance = RequestContext(request))

def GuardarDevolucion(request):

    idDetalleDev = request.GET.get('idDetalleDev')
    detalles = DetalleDevolucion.objects.filter(devolucion = int(idDetalleDev))
    for detalle in detalles:
        bodegaProd = ProductoBodega.objects.get(bodega = 1, producto = detalle.productoDev.codigoProducto)
        if detalle.pesoProducto == 0:
            bodegaProd.unidadesStock += detalle.cantidad
        else:
            bodegaProd.pesoProductoStock += detalle.pesoProducto
        bodegaProd.save()

    msj = 'Se guargaron Exitosamente las devoluciones'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GuaradarPedido(request):

    idPedido = request.GET.get('idPedido')
    pedido = Pedido.objects.get(pk = int(idPedido))
    detPedido = DetallePedido.objects.filter(pedido = int(idPedido))

    for det in detPedido:
        bodega = ProductoBodega.objects.get(bodega = pedido.bodega.codigoBodega,producto = det.producto.codigoProducto)
        bodega.pesoProductoStock -= det.pesoPedido
        bodega.unidadesStock -= det.unidadesPedido
        bodega.save()

        movimiento = Movimientos()
        movimiento.tipo = 'PED%d'%(pedido.numeroPedido)
        movimiento.fechaMov = pedido.fechaPedido
        movimiento.productoMov = det.producto
        movimiento.nombreProd = det.producto.nombreProducto
        movimiento.desde = bodega.bodega.nombreBodega

        if det.pesoPedido == 0:
            movimiento.salida = det.unidadesPedido
        else:
            movimiento.salida = det.pesoPedido

        movimiento.save()

    pedido.guardado = True
    pedido.save()

    msj = 'Se guardaron Exitosamente los Registros'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def VerificarPrecioPedido(request):
    idLista = request.GET.get('idLista')
    idProducto = request.GET.get('idProducto')
    detalleLista = DetalleLista.objects.get(lista = int(idLista),productoLista = int(idProducto))
    valorProducto = detalleLista.precioVenta
    respuesta = json.dumps(valorProducto)
    return HttpResponse(respuesta,mimetype='application/json')

def TemplateAZ(request):
    bodegas = Bodega.objects.all()
    usuario = request.user
    empleado = Empleado.objects.get(usuario = usuario.username)

    if usuario.is_staff:
        plantilla = 'base.html'
    else:
        plantilla = 'PuntoVentaNorte.html'
    return render_to_response('Ventas/TemplateAZ.html',{'empleado':empleado,'plantilla':plantilla,'bodegas':bodegas},context_instance = RequestContext(request))

def ReporteAZ(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    jornada = request.GET.get('jornada')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    idBodega = request.GET.get('bodega')

    #ventas = VentaPunto.objects.filter(fechaVenta__range = (finicio,ffin)).filter(jornada = jornada)
    ventas = VentaPunto.objects.filter(fechaVenta = finicio,jornada = jornada,puntoVenta = int(idBodega)).filter(anulado = False).order_by('factura')
    consecutivo = ConfiguracionPuntos.objects.get(bodega = int(idBodega))

    gravados1 = {}
    gravados2 = {}
    excentos = {}
    excluidos = {}
    totalVenta = {}
    inicial = {}
    final = {}
    consec = {}

    gravados1['Gravados 1'] = 0
    gravados2['Gravados 2'] = 0
    excentos['Exentos'] = 0
    excluidos['Excluidos'] = 0
    totalVenta['Total Venta'] = 0

    finaliza = 0
    cantVentas = ventas.count()
    cont =  0
    inicializa = 0

    for venta in ventas:
        if cont == 0:
            cont +=1
            inicializa = venta.factura
        else:
            break

    for venta in ventas:
        finaliza = venta.factura


    for venta in ventas:
        detalleVenta = DetalleVentaPunto.objects.filter(venta = venta.numeroVenta)
        totalVenta['Total Venta'] += venta.TotalVenta
        finaliza = venta.factura
        if venta.anulado == False:
            for detalle in detalleVenta:
                if detalle.productoVenta.gravado == True:
                    gravados1['Gravados 1'] += detalle.vrTotalPunto
                elif detalle.productoVenta.gravado2 == True:
                    gravados2['Gravados 2'] += detalle.vrTotalPunto
                elif detalle.productoVenta.excento == True:
                    excentos['Exentos'] += detalle.vrTotalPunto
                elif detalle.productoVenta.excluido == True:
                    excluidos['Excluidos'] += detalle.vrTotalPunto

    #inicializa = finaliza - cantVentas
    consecutivo.consecutivoZ += 1
    consecutivo.save()

    inicial['inicializa'] = inicializa
    final['Finaliza'] = finaliza
    consec['Consecutivo'] = consecutivo.consecutivoZ

    #*********************************Pesos y Valores Vendidos *********************************************************

    PesoProductos = {}
    UdnProductos = {}
    ValorProductos = {}
    ValorUnds = {}

    for venta in ventas:
        detalleVenta = DetalleVentaPunto.objects.filter(venta = venta.numeroVenta)
        for detalle in detalleVenta:
            if detalle.productoVenta.pesables == True:
                PesoProductos[detalle.productoVenta.nombreProducto] = 0
                ValorProductos[detalle.productoVenta.nombreProducto] = 0
            else:
                UdnProductos[detalle.productoVenta.nombreProducto] = 0
                ValorUnds[detalle.productoVenta.nombreProducto] = 0



    for venta in ventas:
        detalleVenta = DetalleVentaPunto.objects.filter(venta = venta.numeroVenta)
        for detalle in detalleVenta:
            if detalle.productoVenta.pesables == True:
                PesoProductos[detalle.productoVenta.nombreProducto] += ceil(detalle.pesoVentaPunto)
                ValorProductos[detalle.productoVenta.nombreProducto] += detalle.vrTotalPunto
            else:
                UdnProductos[detalle.productoVenta.nombreProducto] += ceil(detalle.pesoVentaPunto)
                ValorUnds[detalle.productoVenta.nombreProducto] += detalle.vrTotalPunto



    listas = {'gravados1':gravados1,'gravados2':gravados2,
              'excentos':excentos,'excluidos':excluidos,
              'totalVenta':totalVenta,'inicial':inicial,'final':final,
              'consec':consec,'PesoProductos':PesoProductos,'ValorProductos':ValorProductos,
              'UdnProductos':UdnProductos,'ValorUnds':ValorUnds}

    respuesta = json.dumps(listas)

    return HttpResponse(respuesta,mimetype='application/json')

def TemplateReporteVentaNorte(request):
    bodegas = Bodega.objects.all()
    return render_to_response('Ventas/TemplateRepoVentaNorte.html',{'bodegas':bodegas},
                              context_instance = RequestContext(request))

def ReporteVentaNorte(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    jornada = request.GET.get('jornada')
    bodega = request.GET.get('bodega')
    tipoReporte = request.GET.get('tipoReporte')

    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    PesoProductos = {}
    UdnProductos = {}
    ValorProductos = {}
    ValorUnds = {}

    if tipoReporte == 'ventas':
        ventas = VentaPunto.objects.filter(fechaVenta__range = (finicio,ffin)).filter(jornada = jornada , puntoVenta = int(bodega))

        for venta in ventas:
            detalleVenta = DetalleVentaPunto.objects.filter(venta = venta.numeroVenta)
            for detalle in detalleVenta:
                if detalle.productoVenta.pesables:
                    PesoProductos[detalle.productoVenta.nombreProducto] = 0
                    ValorProductos[detalle.productoVenta.nombreProducto] = 0
                else:
                    UdnProductos[detalle.productoVenta.nombreProducto] = 0
                    ValorUnds[detalle.productoVenta.nombreProducto] = 0

        for venta in ventas:
            detalleVenta = DetalleVentaPunto.objects.filter(venta = venta.numeroVenta)
            for detalle in detalleVenta:
                if detalle.productoVenta.pesables:
                    PesoProductos[detalle.productoVenta.nombreProducto] += ceil(detalle.pesoVentaPunto)
                    ValorProductos[detalle.productoVenta.nombreProducto] += detalle.vrTotalPunto
                else:
                    UdnProductos[detalle.productoVenta.nombreProducto] += ceil(detalle.pesoVentaPunto)
                    ValorUnds[detalle.productoVenta.nombreProducto] += detalle.vrTotalPunto
    else:
        pedidos = Pedido.objects.filter(fechaPedido__range = (finicio,ffin)).filter(bodega = int(bodega))

        for pedido in pedidos:
            detallePedido = DetallePedido.objects.filter(pedido = pedido.numeroPedido)
            for detalle in detallePedido:
                if detalle.producto.pesables:
                    PesoProductos[detalle.producto.nombreProducto] = 0
                    ValorProductos[detalle.producto.nombreProducto] = 0
                else:
                    UdnProductos[detalle.producto.nombreProducto] = 0
                    ValorUnds[detalle.producto.nombreProducto] = 0



        for pedido in pedidos:
            detallePedido = DetallePedido.objects.filter(pedido = pedido.numeroPedido)
            for detalle in detallePedido:
                if detalle.producto.pesables:
                    PesoProductos[detalle.producto.nombreProducto] += ceil(detalle.pesoPedido)
                    ValorProductos[detalle.producto.nombreProducto] += detalle.vrTotalPedido
                else:
                    UdnProductos[detalle.producto.nombreProducto] += ceil(detalle.unidadesPedido)
                    ValorUnds[detalle.producto.nombreProducto] += detalle.vrTotalPedido

    listas = {'PesoProductos':PesoProductos,'ValorProductos':ValorProductos,'UdnProductos':UdnProductos,'ValorUnds':ValorUnds}
    respuesta = json.dumps(listas)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionConfigPuntos(request):
    configuraciones = ConfiguracionPuntos.objects.all()
    if request.method =='POST':
        formulario = ConfigPuntosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/configPuntos/')
    else:
        formulario = ConfigPuntosForm()

    return render_to_response('Ventas/TemplateConfigPuntos.html',{'configuraciones':configuraciones,'formulario':formulario},
                              context_instance = RequestContext(request))

def EditaConfigPuntos(request,idConfig):
    configuracion = ConfiguracionPuntos.objects.get(pk = idConfig)
    configuraciones = ConfiguracionPuntos.objects.all()
    if request.method =='POST':
        formulario = ConfigPuntosForm(request.POST,instance=configuracion)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/ventas/configPuntos/')
    else:
        formulario = ConfigPuntosForm(instance=configuracion)

    return render_to_response('Ventas/TemplateConfigPuntos.html',{'configuraciones':configuraciones,'formulario':formulario},
                              context_instance = RequestContext(request))

def TemplateRepListVentasNorte(request):
    provedor = Proveedor.objects.all()
    bodega = Bodega.objects.all()

    return render_to_response('Ventas/TemplateRepListVentasNorte.html',{'provedor':provedor,'bodega':bodega},
                              context_instance = RequestContext(request))

def RepListVentasNorte(request):
    jornada = request.GET.get('jornada')
    idBodega = request.GET.get('bodega')

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()


    bodega = Bodega.objects.get(pk = int(idBodega))
    ventas = VentaPunto.objects.filter(fechaVenta__range = (finicio,ffin),puntoVenta = bodega.codigoBodega).filter(jornada = jornada).order_by('factura')
    respuesta = serializers.serialize('json',ventas)

    return HttpResponse(respuesta,mimetype='application/json')

def AnulaVentas(request):
    idFactura = request.GET.get('idFactura')
    factura = VentaPunto.objects.get(pk = int(idFactura))
    detalleFactura = DetalleVentaPunto.objects.filter(venta = factura.numeroVenta)

    for detalle in detalleFactura:
        bodega = ProductoBodega.objects.get(bodega = factura.puntoVenta.codigoBodega,producto = detalle.productoVenta.codigoProducto)
        bodega.pesoProductoStock += detalle.pesoVentaPunto
        bodega.unidadesStock += detalle.unidades
        bodega.save()

    factura.anulado = True
    factura.save()

    msj = 'Registro Anulado Correctamente'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

