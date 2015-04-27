 # -*- coding: UTF-8 -*-
from decimal import Decimal
from math import ceil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
from Inventario.Forms.forms import *
from Inventario.models import *

from Fabricacion.Forms import *

# Create your views here.

def listaProvedoresAjax(request):
    provedores = Proveedor.objects.all()
    data = serializers.serialize('json',provedores,fields = ('nit','nombreProv','direccionProv','telefonoProv',
                                                             'email','ciudad'))
    return HttpResponse(data, mimetype='application/json')

@login_required()
def inicio(request):
    return render_to_response('Inicio.html',{},context_instance = RequestContext(request))

def home(request):
    productosBajoStock = ProductoBodega.objects.select_related().filter(pesoProductoStock__gt = 500).order_by('bodega')
    costosProductos = Producto.objects.select_related().order_by('nombreProducto')
    return render_to_response('Home.html',{'productosBajoStock':productosBajoStock,'costosProductos':costosProductos},
                              context_instance = RequestContext(request))

#***************************************PRODUCTOS******************************************
def listaProductos(request):
    productos = Producto.objects.select_related().order_by('codigoProducto')

    #se actualiza el precio sugerido del producto
    '''for producto in productos:

        producto.precioSugerido = ceil(producto.costoProducto * 1.33)
        producto.save()'''

    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            # BasicosProcesados solo se grabaran en la bodega de Taller
            if producto.grupo.nombreGrupo == "Basicos Procesados" or producto.grupo.nombreGrupo == "Verduras":

                bodegaInicial = ProductoBodega()
                bodega = Bodega.objects.get(nombreBodega = 'Taller')

                bodegaInicial.producto = producto
                bodegaInicial.nombreProducto = producto.nombreProducto
                bodegaInicial.bodega = bodega
                bodegaInicial.pesoProductoStock = 0
                bodegaInicial.unidadesStock = 0
                bodegaInicial.save()

            else:

                for bod in Bodega.objects.all():

                    bodegaInicial = ProductoBodega()
                    bodega = Bodega.objects.get(pk = bod.codigoBodega)

                    bodegaInicial.producto = producto
                    bodegaInicial.nombreProducto = producto.nombreProducto
                    bodegaInicial.bodega = bodega
                    bodegaInicial.pesoProductoStock = 0
                    bodegaInicial.unidadesStock = 0
                    bodegaInicial.deshidratacion = 0
                    bodegaInicial.save()

            return HttpResponseRedirect('/inventario/listaProd')
    else:
        formulario = ProductoForm()

    return render_to_response('Inventario/GestionProducto.html', {'formulario':formulario,'productos':productos},
                              context_instance = RequestContext(request))

def borrar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    producto.delete()
    return  HttpResponseRedirect('/listaProd')

def editar_producto(request, id_producto):
    productos = Producto.objects.all().order_by('nombreProducto')
    producto = Producto.objects.get(pk=id_producto)
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/listaProd')
    else:
        formulario = ProductoForm(instance=producto)
    return  render_to_response('Inventario/GestionProducto.html',{'formulario':formulario,'productos':productos },
                               context_instance = RequestContext(request))

#******************************************************************************************
#***********************************SUBPRODUCTOS*******************************************

def listaSubProductos(request):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    if request.method == 'POST':

        formulario = SubProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/verSubProductos/')
    else:
        formulario =SubProductoForm()

    return render_to_response('Inventario/GestionSubProducto.html',{'formulario':formulario,'subproductos':subproductos },
                              context_instance = RequestContext(request))


def borrarSubproducto(request, idSubproducto):
    subproducto = SubProducto.objects.get(pk=idSubproducto)
    subproducto.delete()

    return  HttpResponseRedirect('/inventario/verSubProductos')

