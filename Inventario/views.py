from decimal import Decimal

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

from Inventario.Forms.forms import *
from Inventario.models import *






# Create your views here.

def home(request):
    return render_to_response('Home.html',{},context_instance = RequestContext(request))

#***************************************PRODUCTOS******************************************

def listaProductos(request):
    productos = Producto.objects.all().order_by('nombreProducto')
    #Creacion de producto en cada bodega con valor inicial


    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            producto = Producto.objects.get(nombreProducto = request.POST.get('nombreProducto'))

            for bod in Bodega.objects.all():

                bodegaInicial = ProductoBodega()
                bodega = Bodega.objects.get(pk = bod.codigoBodega)

                bodegaInicial.producto = producto
                bodegaInicial.bodega = bodega
                bodegaInicial.pesoProductoStock = 0
                bodegaInicial.unidadesStock = 0
                bodegaInicial.save()


            return HttpResponseRedirect('/listaProd')
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
            return HttpResponseRedirect('/listaProd')
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
            return HttpResponseRedirect('/verSubProductos/')
    else:
        formulario =SubProductoForm()

    return render_to_response('Inventario/GestionSubProducto.html',{'formulario':formulario,'subproductos':subproductos },
                              context_instance = RequestContext(request))


def borrarSubproducto(request, idSubproducto):
    subproducto = SubProducto.objects.get(pk=idSubproducto)
    subproducto.delete()

    return  HttpResponseRedirect('/verSubProductos')

def editarSubproducto(request, idSproducto):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    sproducto = SubProducto.objects.get(pk=idSproducto)
    if request.method == 'POST':
        formulario = SubProductoForm(request.POST, instance=sproducto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/verSubProductos')
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
            return HttpResponseRedirect('/addDSprod/'+ id_subproducto)
    else:
        formulario = DetSubProductoForm(initial={'subproducto':id_subproducto})

    return render_to_response('Inventario/GestionDetalleSubProducto.html',{'Tunds':totalUnd,'TPeso':totalPeso,'formulario':formulario,
                                                         'subrpoductos': subrpoductos,
                                                         'desubproductos': desubproductos},
                                                        context_instance = RequestContext(request))

def borrarDetalleSp(request, idDetalle):
    detsubproducto = DetalleSubProducto.objects.get(pk=idDetalle)
    detsubproducto.delete()
    return  HttpResponseRedirect('/verSubProductos')

#**************************************BODEGA****************************************************

def GestionBodega(request):
    bodegas = Bodega.objects.all()
    if request.method == 'POST':
        formulario = BodegaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/bodega')
    else:
        formulario = BodegaForm()

    return render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas },
                              context_instance = RequestContext(request))


def editarBodega(request, idBodega):
    bodegas = Bodega.objects.all()
    bodega = Bodega.objects.get(pk=idBodega)
    if request.method == 'POST':
        formulario = BodegaForm(request.POST, instance=bodega)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/bodega')
    else:
        formulario = BodegaForm(instance=bodega)

    return  render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas},
                               context_instance = RequestContext(request))

def borrarBodega(request,idbodega ):
    bodega = Bodega.objects.get(pk=idbodega)
    bodega.delete()
    return  HttpResponseRedirect('/bodega')

def GestionProductoBodega(request,idproducto):
    productoBodegas = ProductoBodega.objects.filter(producto = idproducto)

    return render_to_response('Inventario/GestionProductoBodega.html',{'productoBodegas':productoBodegas },
                              context_instance = RequestContext(request))

#*****************************************PROVEEDOR**************************************************

def GestionProvedor(request):
    provedores = Proveedor.objects.all()
    if request.method == 'POST':
        formulario = ProvedorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/provedor')
    else:
        formulario = ProvedorForm()

    return render_to_response('Inventario/GestionProvedor.html',{'formulario':formulario,'provedores':provedores },
                              context_instance = RequestContext(request))

#************************************************GANADO*******************************************************

