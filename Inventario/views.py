 # -*- coding: UTF-8 -*-
from decimal import Decimal
from math import ceil

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse

#Imports necesarios para el uso de Pisa PDF
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string

from Inventario.Forms.forms import *
from Inventario.models import *

from Fabricacion.Forms import *



# Create your views here.

def listaProvedoresAjax(request):
    provedores = Proveedor.objects.all()
    data = serializers.serialize('json',provedores,fields = ('nit','nombreProv','direccionProv','telefonoProv',
                                                             'email','ciudad'))

    return HttpResponse(data, mimetype='application/json')


def home(request):
    productosBajoStock = ProductoBodega.objects.all().filter(pesoProductoStock__gt = 5000).order_by('bodega')
    costosProductos = Producto.objects.all().order_by('nombreProducto')

    return render_to_response('Home.html',{'productosBajoStock':productosBajoStock,
                                           'costosProductos':costosProductos},context_instance = RequestContext(request))

#***************************************PRODUCTOS******************************************
def listaProductos(request):
    productos = Producto.objects.all().order_by('codigoProducto')

    #se actualiza el precio sugerido del producto
    for producto in productos:
        producto.precioSugerido = ceil(producto.costoProducto / 0.78)
        producto.save()

    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            # insumos o BasicosProcesados solo se grabaran en la bodega de Taller
            if producto.grupo.nombreGrupo == "Insumos" or producto.grupo.nombreGrupo == "Basicos Procesados" or producto.grupo.nombreGrupo == "Verduras":

                bodegaInicial = ProductoBodega()
                bodega = Bodega.objects.get(nombreBodega = 'Taller')

                bodegaInicial.producto = producto
                bodegaInicial.bodega = bodega
                bodegaInicial.pesoProductoStock = 0
                bodegaInicial.unidadesStock = 0
                bodegaInicial.save()

            else:

                for bod in Bodega.objects.all():

                    bodegaInicial = ProductoBodega()
                    bodega = Bodega.objects.get(pk = bod.codigoBodega)

                    bodegaInicial.producto = producto
                    bodegaInicial.bodega = bodega
                    bodegaInicial.pesoProductoStock = 0
                    bodegaInicial.unidadesStock = 0
                    bodegaInicial.save()

            return HttpResponseRedirect('/inventario/listaProd')
    else:
        formulario =ProductoForm()

    return render_to_response('Inventario/GestionProducto.html',{'formulario':formulario,'productos':productos },
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
    if request.method == 'POST':
        formulario = BodegaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
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

    return render_to_response('Inventario/GestionProductoBodega.html',{'productoBodegas':productoBodegas,'producto':producto },
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
        formulario = GanadoForm(initial={'precioKiloEnPie':3150,'compra':idcompra,'piel':'Friana'})

    return render_to_response('Inventario/GestionGanado.html',{'formulario':formulario,'ganados':ganados,'compra':idcompra },
                              context_instance = RequestContext(request))

#**********************************************COMPRA***********************************************************
def GestionCompra(request):

    compras = Compra.objects.all()

    if request.method == 'POST':
        formulario = CompraForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/inventario/compra')
    else:
        formulario =CompraForm()

    return render_to_response('Inventario/GestionCompras.html',{'formulario':formulario,'compras':compras },
                              context_instance = RequestContext(request))

def GestionDetalleCompra(request,idcompra):

    compra = Compra.objects.get(pk = idcompra)
    detcompras = DetalleCompra.objects.filter(compra = idcompra)
    totalCompra  = 0
    for dcmp in detcompras: # clacular los totales de la lista de detalles de subproducto
                totalCompra += dcmp.subtotal

    if request.method == 'POST':
        formulario = DetalleCompraForm(idcompra,request.POST)
        if formulario.is_valid():
            detalleCompra = formulario.save()

            productoBodega = ProductoBodega.objects.get(bodega = 6,producto = detalleCompra.producto.codigoProducto)
            producto = Producto.objects.get(pk = detalleCompra.producto.codigoProducto)

            # Si el producto es un insumo

            if detalleCompra.producto.grupo.id == 6 :

                productoBodega.pesoProductoStock += detalleCompra.pesoProducto
                productoBodega.save()

                producto.costoProducto = detalleCompra.vrCompraProducto
                producto.save()

            # Si el producto es una verdura
            elif detalleCompra.producto.grupo.id == 7:

                productoBodega.pesoProductoStock += 0
                productoBodega.save()

            #Si el producto es para compra venta

            elif detalleCompra.producto.grupo.id == 9:

                productoBodegaCV = ProductoBodega.objects.get(bodega = 5,producto = detalleCompra.producto.codigoProducto)
                productoBodegaCV.pesoProductoStock += detalleCompra.pesoProducto
                productoBodegaCV.save()

            #Si el producto es Basico Procesado
            elif detalleCompra.producto.grupo.id == 8:

                producto.costoProducto = detalleCompra.vrCompraProducto
                producto.save()
                productoBodegaBP = ProductoBodega.objects.get(bodega = 6,producto = detalleCompra.producto.codigoProducto)
                productoBodegaBP.pesoProductoStock += detalleCompra.pesoProducto
                productoBodegaBP.save()

            detcompras = DetalleCompra.objects.filter(compra = idcompra)
            totalCompra  = 0
            for dcmp in detcompras: # clacular los totales de la lista de detalles de subproducto
                totalCompra += dcmp.subtotal

            compra.vrCompra = totalCompra
            compra.save()


            return HttpResponseRedirect('/inventario/detcompra/'+ idcompra)
    else:
        formulario = DetalleCompraForm(idcompra,initial={'compra':idcompra })

    return render_to_response('Inventario/GestionDetalleCompra.html',{'formulario':formulario,
                                                         'compra': compra,
                                                         'detcompras': detcompras, 'totalCompra':totalCompra},
                                                        context_instance = RequestContext(request))
#********************************************TRASLADOS******************************************************
def GestionTraslados(request):
    traslados = Traslado.objects.all().order_by('fechaTraslado')
    if request.method == 'POST':

        formulario = TrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/traslado')
    else:
        formulario =TrasladoForm()

    return render_to_response('Inventario/GestionTraslado.html',{'formulario':formulario,'traslados':traslados },
                              context_instance = RequestContext(request))


def GestionDetalleTraslado(request,idtraslado):

    traslado = Traslado.objects.get(pk = idtraslado)
    detraslados = DetalleTraslado.objects.filter(traslado = idtraslado)

    exito = False

    if request.method == 'POST':
        formulario = DetalleTrasladoForm(request.POST)
        if formulario.is_valid():

            bodegaActual = ProductoBodega.objects.get(bodega = traslado.bodegaActual.codigoBodega,
                                                      producto = request.POST.get('producto'))
            destino = Bodega.objects.get(nombreBodega = traslado.bodegaDestino)
            bodegaDestino = ProductoBodega.objects.get(bodega = destino.codigoBodega,
                                                       producto = request.POST.get('producto'))

            #Verificamos si la cantidad de producto que se traslada no excede las existencias
            if int(request.POST.get('pesoTraslado')) <= bodegaActual.pesoProductoStock :
                formulario.save()
                pesoActualizado = bodegaActual.pesoProductoStock - int(request.POST.get('pesoTraslado'))
                unidadesActualizadas = bodegaActual.unidadesStock - int(request.POST.get('unidadesTraslado'))

                pesoDestinoActualizado = bodegaDestino.pesoProductoStock + int(request.POST.get('pesoTraslado'))
                unidadesDestinoActualizadas = bodegaActual.unidadesStock + int(request.POST.get('unidadesTraslado'))

                #Se extrae de la bodega actual
                bodegaActual.pesoProductoStock = pesoActualizado
                bodegaActual.pesoProductoKilos = pesoActualizado / 1000
                bodegaActual.unidadesStock = unidadesActualizadas
                bodegaActual.save()

                #Se graba en la bodega destino
                bodegaDestino.pesoProductoStock = pesoDestinoActualizado
                bodegaDestino.pesoProductoKilos = pesoDestinoActualizado / 1000
                bodegaDestino.unidadesStock= unidadesDestinoActualizadas
                bodegaDestino.save()

            else:
                exito = True

            return render_to_response('Inventario/GestionDetalleTraslado.html',{'idtraslado':idtraslado,'cantidadActual':bodegaActual,
                                                                                'exito':exito,'formulario':formulario,

                                                                                'traslado': traslado,'detraslados': detraslados},
                                                        context_instance = RequestContext(request))
    else:
        formulario = DetalleTrasladoForm(initial={'traslado':idtraslado})


    return render_to_response('Inventario/GestionDetalleTraslado.html',{'idtraslado':idtraslado,'exito':exito,'formulario':formulario,
                                                         'traslado': traslado,'detraslados': detraslados},
                                                        context_instance = RequestContext(request))



def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def ReporteTraslado(request,idTraslado):
   # Reporte pdf de traslados

    detalleTraslado = DetalleTraslado.objects.filter(traslado = idTraslado)
    traslado = Traslado.objects.get(pk = idTraslado)

    html = render_to_string('Fabricacion/ReporteTraslado.html', {'pagesize':'A4', 'detalleTraslado':detalleTraslado,'traslado':traslado},
                            context_instance=RequestContext(request))
    return generar_pdf(html)