def editarSubproducto(request, idSproducto):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    sproducto = SubProducto.objects.get(pk=idSproducto)
    if request.method == 'POST':
        formulario = SubProductoForm(request.POST, instance=sproducto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/verSubProductos')
    else:
        formulario = SubProductoForm(instance=sproducto)

    return  render_to_response('Inventario/GestionSubProducto.html',{'formulario':formulario,'subproductos':subproductos},
                               context_instance = RequestContext(request))

def AgregarDetSubProducto(request,id_subproducto):

    subrpoductos = SubProducto.objects.get(pk = id_subproducto)
    desubproductos = DetalleSubProducto.objects.filter(subproducto = id_subproducto)

    detSubp = DetalleSubProducto.objects.all()
    totalPeso = 0
    totalUnd = 0

    for dts in detSubp: # clacular los totales de la lista de detalles de subproducto
        totalPeso += dts.pesoUnitProducto
        totalUnd += dts.unidades

    if request.method == 'POST':
        formulario = DetSubProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/addDSprod/'+ id_subproducto)
    else:
        formulario = DetSubProductoForm(initial={'subproducto':id_subproducto})

    return render_to_response('Inventario/GestionDetalleSubProducto.html',{'Tunds':totalUnd,'TPeso':totalPeso,'formulario':formulario,
                                                         'subrpoductos': subrpoductos,
                                                         'desubproductos': desubproductos},
                                                        context_instance = RequestContext(request))

def borrarDetalleSp(request, idDetalle):
    detsubproducto = DetalleSubProducto.objects.get(pk=idDetalle)
    detsubproducto.delete()
    return  HttpResponseRedirect('/inventario/verSubProductos')

#**************************************BODEGA****************************************************

def GestionBodega(request):
    bodegas = Bodega.objects.all()
    prodBods = ProductoBodega.objects.all()

    '''for bodega in prodBods:
        bodega.nombreProducto = bodega.producto.nombreProducto
        bodega.save()'''


    if request.method == 'POST':
        formulario = BodegaForm(request.POST)
        if formulario.is_valid():
            bodega = formulario.save()


            producto = Producto.objects.all()

            for prod in producto:

                grupo = prod.grupo.nombreGrupo

                if grupo == 'Reses' or grupo == 'Cerdos' or grupo == 'Cerdas' or grupo == 'Compra/Venta' or grupo == 'Pollos':
                    productoBodega = ProductoBodega()
                    productoBodega.producto = prod
                    productoBodega.bodega = bodega
                    productoBodega.pesoProductoStock = 0
                    productoBodega.unidadesStock = 0
                    productoBodega.save()



            return HttpResponseRedirect('/inventario/bodega')
    else:
        formulario = BodegaForm()

    return render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas },
                              context_instance = RequestContext(request))

def GestionGrupo(request):
    grupos = Grupo.objects.all()
    if request.method == 'POST':
        formulario = GrupoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/grupo')
    else:
        formulario = GrupoForm()

    return render_to_response('Inventario/GestionGrupo.html',{'formulario':formulario,'grupos':grupos },
                              context_instance = RequestContext(request))

#*******************************************RECEPCION DE GANADO*********************************************************
def GestionPlanillaRecepcion(request,idcompra):

    recepciones = PlanillaRecepcion.objects.filter(compra = idcompra)
    detCompra = DetalleCompra.objects.filter(compra = idcompra)
    compra = Compra.objects.get(pk = idcompra)
    compra.cantCabezas = detCompra.count()

    if request.method == 'POST':
        formulario = PlanillaRecepcionForm(request.POST)
        if formulario.is_valid():
            Recepcion = formulario.save()

            Recepcion.tipoGanado = request.POST.get('tipoGanado')
            Recepcion.cantCabezas = detCompra.count()
            Recepcion.transporte = request.POST.get('transporte')
            Recepcion.save()

            return HttpResponseRedirect('/inventario/recepcion/'+ idcompra)
    else:
        formulario = PlanillaRecepcionForm(initial={'compra':idcompra})

    return render_to_response('Fabricacion/GestionPlanillaRecepcion.html',{'formulario':formulario,'recepciones':recepciones },
                              context_instance = RequestContext(request))


def editarBodega(request, idBodega):
    bodegas = Bodega.objects.all()
    bodega = Bodega.objects.get(pk=idBodega)
    if request.method == 'POST':
        formulario = BodegaForm(request.POST, instance=bodega)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/bodega')
    else:
        formulario = BodegaForm(instance=bodega)

    return  render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas},
                               context_instance = RequestContext(request))

def borrarBodega(request,idbodega ):
    bodega = Bodega.objects.get(pk=idbodega)
    bodega.delete()
    return  HttpResponseRedirect('/inventario/bodega')

def GestionProductoBodega(request,idproducto):
    productoBodegas = ProductoBodega.objects.filter(producto = idproducto)
    producto = Producto.objects.get(pk = idproducto)

    return render_to_response('Inventario/GestionProductoBodega.html',{'productoBodegas':productoBodegas,
                                                                       'producto':producto },
                              context_instance = RequestContext(request))

#*****************************************PROVEEDOR**************************************************

def GestionProvedor(request):
    provedores = Proveedor.objects.all()
    if request.method == 'POST':
        formulario = ProvedorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/provedor')
    else:
        formulario = ProvedorForm()

    return render_to_response('Inventario/GestionProvedor.html',{'formulario':formulario,'provedores':provedores },
                              context_instance = RequestContext(request))

#************************************************GANADO*******************************************************