def GestionGanado(request,idcompra):

    ganados = Ganado.objects.order_by('-codigoGanado')
    compra = Compra.objects.get(pk = idcompra)
    detallecompra = DetalleCompra()
    ganado = Ganado()



    if request.method == 'POST':
        formulario = GanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            ganado.codigoGanado = ganados[0].codigoGanado
            ganado.genero = request.POST.get('genero')
            ganado.pesoEnPie = request.POST.get('pesoEnPie')
            ganado.precioKiloEnPie = request.POST.get('precioKiloEnPie')
            ganado.precioTotal = request.POST.get('precioTotal')
            ganado.difPieCanal = request.POST.get('difPieCanal')

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

            compraTotal = Compra(
                                codigoCompra = compra.codigoCompra,
                                encargado = compra.encargado,
                                proveedor = compra.proveedor,
                                fechaCompra = compra.fechaCompra,
                                vrCompra = totalCompra,
                                tipo = compra.tipo
                                )


            compraTotal.save()


            return HttpResponseRedirect('/ganado/'+idcompra)
    else:
        formulario = GanadoForm()

    return render_to_response('Inventario/GestionGanado.html',{'formulario':formulario,'ganados':ganados,'compra':idcompra },
                              context_instance = RequestContext(request))

#**********************************************COMPRA***********************************************************

def GestionCompra(request):

    compras = Compra.objects.all()

    if request.method == 'POST':
        formulario = CompraForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/compra')
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
        formulario = DetalleCompraForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            detcompras = DetalleCompra.objects.filter(compra = idcompra)
            totalCompra  = 0
            for dcmp in detcompras: # clacular los totales de la lista de detalles de subproducto
                totalCompra += dcmp.subtotal

            compraTotal = Compra(
                                codigoCompra = compra.codigoCompra,
                                encargado = compra.encargado,
                                proveedor = compra.proveedor,
                                fechaCompra = compra.fechaCompra,
                                vrCompra = totalCompra )

            compraTotal.save()

            return HttpResponseRedirect('/detcompra/'+ idcompra)
    else:
        formulario = DetalleCompraForm(initial={'compra':idcompra})

    return render_to_response('Inventario/GestionDetalleCompra.html',{'formulario':formulario,
                                                         'compra': compra,
                                                         'detcompras': detcompras, 'totalCompra':totalCompra},
                                                        context_instance = RequestContext(request))

def GestionDesposte(request):
    despostes = PlanillaDesposte.objects.all()

    if request.method == 'POST':

        formulario = DesposteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/desposte/')
    else:
        formulario =DesposteForm()

    return render_to_response('Inventario/GestionDesposte.html',{'formulario':formulario,'despostes':despostes},
                              context_instance = RequestContext(request))

def GestionCanal(request,idganado):
    canal = Canal.objects.filter(ganado = idganado)
    ganado = Ganado.objects.get(pk = idganado)
    compra = DetalleCompra.objects.get(ganado = idganado)
    objCompra = Compra.objects.get(pk = compra.compra.codigoCompra)
    codigoCompra = compra.compra.codigoCompra
    factura = Compra.objects.get(pk = compra.compra.codigoCompra)
    sacrificio = Sacrificio.objects.get(compra = objCompra.codigoCompra)
    detcompra = DetalleCompra.objects.filter(compra = codigoCompra) # variable para conocer la cantidad de reces que se compraron


    detalleCompra = DetalleCompra()


    if request.method == 'POST':
        formulario = CanalForm(request.POST)


        if formulario.is_valid():
            planilla = PlanillaDesposte.objects.get(pk = request.POST.get('planilla'))

            vrKiloCanal = ((factura.vrCompra + sacrificio.vrDeguello + sacrificio.vrTransporte) -
                          (sacrificio.piel + sacrificio.vrMenudo))/ (int(request.POST.get('peosTotalCanal'))*detcompra.count())

            canal = Canal()
            canal.ganado = ganado
            canal.planilla = planilla
            canal.pesoPiernas = request.POST.get('pesoPiernas')
            canal.pesoBrazos = request.POST.get('pesoBrazos')
            canal.peosTotalCanal = request.POST.get('peosTotalCanal')
            canal.vrKiloCanal = vrKiloCanal

            canal.save()

            ganadoUpd = Ganado()

            ganadoUpd.codigoGanado = ganado.codigoGanado

            ganadoUpd.genero=ganado.genero
            ganadoUpd.piel= ganado.piel
            ganadoUpd.pesoEnPie = ganado.pesoEnPie
            ganadoUpd.precioKiloEnPie = ganado.precioKiloEnPie
            ganadoUpd.precioTotal = ganado.precioTotal
            ganadoUpd.difPieCanal = (ganado.pesoEnPie - Decimal(canal.peosTotalCanal))/100
            ganadoUpd.fechaIngreso = ganado.fechaIngreso
            ganadoUpd.save()

            detalleCompra.id = compra.id
            detalleCompra.compra = objCompra
            detalleCompra.ganado = ganado
            detalleCompra.pesoProducto = compra.pesoProducto
            detalleCompra.unidades = compra.unidades
            detalleCompra.vrCompraProducto = compra.vrCompraProducto
            detalleCompra.subtotal = compra.subtotal
            detalleCompra.estado = True
            detalleCompra.save()
            return HttpResponseRedirect('/canal/'+ idganado)
    else:
        formulario = CanalForm(initial={'ganado':idganado})

    return render_to_response('Inventario/GestionCanal.html',{'formulario':formulario,'ganado':ganado,'canal':canal,
                                                              'codigoCompra':codigoCompra},
                              context_instance = RequestContext(request))