def GestionGanado(request,idcompra):

    ganados = Ganado.objects.filter(compra = idcompra).order_by('-codigoGanado')
    compra = Compra.objects.get(pk = idcompra)
    detallecompra = DetalleCompra()
    totalPie = 0
    for ganado in ganados:
        totalPie += ganado.pesoEnPie
        ganado.TotalpesoEnPie = totalPie
        ganado.save()


    if request.method == 'POST':
        formulario = GanadoForm(request.POST)
        if formulario.is_valid():
            ganado = formulario.save()



            detallecompra.compra = compra
            detallecompra.ganado = ganado
            detallecompra.pesoProducto = request.POST.get('pesoEnPie')
            detallecompra.unidades = 1
            detallecompra.vrCompraProducto = ganado.precioTotal
            detallecompra.estado = False
            detallecompra.subtotal = ganado.precioTotal
            detallecompra.save()

            artCompra = DetalleCompra.objects.filter(compra = idcompra)
            totalCompra = 0
            totalPesoFactura = 0

            for dcmp in artCompra:
                totalPesoFactura += dcmp.pesoProducto

            for dcmp in artCompra:
                totalCompra += dcmp.subtotal

            compra.vrCompra = totalCompra
            compra.save()

            return HttpResponseRedirect('/inventario/ganado/'+idcompra)
    else:
        kiloEnPie= ValoresCostos.objects.get(nombreCosto = 'Costos Reses').valorKiloPie
        formulario = GanadoForm(initial={'precioKiloEnPie':kiloEnPie,'compra':idcompra,'piel':'Friana'})

    return render_to_response('Inventario/GestionGanado.html',{'formulario':formulario,'ganados':ganados,'compra':idcompra },
                              context_instance = RequestContext(request))

#**********************************************************COMPRA*******************************************************
def GestionCompra(request):
    usuario = request.user
    emp = Empleado.objects.get(usuario = usuario.username)
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    if usuario.is_staff:
        compras = Compra.objects.select_related().filter(fechaCompra__range =(fechainicio,fechafin))
        plantilla = 'base.html'

    else:
        compras = Compra.objects.select_related().filter(fechaCompra__range =(fechainicio,fechafin),bodegaCompra = emp.punto.codigoBodega )
        plantilla = 'PuntoVentaNorte.html'


    #compras= Compra.objects.all()

    if request.method == 'POST':
        formulario = CompraForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/inventario/compra')
    else:
        formulario =CompraForm(initial={'encargado':12951685,'bodegaCompra':emp.punto.codigoBodega})


    return render_to_response('Inventario/GestionCompras.html',{'plantilla':plantilla,'formulario':formulario,'compras':compras },
                              context_instance = RequestContext(request))

def borrarCompra(request, idCompra):
    compra = Compra.objects.get(pk = idCompra)
    compra.delete()
    return HttpResponseRedirect('/inventario/compra')

def ModificaCompra(request,idCompra):
    usuario = request.user
    fechainicio = date.today() - timedelta(days=22)
    fechafin = date.today()
    compras = Compra.objects.filter(fechaCompra__range =(fechainicio,fechafin))
    compra = Compra.objects.get(pk = idCompra)
    #compras= Compra.objects.all()

    if request.method == 'POST':
        formulario = CompraForm(request.POST,instance=compra)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/inventario/compra')
    else:
        formulario = CompraForm(initial={'encargado':12951685},instance=compra)
    plantilla = ''
    if usuario.is_staff:
        plantilla = 'base.html'
    else:
        plantilla = 'PuntoVentaNorte.html'


    return render_to_response('Inventario/GestionCompras.html',{'plantilla':plantilla,'formulario':formulario,'compras':compras },
                              context_instance = RequestContext(request))

def borrarDetCompra(request, idDetCompra):
    detCompra = DetalleCompra.objects.get(pk = idDetCompra)
    detCompra.delete()
    return  HttpResponseRedirect('/inventario/detcompra/'+str(detCompra.compra.codigoCompra))


def GestionDetalleCompra(request,idcompra):

    compra = Compra.objects.get(pk = idcompra)
    detcompras = DetalleCompra.objects.filter(compra = idcompra)
    totalCompra  = 0
    totalPeso = 0

    # clacular los totales de la lista de detalles de subproducto
    for dcmp in detcompras:
        totalCompra += dcmp.subtotal
    for dcmp in detcompras:
        totalPeso += dcmp.pesoProducto

    compra.vrCompra = totalCompra
    compra.save()

    if request.method == 'POST':
        formulario = DetalleCompraForm(idcompra,request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/inventario/detcompra/'+ idcompra)
    else:
        formulario = DetalleCompraForm(idcompra,initial={'compra':idcompra })

    return render_to_response('Inventario/GestionDetalleCompra.html',{'formulario':formulario,
                                                         'compra': compra,'detcompras': detcompras,
                                                         'totalCompra':totalCompra,'totalPeso':totalPeso},
                                                        context_instance = RequestContext(request))

def EditaDetalleCompra(request,idDetCompra):

    detCompra = DetalleCompra.objects.get(pk = idDetCompra)
    compra = Compra.objects.get(pk = detCompra.compra.codigoCompra)
    detcompras = DetalleCompra.objects.filter(compra = compra.codigoCompra)
    totalCompra  = 0
    totalPeso = 0

    # clacular los totales de la lista de detalles de subproducto
    for dcmp in detcompras:
        totalCompra += dcmp.subtotal
    for dcmp in detcompras:
        totalPeso += dcmp.pesoProducto

    compra.vrCompra = totalCompra
    compra.save()

    if request.method == 'POST':
        formulario = DetalleCompraForm(str(compra.codigoCompra),request.POST,instance=detCompra)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/inventario/detcompra/'+ str(compra.codigoCompra))
    else:
        formulario = DetalleCompraForm(str(compra.codigoCompra),initial={'compra':compra.codigoCompra},instance=detCompra)

    return render_to_response('Inventario/GestionDetalleCompra.html',{'formulario':formulario,
                                                         'compra': compra,'detcompras': detcompras,
                                                         'totalCompra':totalCompra,'totalPeso':totalPeso},
                                                        context_instance = RequestContext(request))

def GuardarDetCompra(request):
    idcompra = request.GET.get('idCompra')
    compra = Compra.objects.get(pk = int(idcompra))
    detcompras = DetalleCompra.objects.filter(compra = compra.codigoCompra)

    for detalle in detcompras:
        productoBodega = ProductoBodega.objects.get(bodega = compra.bodegaCompra.codigoBodega,producto = detalle.producto.codigoProducto)
        producto = Producto.objects.get(pk = detalle.producto.codigoProducto)
        movimiento = Movimientos()#Registro los datos en la tabla de movimientos
        movimiento.tipo = 'CMP%d'%(compra.codigoCompra)
        movimiento.fechaMov = compra.fechaCompra
        movimiento.productoMov = detalle.producto
        movimiento.nombreProd =  detalle.producto.nombreProducto
        movimiento.Hasta = compra.bodegaCompra.nombreBodega

        #if compra.tipo.id == 6 or compra.tipo.id == 7 or compra.tipo.id == 8 or compra.tipo.id == 9:

        productoBodega.pesoProductoStock += detalle.pesoProducto
        productoBodega.unidadesStock += detalle.unidades
        productoBodega.save()

        if detalle.producto.pesables == True:
            movimiento.entrada = detalle.pesoProducto
        else:
            movimiento.entrada = detalle.unidades

        producto.costoProducto = detalle.vrCompraProducto
        producto.save()
        movimiento.save()

    compra.guardado = True
    compra.save()
    msj = 'Registros Guardados exitosamente'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')


def EditaCompra(request,idDetCompra):

    detcompra = DetalleCompra.objects.get(pk = idDetCompra)
    compra = Compra.objects.get(pk = detcompra.compra.codigoCompra)
    detcompras = DetalleCompra.objects.filter(compra = compra.codigoCompra)

    if request.method == 'POST':
        formulario = DetalleCompraForm(compra.codigoCompra,request.POST,instance=detcompra)
        if formulario.is_valid():
            datos = formulario.save()
            for detcomp in detcompras:
                #Guardamos las cantidades en la bodega ademas del costo del producto
                producto = Producto.objects.get(pk = detcomp.producto.codigoProducto)
                bodega = ProductoBodega.objects.get(bodega = 5,producto = producto.codigoProducto)

                producto.costoProducto = datos.vrKiloDescongelado
                producto.save()

                bodega.pesoProductoStock += datos.pesoDescongelado
                bodega.unidadesStock += datos.unidades
                bodega.save()

                movimiento = Movimientos()
                movimiento.tipo = 'CMP%d'%(compra.codigoCompra)
                movimiento.fechaMov = compra.fechaCompra
                movimiento.productoMov = detcomp.producto
                movimiento.nombreProd = detcomp.producto.nombreProducto
                movimiento.entrada = datos.pesoDescongelado
                movimiento.Hasta = bodega.bodega.nombreBodega
                movimiento.save()

                detcompra.estado =True
                detcompra.save()
            return HttpResponseRedirect('/inventario/detcompra/'+ str(compra.codigoCompra))
    else:
        formulario = DetalleCompraForm(compra.codigoCompra,initial={'compra':compra.codigoCompra },instance=detcompra)

    return render_to_response('Inventario/GestionDetalleCompra.html',{'formulario':formulario,'compra': compra,
                                                         'detcompras': detcompras},
                                                        context_instance = RequestContext(request))
#********************************************TRASLADOS******************************************************
def GestionTraslados(request):
    usuario = request.user
    empleado = Empleado.objects.get(usuario = usuario.username)
    fechainicio = date.today() - timedelta(days=11)
    fechafin = date.today()

    if usuario.is_staff:
        q1 = Traslado.objects.all().order_by('fechaTraslado').\
        filter(fechaTraslado__range = (fechainicio,fechafin))
        traslados = q1
    else:
        q1 = Traslado.objects.all().order_by('fechaTraslado').\
        filter(fechaTraslado__range = (fechainicio,fechafin))\
        .filter(bodegaActual = empleado.punto.codigoBodega)

        q2 = Traslado.objects.all().order_by('fechaTraslado').\
            filter(fechaTraslado__range = (fechainicio,fechafin),
                   bodegaDestino = empleado.punto.nombreBodega)
        traslados = q1|q2

    if request.method == 'POST':

        formulario = TrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/traslado')
    else:
        formulario =TrasladoForm()

    plantilla = ''
    if usuario.is_staff:
        plantilla = 'base.html'
    else:
        plantilla = 'PuntoVentaNorte.html'

    return render_to_response('Inventario/GestionTraslado.html',{'plantilla':plantilla,'formulario':formulario,'traslados':traslados },
                              context_instance = RequestContext(request))

def EditaTraslados(request,idTraslado):
    trasladoEditar = Traslado.objects.get(pk = idTraslado)
    usuario = request.user
    empleado = Empleado.objects.get(usuario = usuario.username)
    fechainicio = date.today() - timedelta(days=11)
    fechafin = date.today()

    if usuario.is_staff:
        q1 = Traslado.objects.all().order_by('fechaTraslado').\
        filter(fechaTraslado__range = (fechainicio,fechafin))
        traslados = q1
    else:
        q1 = Traslado.objects.all().order_by('fechaTraslado').\
        filter(fechaTraslado__range = (fechainicio,fechafin))\
        .filter(bodegaActual = empleado.punto.codigoBodega)
        q2 = Traslado.objects.all().order_by('fechaTraslado').\
        filter(fechaTraslado__range = (fechainicio,fechafin))\
        .filter(bodegaDestino = empleado.punto.nombreBodega)
        traslados = q1|q2

    if request.method == 'POST':

        formulario = TrasladoForm(request.POST,instance=trasladoEditar)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/traslado')
    else:
        formulario =TrasladoForm(instance=trasladoEditar)

    plantilla = ''
    if usuario.is_staff:
        plantilla = 'base.html'
    else:
        plantilla = 'PuntoVentaNorte.html'

    return render_to_response('Inventario/GestionTraslado.html',{'plantilla':plantilla,'formulario':formulario,'traslados':traslados },
                              context_instance = RequestContext(request))


def borrarTraslado(request,idTraslado):
    traslado = Traslado.objects.select_related().get(pk = idTraslado)
    detalletraslado = DetalleTraslado.objects.select_related().filter(traslado = idTraslado)

    for detalle in detalletraslado:

        bodegaOrigen = ProductoBodega.objects.get(bodega = traslado.bodegaActual.codigoBodega,producto = detalle.productoTraslado.codigoProducto)
        bodegaDestino = ProductoBodega.objects.get(bodega__nombreBodega = traslado.bodegaDestino,producto = detalle.productoTraslado.codigoProducto)

        bodegaOrigen.pesoProductoStock += detalle.pesoTraslado
        bodegaOrigen.unidadesStock += detalle.unidadesTraslado

        bodegaDestino.pesoProductoStock -= detalle.pesoTraslado
        bodegaDestino.unidadesStock -= detalle.unidadesTraslado

        movimiento = Movimientos()
        movimiento.tipo = 'TRSREV%d'%(traslado.codigoTraslado)
        movimiento.productoMov = detalle.productoTraslado
        movimiento.nombreProd = detalle.productoTraslado.nombreProducto
        movimiento.fechaMov = traslado.fechaTraslado
        movimiento.desde = bodegaDestino.bodega.nombreBodega
        movimiento.Hasta = bodegaOrigen.bodega.nombreBodega
        if detalle.productoTraslado.noPesables:
            movimiento.entrada = detalle.unidadesTraslado
            movimiento.salida = detalle.unidadesTraslado
        else:
            movimiento.entrada = detalle.pesoTraslado
            movimiento.salida = detalle.pesoTraslado

        movimiento.save()
        bodegaOrigen.save()
        bodegaDestino.save()

    traslado.delete()
    return HttpResponseRedirect('/inventario/traslado')


def GestionDetalleTraslado(request,idtraslado):

    traslado = Traslado.objects.get(pk = idtraslado)
    detraslados = DetalleTraslado.objects.filter(traslado = idtraslado)

    exito = False

    if request.method == 'POST':
        formulario = DetalleTrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/dettraslado/'+ idtraslado)

    else:
        formulario = DetalleTrasladoForm(initial={'traslado':idtraslado})


    return render_to_response('Inventario/GestionDetalleTraslado.html',{'idtraslado':idtraslado,'exito':exito,'formulario':formulario,
                                                         'traslado': traslado,'detraslados': detraslados},
                                                        context_instance = RequestContext(request))
def EditaDetalleTraslado(request,idDettraslado):
    det = DetalleTraslado.objects.get(pk = idDettraslado)
    traslado = Traslado.objects.get(pk = det.traslado.codigoTraslado)
    detraslados = DetalleTraslado.objects.filter(traslado = traslado.codigoTraslado)


    if request.method == 'POST':
        formulario = DetalleTrasladoForm(request.POST, instance=det)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/dettraslado/'+ str(traslado.codigoTraslado))

    else:
        formulario = DetalleTrasladoForm(initial={'traslado':traslado.codigoTraslado},instance=det)


    return render_to_response('Inventario/GestionDetalleTraslado.html',{'idtraslado':traslado.codigoTraslado,'formulario':formulario,
                                                         'traslado': traslado,'detraslados': detraslados},
                                                        context_instance = RequestContext(request))
def borrarDetTraslado(request,idDetTraslado):
    #Borra el detalle de los traslados
    detalle = DetalleTraslado.objects.select_related().get(pk = idDetTraslado)
    detalle.delete()
    return HttpResponseRedirect('/inventario/dettraslado/'+ str(detalle.traslado.codigoTraslado))


def GuardarTraslado(request):

    codigoTraslado = request.GET.get('codigoTraslado')
    detalleTraslado = DetalleTraslado.objects.filter(traslado = int(codigoTraslado))
    traslado = Traslado.objects.get(pk = int(codigoTraslado))
    cont = 0

    for detalle in detalleTraslado:

        bodegaOrigen = ProductoBodega.objects.get(bodega = traslado.bodegaActual.codigoBodega,producto = detalle.productoTraslado.codigoProducto)
        bodegaDestino = ProductoBodega.objects.get(bodega__nombreBodega = traslado.bodegaDestino,producto = detalle.productoTraslado.codigoProducto)

        bodegaOrigen.pesoProductoStock -= detalle.pesoTraslado
        bodegaOrigen.unidadesStock -= detalle.unidadesTraslado


        bodegaDestino.pesoProductoStock += detalle.pesoTraslado
        bodegaDestino.unidadesStock += detalle.unidadesTraslado

        movimiento = Movimientos()
        movimiento.tipo = 'TRS%d'%(traslado.codigoTraslado)
        movimiento.productoMov = detalle.productoTraslado
        movimiento.nombreProd = detalle.productoTraslado.nombreProducto
        movimiento.fechaMov = traslado.fechaTraslado
        movimiento.desde = bodegaOrigen.bodega.nombreBodega
        movimiento.Hasta = bodegaDestino.bodega.nombreBodega
        if detalle.pesoTraslado == 0:
            movimiento.entrada = detalle.unidadesTraslado
            movimiento.salida = detalle.unidadesTraslado
        else:
            movimiento.entrada = detalle.pesoTraslado
            movimiento.salida = detalle.pesoTraslado

        movimiento.save()
        bodegaOrigen.save()
        bodegaDestino.save()



        cont += 1
    traslado.guardado = True
    traslado.save()
    exito = 'se guardaron %d registros Exitosamente'%cont

    respuesta = json.dumps(exito)

    return HttpResponse(respuesta,mimetype='application/json')

def consultaStock(request):
    codigoProducto = request.GET.get('producto')
    codigoTraslado = request.GET.get('codigoTraslado')
    traslado = Traslado.objects.get(pk = int(codigoTraslado))

    bodega = ProductoBodega.objects.get(bodega = traslado.bodegaActual,producto = int(codigoProducto))

    pesoTraslado = request.GET.get('pesoTraslado')
    undTraslado =request.GET.get('undTraslado')


    if int(undTraslado) == 0 and int(pesoTraslado) <= bodega.pesoProductoStock:
        msj =''
    elif int(pesoTraslado) == 0 and int(undTraslado) <= bodega.unidadesStock:
        msj =''
    else:
        msj = 'No hay esa cantidad en bodega, ahora hay : %d'%bodega.pesoProductoStock

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionMovimientos (request):
    fechainicio = date.today() - timedelta(days=20)
    fechafin = date.today()
    movimientos = Movimientos.objects.all().filter(fechaMov__range = (fechainicio,fechafin))
    return render_to_response('Inventario/GestionMovimientos.html',{'movimientos':movimientos},
                                                        context_instance = RequestContext(request))

def ComprasProveedor(request):
    provedor = Proveedor.objects.all()
    bodega = Bodega.objects.all()
    return render_to_response('Inventario/CompraProvedor.html',{'provedor':provedor,'bodega':bodega},
                              context_instance = RequestContext(request))

def ReporteCompra(request):
    idProvedor = request.GET.get('provedor')
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

    provedor = Proveedor.objects.get(pk = int(idProvedor))
    bodega = Bodega.objects.get(pk = int(idBodega))

    compras = Compra.objects.filter(fechaCompra__range = (finicio,ffin)).filter(proveedor = provedor.codigoProveedor).filter(bodegaCompra = bodega.codigoBodega)

    respuesta = serializers.serialize('json',compras)


    return HttpResponse(respuesta,mimetype='application/json')


def TemplateReporteFaltantes (request):
    bodegas = Bodega.objects.all()
    hoy = datetime.today()
    usuario = request.user.username
    return render_to_response('Inventario/ReporteFaltantes.html',{'bodegas':bodegas,'hoy':hoy,'usuario':usuario},
                                                        context_instance = RequestContext(request))

def ReporteFaltantes (request):
    idBodega = request.GET.get('bodega')
    bodega = Bodega.objects.get(pk = int(idBodega))

    productoBodega = ProductoBodega.objects.filter(bodega = bodega.codigoBodega).filter(producto__numeroProducto__gt = 0).order_by('producto__numeroProducto')

    respuesta = serializers.serialize('json',productoBodega)
    return HttpResponse(respuesta,mimetype='application/json')

def ConciliaInventario (request):

    datos = request.GET.get('datos')
    datosJson = json.loads(datos)
    for dato in datosJson:

        producto = ProductoBodega.objects.select_related().get(producto = dato['Codigo'],bodega__nombreBodega = dato['Bodega'])
        if producto.producto.pesables:
            producto.pesoProductoStock = Decimal(dato['Fisico'])
        else:
            producto.unidadesStock = int(dato['Fisico'])
        producto.save()
    msj =  'Exito'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def Deshidratacion(request):
    bodega = request.GET.get('bodega')
    cont = 0

    productos = ProductoBodega.objects.filter(bodega = int(bodega),producto__pesables = True)

    for producto in productos:

        if producto.pesoProductoStock > 0:

            pesoProducto = producto.pesoProductoStock
            #Calculo de Deshidratacion
            deshidratacion = (pesoProducto * Decimal(0.8))/100
            pesoAjustado = pesoProducto - Decimal(ceil(deshidratacion))
            producto.pesoProductoStock = pesoAjustado
            producto.save()
            cont += 1

    msj = 'Deshidratacion aplicada correctamente a %d productos'%cont
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def TemplateMovimientos(request):
    productos = Producto.objects.all()
    bodegas = Bodega.objects.all()
    return render_to_response('Inventario/ReporteMovimientos.html',{'productos':productos,'bodegas':bodegas},
                              context_instance = RequestContext(request))

def ReporteMovimientos(request):
    idProducto = request.GET.get('producto')
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
    q1 = ''
    q2 = ''
    respuesta = ''

    if idProducto :
        q1 = Movimientos.objects.filter(fechaMov__range = (finicio,ffin)).filter(productoMov = int(idProducto))
        respuesta = serializers.serialize('json',q1)
    elif idBodega:
        bodega = Bodega.objects.get(pk = int(idBodega))
        q1 = Movimientos.objects.filter(fechaMov__range = (finicio,ffin)).filter(Hasta = bodega.nombreBodega).exclude(tipo__contains = 'VN').order_by('tipo')
        q2 = Movimientos.objects.filter(fechaMov__range = (finicio,ffin)).filter(desde = bodega.nombreBodega).exclude(tipo__contains = 'VN').order_by('tipo')
        respuesta = serializers.serialize('json',q1|q2)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionAjustes(request):
    fechainicio = date.today() - timedelta(days=1)
    fechafin = date.today()
    ajustes = Ajustes.objects.select_related().filter(fechaAjuste__range = (fechainicio,fechafin)).order_by('fechaAjuste')
    if request.method == 'POST':

        formulario = AjustesForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/ajustes')
    else:
        formulario =AjustesForm()

    return render_to_response('Inventario/GestionAjustes.html',{'formulario':formulario,'ajustes':ajustes },
                              context_instance = RequestContext(request))

def GuardarAjuste(request):
    idAjuste = request.GET.get('idAjuste')
    ajuste = Ajustes.objects.get(pk = int(idAjuste))

    bodegaAjuste = ProductoBodega.objects.get(bodega = ajuste.bodegaAjuste.codigoBodega,producto = ajuste.productoAjuste.codigoProducto)

    if ajuste.sumar == True:
        bodegaAjuste.pesoProductoStock += ajuste.pesoAjuste
        bodegaAjuste.unidadesStock += ajuste.unidades
        bodegaAjuste.save()

        movimiento = Movimientos()
        movimiento.tipo = 'AJU%d'%(ajuste.id)
        movimiento.fechaMov = ajuste.fechaAjuste
        movimiento.productoMov = ajuste.productoAjuste
        movimiento.nombreProd = ajuste.productoAjuste.nombreProducto
        if ajuste.pesoAjuste == 0:
            movimiento.entrada = ajuste.unidades
        else:
            movimiento.entrada = ajuste.pesoAjuste
        movimiento.Hasta = ajuste.bodegaAjuste.nombreBodega
        movimiento.save()
    else:
        bodegaAjuste.pesoProductoStock -= ajuste.pesoAjuste
        bodegaAjuste.unidadesStock -= ajuste.unidades
        bodegaAjuste.save()

        movimiento = Movimientos()
        movimiento.tipo = 'AJU%d'%(ajuste.id)
        movimiento.fechaMov = ajuste.fechaAjuste
        movimiento.productoMov = ajuste.productoAjuste
        movimiento.nombreProd = ajuste.productoAjuste.nombreProducto
        if ajuste.pesoAjuste == 0:
            movimiento.salida = ajuste.unidades
        else:
            movimiento.salida = ajuste.pesoAjuste
        movimiento.Hasta = ajuste.bodegaAjuste.nombreBodega
        movimiento.save()

    ajuste.guardado = True
    ajuste.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def CantidadActual(request):
    idProducto = request.GET.get('producto')
    idBodega = request.GET.get('bodega')

    bodega = ProductoBodega.objects.get(bodega = int(idBodega),producto = int(idProducto))
    pesoActual = {}
    undActual = {}

    pesoActual['Peso Actual'] = ceil(bodega.pesoProductoStock)
    undActual['Unidades Actuales'] = bodega.unidadesStock

    lista = {'pesoActual':pesoActual,'undActual':undActual}


    respuesta = json.dumps(lista)

    return HttpResponse(respuesta,mimetype='application/json')

def EditarAjustes(request,idAjuste):
    fechainicio = date.today() - timedelta(days=20)
    fechafin = date.today()
    ajustes = Ajustes.objects.all().order_by('fechaAjuste').filter(fechaAjuste__range = (fechainicio,fechafin))
    ajuste = Ajustes.objects.get(pk = idAjuste)
    if request.method == 'POST':

        formulario = AjustesForm(request.POST,instance=ajuste)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/ajustes')
    else:
        formulario =AjustesForm(instance=ajuste)

    return render_to_response('Inventario/GestionAjustes.html',{'formulario':formulario,'ajustes':ajustes },
                              context_instance = RequestContext(request))



def GestionFaltante(request):
    faltantes = Faltantes.objects.all()
    if request.method == 'POST':
        formulario = FaltanteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/faltante')
    else:
        formulario = FaltanteForm()

    return render_to_response('Inventario/TemplateFaltante.html',{'formulario':formulario,'faltantes':faltantes },
                              context_instance = RequestContext(request))

def GenerarFaltante(request):
    idFaltante = request.GET.get('idFaltante')
    nombreBodega = request.GET.get('nombreBodega')
    bodega = Bodega.objects.get(nombreBodega = nombreBodega)
    faltante = Faltantes.objects.get(pk = int(idFaltante))
    existencias = ProductoBodega.objects.filter(bodega = bodega.codigoBodega).filter(pesoProductoStock__gt = 0)
    existencias2 = ProductoBodega.objects.filter(bodega = bodega.codigoBodega).filter(unidadesStock__gt = 0)
    existencias3 = ProductoBodega.objects.filter(bodega = bodega.codigoBodega).filter(pesoProductoStock__lt = 0)
    existencias4 = ProductoBodega.objects.filter(bodega = bodega.codigoBodega).filter(unidadesStock__lt = 0)

    for existencia in existencias:
        detalleFaltante = DetalleFaltantes()
        detalleFaltante.faltante = faltante
        detalleFaltante.productoFaltante = existencia.producto
        detalleFaltante.pesoActual = existencia.pesoProductoStock
        detalleFaltante.save()

    for existencia in existencias2:
        detalleFaltante = DetalleFaltantes()
        detalleFaltante.faltante = faltante
        detalleFaltante.productoFaltante = existencia.producto
        detalleFaltante.unidadActual = existencia.unidadesStock
        detalleFaltante.save()

    for existencia in existencias3:
        detalleFaltante = DetalleFaltantes()
        detalleFaltante.faltante = faltante
        detalleFaltante.productoFaltante = existencia.producto
        detalleFaltante.pesoActual = existencia.pesoProductoStock
        detalleFaltante.save()

    for existencia in existencias4:
        detalleFaltante = DetalleFaltantes()
        detalleFaltante.faltante = faltante
        detalleFaltante.productoFaltante = existencia.producto
        detalleFaltante.unidadActual = existencia.unidadesStock
        detalleFaltante.save()


    msj = 'Reporte Generado Exitosamente'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionDetalleFaltante(request,idFaltante):
    faltante = Faltantes.objects.get(pk = idFaltante)
    detalleFaltantes = DetalleFaltantes.objects.filter(faltante = idFaltante)

    if request.method == 'POST':
        formulario = DetalleFaltanteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/detalleFaltante'+ idFaltante)
    else:
        formulario = DetalleFaltanteForm()

    return render_to_response('Inventario/TemplateGestionDetalleFaltante.html',{'formulario':formulario,'faltante':faltante,'detalleFaltantes':detalleFaltantes },
                              context_instance = RequestContext(request))

def EditaDetalleFaltante(request,idDetFaltante):
    detFaltante = DetalleFaltantes.objects.get(pk  = idDetFaltante)
    faltante = Faltantes.objects.get(pk = detFaltante.faltante.id)
    detalleFaltantes = DetalleFaltantes.objects.filter(faltante = faltante.id)

    if request.method == 'POST':
        formulario = DetalleFaltanteForm(request.POST,instance=detFaltante)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/detalleFaltante'+ str(faltante.id))
    else:
        formulario = DetalleFaltanteForm(initial={'faltante':faltante.id},instance=detFaltante)

    return render_to_response('Inventario/TemplateGestionDetalleFaltante.html',{'formulario':formulario,'faltante':faltante,'detalleFaltantes':detalleFaltantes },
                              context_instance = RequestContext(request))