def GestionCanalDetalleDesposte(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

    totalReses = canales.count()
    totalDesposte = 0
    totalCanal = 0


    #proceso para guardar todos los productos despostados en la tabla producto.



    for detplanilla in detalleDespostes:
        totalDesposte += detplanilla.PesoProducto
    for canal in canales :
        totalCanal += canal.peosTotalCanal

    totalCanal *= 1000

    #costoCanalDesposte = totalCanal *

    if request.method == 'POST':
        formulario = DetalleDesposteForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            producto = Producto.objects.get(pk = request.POST.get('producto'))
            bodega = Bodega.objects.get(pk = 5)
            bodegaprodID = ProductoBodega.objects.get(bodega = 5,producto = producto.codigoProducto )

            bodegaProducto = ProductoBodega()
            bodegaProducto.id = bodegaprodID.id
            bodegaProducto.producto = producto
            bodegaProducto.bodega = bodega
            bodegaProducto.pesoProductoStock = request.POST.get('PesoProducto')
            bodegaProducto.unidadesStock = 0

            bodegaProducto.save()

            desposte = PlanillaDesposte.objects.get(pk = idplanilla)
            canales = Canal.objects.filter(planilla = idplanilla)
            detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

            totalDesposte = 0
            totalCanal = 0

            for detplanilla in detalleDespostes:
                totalDesposte += detplanilla.PesoProducto

            for canal in canales :
                totalCanal += canal.peosTotalCanal
            totalCanal *= 1000
            difCanalDesposte = (totalCanal - totalDesposte)/totalReses

            desposte = PlanillaDesposte(
                codigoPlanilla = idplanilla,
                fechaDesposte = desposte.fechaDesposte,
                resesADespostar = totalReses,
                totalDespostado = totalDesposte,
                difCanalADespostado = difCanalDesposte
            )

            desposte.save()
            return HttpResponseRedirect('/detalleDesposte/'+ idplanilla)
    else:
        formulario = DetalleDesposteForm(initial={'planilla':idplanilla})

    return render_to_response('Inventario/GestionCanalDetalleDesposte.html',{'formulario':formulario,'desposte':desposte
                                                                            ,'canales':canales,'detalleDespostes':detalleDespostes,
                                                                             'totalCanal':totalCanal,'totalDesposte':totalDesposte},
                              context_instance = RequestContext(request))

#**************************************************** EMPLEADOS ************************************************

def GestionEmpleados(request):

    empleados = Empleado.objects.all()

    if request.method == 'POST':

        formulario = EmpleadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/empleado/')
    else:
        formulario =EmpleadoForm()

    return render_to_response('Inventario/GestionEmpleados.html',{'formulario':formulario,'empleados':empleados },
                              context_instance = RequestContext(request))

def GestionCargos(request):

    cargos = Cargo.objects.all()

    if request.method == 'POST':

        formulario = CargoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/cargo/')
    else:
        formulario = CargoForm()

    return render_to_response('Inventario/Cargo.html',{'formulario':formulario,'cargos':cargos },
                              context_instance = RequestContext(request))

#********************************************TRASLADOS******************************************************
def GestionTraslados(request):
    traslados = Traslado.objects.all()
    if request.method == 'POST':

        formulario = TrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/traslado/')
    else:
        formulario =TrasladoForm()

    return render_to_response('Inventario/GestionTraslado.html',{'formulario':formulario,'traslados':traslados },
                              context_instance = RequestContext(request))


def GestionDetalleTraslado(request,idtraslado):

    traslado = Traslado.objects.get(pk = idtraslado)
    detraslados = DetalleTraslado.objects.filter(traslado = idtraslado)


    if request.method == 'POST':
        formulario = DetalleTrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            bodegaActual = ProductoBodega.objects.get(bodega = traslado.bodegaActual.codigoBodega,
                                                      producto = request.POST.get('producto'))
            destino = Bodega.objects.get(nombreBodega = traslado.bodegaDestino)
            bodegaDestino = ProductoBodega.objects.get(bodega = destino.codigoBodega,
                                                       producto = request.POST.get('producto'))


            producto = Producto.objects.get(pk = request.POST.get('producto'))
            #subproducto = SubProducto.objects.get(pk = request.POST.get('subproducto'))

            pesoActualizado = bodegaActual.pesoProductoStock - int(request.POST.get('pesoPiezasTraslado'))
            unidadesActualizadas = bodegaActual.unidadesStock - int(request.POST.get('unidadesTraslado'))

            pesoDestinoActualizado = bodegaDestino.pesoProductoStock + int(request.POST.get('pesoPiezasTraslado'))
            unidadesDestinoActualizadas = bodegaActual.unidadesStock + int(request.POST.get('unidadesTraslado'))

            bodegaactual = ProductoBodega()
            bodegaactual.bodega = Bodega.objects.get(pk = bodegaActual.bodega.codigoBodega)
            bodegaactual.id = bodegaActual.id
            bodegaactual.producto = producto
            bodegaactual.pesoProductoStock = pesoActualizado
            bodegaactual.pesoProductoKilos = pesoActualizado / 1000
            bodegaactual.unidadesStock = unidadesActualizadas

            bodegaactual.save()

            bodegadestino = ProductoBodega()
            bodegadestino.id = bodegaDestino.id
            bodegadestino.bodega = Bodega.objects.get(pk = bodegaDestino.bodega.codigoBodega)
            bodegadestino.producto = producto
            bodegadestino.pesoProductoKilos = pesoDestinoActualizado / 1000
            bodegadestino.pesoProductoStock = pesoDestinoActualizado
            bodegadestino.unidadesStock = unidadesDestinoActualizadas


            bodegadestino.save()

            return HttpResponseRedirect('/dettraslado/'+ idtraslado)
    else:
        formulario = DetalleTrasladoForm(initial={'traslado':idtraslado})


    return render_to_response('Inventario/GestionDetalleTraslado.html',{'formulario':formulario,
                                                         'traslado': traslado,
                                                         'detraslados': detraslados},
                                                        context_instance = RequestContext(request))


def GestionSacrificio(request,idcompra):
    sacrificios = Sacrificio.objects.all()
    detalleCompra = DetalleCompra.objects.filter(compra = idcompra)
    compraActual = Compra.objects.get(pk = idcompra)

    totalpiel = 0

    for detcompra in detalleCompra:#Total pieles de ganados en compra
        ganado = Ganado.objects.get(pk = detcompra.ganado.codigoGanado)
        totalpiel += ganado.piel



    if request.method == 'POST':
        formSacrificio = SacrificioForm(request.POST)

        if formSacrificio.is_valid():


            menudo = detalleCompra.count() * int(request.POST.get('vrMenudo'))
            deguello = detalleCompra.count() * int(request.POST.get('vrDeguello'))
            transporte = detalleCompra.count() * int(request.POST.get('vrTransporte'))
            sacrificio = Sacrificio()

            compra = Compra.objects.get(pk = idcompra)

            sacrificio.compra = compra
            sacrificio.piel = totalpiel
            sacrificio.vrMenudo = menudo
            sacrificio.vrDeguello = deguello
            sacrificio.vrTransporte = transporte
            sacrificio.cantReses = detalleCompra.count()
            sacrificio.cola = request.POST.get('cola')
            sacrificio.rinones = request.POST.get('rinones')
            sacrificio.creadillas = request.POST.get('creadillas')
            sacrificio.recortes = request.POST.get('recortes')
            sacrificio.desecho= request.POST.get('desecho')

            sacrificio.save()

            return HttpResponseRedirect('/sacrificio/'+idcompra)

    else:
        formSacrificio = SacrificioForm(initial={'compra':idcompra})


    return render_to_response('Inventario/GestionSacrificio.html',{'formSacrificio':formSacrificio,
                                                                   'sacrificios':sacrificios,
                                                                   'compraActual':compraActual },
                              context_instance = RequestContext(request))
