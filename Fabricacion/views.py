 # -*- coding: UTF-8 -*-
from decimal import Decimal
from math import ceil
from django.db.models import Avg
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View,TemplateView

import json
from Inventario.Forms.forms import *
from Fabricacion.Forms import *
from Fabricacion.models import *
from Inventario.models import *




#******************************************************CANAL***********************************************************
def GestionCanal(request,idrecepcion):

    canales = Canal.objects.filter(recepcion = idrecepcion).order_by('nroCanal')#para renderizar las listas
    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    compra = Compra.objects.get(pk = recepcion.compra.codigoCompra)
    sacrificio = Sacrificio.objects.get(recepcion = idrecepcion)
    cantidad = canales.count() +1
    kiloCanal = 0
    nroCanal = 0 #Representa el numero de canal actual
    for can in canales :
        kiloCanal = can.vrKiloCanal
        nroCanal = can.nroCanal

    recepcion.vrKiloCanal = kiloCanal
    recepcion.save()


    if request.method == 'POST':
        formulario = CanalForm(request.POST)


        if formulario.is_valid():

            #planilla = PlanillaDesposte.objects.get(pk = request.POST.get('planilla'))
            #canalesPlanilla = Canal.objects.filter(planilla = planilla.codigoPlanilla)# Canales por planilla
            pesoCanales = 0
            pesoPie = 0
            vrFactura = 0

            for canale in canales:
                    pesoCanales += canale.pesoPorkilandia

            canal = Canal()
            canal.recepcion = recepcion
            #canal.planilla = planilla
            canal.pesoFrigovito = request.POST.get('pesoFrigovito')
            canal.pesoPorkilandia = request.POST.get('pesoPorkilandia')
            canal.difPesos = request.POST.get('difPesos')
            canal.genero = request.POST.get('genero')
            canal.nroCanal = request.POST.get('nroCanal')

            if compra.tipo.nombreGrupo == 'Reses':

                vrKiloCanal = ((compra.vrCompra + sacrificio.vrDeguello + sacrificio.vrTransporte) -
                          (sacrificio.piel + sacrificio.vrMenudo))/ (pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))

                vrArrobaCanal = vrKiloCanal * Decimal(12.5)

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal
                vrFactura = compra.vrCompra

                transporte = sacrificio.vrTransporte

            elif compra.tipo.nombreGrupo == 'Cerdos':

                menudo = 7000 * cantidad
                flete = 500000
                transporte = sacrificio.vrTransporte * cantidad
                deguello = 37000 * cantidad

                if pesoCanales == 0:#para cuando se ingresa la primera vez
                    pesoCanales = 1000


                pesoPorkilandia = Decimal(request.POST.get('pesoPorkilandia'))

                vrFactura = (pesoCanales + pesoPorkilandia) * 6950 #--> 6050 es el valor establecido por granjas el paraiso
                pesoPie = Decimal(ceil(pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))) / (Decimal(0.82))
                #KiloPie = vrFactPie / pesoPie
                vrFactPie = (vrFactura - deguello - flete) + menudo
                costoCanales = (vrFactPie + deguello + flete + transporte) - menudo
                vrKiloCanal = ceil(costoCanales / (pesoCanales + pesoPorkilandia))
                vrArrobaCanal = vrKiloCanal * 12.5

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal

                encargado = Empleado.objects.get(pk = compra.encargado.codigoEmpleado)
                provedor = Proveedor.objects.get(pk = compra.proveedor.codigoProveedor)


            else:
                menudo = 12000 * cantidad
                transporte = 7000* cantidad
                deguello = 48200 * cantidad
                pesoPorkilandia = Decimal(request.POST.get('pesoPorkilandia'))
                cantidadCanalCerdasGrandes = Canal.objects.filter(recepcion = idrecepcion,pesoPorkilandia__gte = 200)# busca registros que el peso sea mayor o igual a 150
                cantidadCanalCerdasChicas = Canal.objects.filter(recepcion = idrecepcion,pesoPorkilandia__lte = 199)# busca registros que el peso sea menor o igual a 150

                incrementoCG = 35 * cantidadCanalCerdasGrandes.count()
                incrementoCP = 32 * cantidadCanalCerdasChicas.count()

                if pesoPorkilandia >= 200:
                    incrementoCG += 35
                else:
                    incrementoCP += 32


                if pesoCanales == 0:#para cuando se ingresa la primera vez
                    pesoCanales = 1000



                pesoPie = pesoCanales + pesoPorkilandia + incrementoCG + incrementoCP
                vrFactura = pesoPie * ValoresCostos.objects.get(nombreCosto = 'Costos Cerdas').valorKiloPie
                 #--> 4400 es el valor establecido por granjas el paraiso
                costoCanales = (vrFactura + deguello + transporte) - menudo
                vrKiloCanal = ceil(costoCanales / (pesoCanales + pesoPorkilandia))
                vrArrobaCanal = vrKiloCanal * 12.5

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal

            #Se ggraba el vr del transporte
            recepcion.vrTransporte = transporte

            #se graba el valor de la factura
            compra.vrCompra = vrFactura
            compra.save()
            # se guarda el canal
            canal.save()

            # Se guarda informacion adicional en el modelo recepcion

            PesoTotalCanales = 0
            TotalPesoPie = 0
            canal = Canal.objects.filter(recepcion = idrecepcion)
            detCompra = DetalleCompra.objects.filter(compra = compra.codigoCompra)


            if recepcion.tipoGanado == 'Mayor':
                for det in detCompra:
                    ganado = Ganado.objects.get(pk = det.ganado.codigoGanado)
                    TotalPesoPie += ganado.pesoEnPie
            else:
                TotalPesoPie = pesoPie


            for cnl in canal:
                PesoTotalCanales += cnl.pesoPorkilandia


            recepcion.difPieCanal = ceil(((Decimal(TotalPesoPie) - PesoTotalCanales)*100)/Decimal(TotalPesoPie))
            recepcion.pesoCanales = PesoTotalCanales
            recepcion.cantCabezas = cantidad
            recepcion.save()


            return HttpResponseRedirect('/fabricacion/canal/'+ idrecepcion)
    else:
        formulario = CanalForm(initial={'recepcion':idrecepcion,'nroCanal':nroCanal + 1})

    return render_to_response('Fabricacion/GestionCanal.html',{'formulario':formulario,'canales':canales,'recepcion':recepcion},
                              context_instance = RequestContext(request))


def MarcarCanalDesposte(request, idcanal):

    canal = Canal.objects.get(pk=idcanal)
    recepcion = PlanillaRecepcion.objects.get(pk = canal.recepcion.codigoRecepcion)
    canales = Canal.objects.filter(recepcion = recepcion.codigoRecepcion)

    if request.method == 'POST':
        formulario = CanalForm(request.POST,instance=canal)
        if formulario.is_valid():

            formulario.save()
            return HttpResponseRedirect('/fabricacion/canal/'+ str(recepcion.codigoRecepcion))
    else:
        formulario = CanalForm(initial={'estado':True},instance=canal)

    return render_to_response('Fabricacion/GestionCanal.html',{'formulario':formulario,'canales':canales,'recepcion':recepcion},
                              context_instance = RequestContext(request))


def GestionSacrificio(request,idrecepcion):

    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    sacrificios = Sacrificio.objects.filter(recepcion = idrecepcion)
    detCompra = DetalleCompra.objects.filter(compra = recepcion.compra.codigoCompra)

    totalPieles = 0

    for det in detCompra:
        ganado = Ganado.objects.get(pk = det.ganado.codigoGanado)
        totalPieles += ganado.piel


    if request.method == 'POST':
        formSacrificio = SacrificioForm(request.POST)

        if formSacrificio.is_valid():
            sacrificio = formSacrificio.save()

            cantCabezas = recepcion.cantCabezas

            menudo = cantCabezas * 90000
            deguello = cantCabezas * 82800
            if recepcion.transporte == 'Particular':
                transporte = 0
            else:
                transporte = cantCabezas * 8000

            sacrificio.recepcion = recepcion
            sacrificio.piel = totalPieles
            sacrificio.vrMenudo = menudo
            sacrificio.vrDeguello = deguello
            sacrificio.vrTransporte = transporte
            sacrificio.save()

            prodLimpieza = ['Cola','Rinones','Creadillas','Recortes Sacrificio','Ubre' ]
            item = ['cola','rinones','creadillas','recortes','ubre' ]
            cont = 0

            for productos  in prodLimpieza:

                producto = Producto.objects.get(nombreProducto = productos )
                existencia = ProductoBodega.objects.get(producto = producto.codigoProducto , bodega = 5)

                existencia.producto = producto
                existencia.pesoProductoStock += existencia.pesoProductoStock + Decimal(request.POST.get(item[cont]))
                existencia.save()

                cont +=1


            return HttpResponseRedirect('/fabricacion/sacrificio/'+idrecepcion)

    else:
        formSacrificio = SacrificioForm(initial={'recepcion':idrecepcion})


    return render_to_response('Fabricacion/GestionSacrificio.html',{'formSacrificio':formSacrificio,
                                                                   'sacrificios':sacrificios},
                              context_instance = RequestContext(request))

def GestionEnsalinado(request):
    ensalinados = Ensalinado.objects.all()
    if request.method == 'POST':
        formulario = EnsalinadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/ensalinados/')
    else:
        formulario = EnsalinadoForm()

    return render_to_response('Fabricacion/GestionEnsalinados.html',{'formulario':formulario,'ensalinados':ensalinados },
                              context_instance = RequestContext(request))

def EditaEnsalinado(request,idEnsalinado):

    ensalinados = Ensalinado.objects.all()
    ensalinado = Ensalinado.objects.get(pk = idEnsalinado)


    if request.method == 'POST':
        formulario = EnsalinadoForm(request.POST,instance=ensalinado)

        if formulario.is_valid():
            formulario.save()
            ensalinado.estado = True
            ensalinado.save()
            return HttpResponseRedirect('/fabricacion/ensalinados/')
    else:
        formulario = EnsalinadoForm(instance=ensalinado)

    return render_to_response('Fabricacion/GestionEnsalinados.html',{'formulario':formulario,'ensalinados':ensalinados },
                              context_instance = RequestContext(request))

def GuardaEnsalinado(request):

    idEnsalinado = request.GET.get('idEnsalinado')
    ensalinado = Ensalinado.objects.get(pk = int(idEnsalinado))
    sal = Producto.objects.get(nombreProducto = 'Sal')
    papaina = Producto.objects.get(nombreProducto = 'Papaina')

    salBodega = ProductoBodega.objects.get(bodega = 6 , producto__nombreProducto = 'Sal')
    PapainaBodega = ProductoBodega.objects.get(bodega = 6 , producto__nombreProducto = 'Papaina')

    producto = Producto.objects.get(nombreProducto = ensalinado.productoEnsalinado.nombreProducto)

    costoSal = (ensalinado.pesoSal/ 1000) * sal.costoProducto
    costoPapaina = (ensalinado.pesoPapaina / 1000) * papaina.costoProducto
    costoProductoEnsalinado = (ensalinado.pesoProducto / 1000) * producto.costoProducto
    costoInsumos = costoSal + costoPapaina + costoProductoEnsalinado
    #cif = 30 * (ensalinado.pesoProductoDespues / 1000)
    mod = ensalinado.mod
    costoTotal = mod + costoInsumos
    costoKilo = ceil(costoTotal / (ensalinado.pesoProductoDespues /1000))

    ensalinado.costoTotal = costoTotal
    ensalinado.costoKilo = costoKilo
    ensalinado.guardado = True
    ensalinado.save()

    # se guarda en el Producto el Costo del Kilo
    piernaEnsalinada = Producto.objects.get(nombreProducto = 'Pierna Ensalinada')
    piernaEnsalinada.costoProducto = costoKilo
    piernaEnsalinada.save()

    #Se guarda la cantidad final en la bodega de taller
    bodegaEnsalinado = ProductoBodega.objects.get(bodega = 6,producto = piernaEnsalinada.codigoProducto)
    bodegaEnsalinado.pesoProductoStock += ensalinado.pesoProductoDespues
    bodegaEnsalinado.save()

    #se resta la cantidad de Carne que se utilizo para el ensalinado
    bodegaProductoAntes = ProductoBodega.objects.get(bodega = 6, producto = producto.codigoProducto)
    bodegaProductoAntes.pesoProductoStock -= ensalinado.pesoProductoAntes
    bodegaProductoAntes.save()


    #Se guarda la cantidad a restar para la sal

    salBodega.pesoProductoStock -= ensalinado.pesoSal
    salBodega.save()

    #Se guarda la cantidad a restar para la Papaina

    PapainaBodega.pesoProductoStock -= ensalinado.pesoPapaina
    PapainaBodega.save()

    respuesta = json.dumps('Guardado Exitoso!!')
    return HttpResponse(respuesta,mimetype='application/json')

def GestionVerduras(request,idDetcompra):
    detalleCompra = DetalleCompra.objects.get(pk = idDetcompra)
    verduras = LimpiezaVerduras.objects.filter(compra = detalleCompra.id )
    compra = Compra.objects.get(pk = detalleCompra.compra.codigoCompra)
    producto = Producto.objects.get(pk = detalleCompra.producto.codigoProducto)
    detalles = DetalleCompra.objects.filter(compra = compra.codigoCompra)

    pesoDetalle = 0

    for detalle in detalles:
        pesoDetalle += detalle.pesoProducto

    if request.method == 'POST':

        formulario = LimpiezaVerdurasForm(request.POST)
        if formulario.is_valid():
            verdura = formulario.save()

            #Calculo del costo de la verdura limpia

            vrCompra = detalleCompra.subtotal
            porcentajeTransporte = ((detalleCompra.pesoProducto * 100) /pesoDetalle)/100
            transporte = compra.vrTransporte * porcentajeTransporte
            mod = verdura.mod
            cif = verdura.cif
            costo = vrCompra + cif + mod + transporte
            costoKilo = ceil(costo / (verdura.pesoProducto / 1000 ))

            #Se guarda el costo de la verdura limpia
            verdura.vrKilo = costoKilo
            verdura.save()

            #guardamos el producto en Bodega

            bodegaProducto = ProductoBodega.objects.get(bodega = 6 , producto = producto.codigoProducto )
            bodegaProducto.pesoProductoStock += verdura.pesoProducto
            bodegaProducto.pesoProductoKilos = bodegaProducto.pesoProductoStock / 1000
            bodegaProducto.save()

            #guardamos el costo del producto

            producto.costoProducto = costoKilo
            producto.save()

            # se cambia el estado a verdadero para producto Limpio!!!
            detalleCompra.estado = True
            detalleCompra.save()


            return HttpResponseRedirect('/fabricacion/verduras/'+ idDetcompra)
    else:
        formulario = LimpiezaVerdurasForm(initial={'compra':idDetcompra,'producto': detalleCompra.producto.codigoProducto})

    return render_to_response('Fabricacion/GestionVerduras.html',{'formulario':formulario,'verduras':verduras,
                                                                 'compra':detalleCompra.compra.codigoCompra },
                              context_instance = RequestContext(request))

def GestionCondimento(request):
    condimentos  = Condimento.objects.all()

    if request.method == 'POST':

        formulario = CondimentoForm(request.POST)
        if formulario.is_valid():
            condimento = formulario.save()

            #Guardamos el condimento producido en Bodega
            bodega = ProductoBodega.objects.get(bodega = 6, producto__nombreProducto = 'Condimento Natural')
            bodega.pesoProductoStock += condimento.pesoCondimento
            bodega.save()

            #guardamos el peso de producto en Kg ya que al ingresar este se especifica en gramos
            condimento.pesoCondimento = (condimento.pesoCondimento / 1000)
            condimento.save()

            return HttpResponseRedirect('/fabricacion/condimento/')
    else:
        formulario = CondimentoForm()

    return render_to_response('Fabricacion/GestionCondimento.html',{'formulario':formulario,'condimentos':condimentos },
                              context_instance = RequestContext(request))

def GestionDetalleCondimento(request,idcondimento):
    condimento = Condimento.objects.get(pk = idcondimento)
    detalleCondimentos = DetalleCondimento.objects.filter(condimento = idcondimento)

    if request.method == 'POST':

        formulario = DetalleCondimentoForm(request.POST)
        if formulario.is_valid():
            detalle = formulario.save()

            producto = Producto.objects.get(pk = detalle.productoCondimento.codigoProducto)
            costoProducto = producto.costoProducto
            costoTotalVerduras =(condimento.cantFormulas * costoProducto )* (detalle.pesoProducto/1000)

            # Se resta la cantidad de producrto utilizado en las formulas de condimento y se graba el registro
            bodega = ProductoBodega.objects.get(bodega = 6, producto = detalle.productoCondimento.codigoProducto)
            bodega.pesoProductoStock -= (detalle.pesoProducto * condimento.cantFormulas)
            bodega.save()

            detalle.costoProducto = costoProducto
            detalle.costoTotalProducto = costoTotalVerduras
            detalle.pesoProducto /= 1000

            detalle.save()



            return HttpResponseRedirect('/fabricacion/detallecondimento/'+ idcondimento)
    else:
        formulario = DetalleCondimentoForm(initial={'condimento':idcondimento})

    return render_to_response('Fabricacion/GestionDetalleCondimento.html',{'formulario':formulario,
                                                                   'condimento': condimento,'idcondimento':idcondimento,
                                                                   'detalleCondimentos':detalleCondimentos },
                              context_instance = RequestContext(request))

def CostoCondimento(request,idcondimento):

    condimento = Condimento.objects.get(pk = idcondimento)
    detalleCondimentos = DetalleCondimento.objects.filter(condimento = idcondimento)
    formulario = DetalleCondimentoForm(initial={'condimento':idcondimento})

    pesoCondProcesado = condimento.pesoCondimento
    costoVerduras = 0

    for costo in detalleCondimentos:
        costoVerduras += costo.costoTotalProducto

    mod = condimento.mod
    cif = condimento.cif
    costoCondProsecesado = costoVerduras + cif + mod
    costoLitroCond = ceil(costoCondProsecesado/ pesoCondProcesado)

    #Se graban todos los calculos realizados

    condimento.costoLitroCondimento = costoLitroCond
    condimento.costoCondimento = ceil(costoCondProsecesado)

    condimento.save()

    producto = Producto.objects.get(nombreProducto = 'Condimento Natural')
    producto.costoProducto = costoLitroCond
    producto.save()



    return render_to_response('Fabricacion/GestionDetalleCondimento.html',{'formulario':formulario,
                                                                   'condimento': condimento,'idcondimento':idcondimento,
                                                                   'detalleCondimentos':detalleCondimentos },
                              context_instance = RequestContext(request))



#*********************************************************** MIGA*******************************************************

def GestionMiga(request):
    migas  = Miga.objects.all()

    if request.method == 'POST':

        formulario = MigaForm(request.POST)
        if formulario.is_valid():
            miga = formulario.save()

            #Guardamos la cantidad de producto procesado en la bodega de planta de procesos
            bodegaMiga = ProductoBodega.objects.get(bodega = 6, producto__nombreProducto = 'Miga Preparada' )
            bodegaMiga.pesoProductoStock += miga.PesoFormulaMiga
            bodegaMiga.save()

            miga.PesoFormulaMiga /= 1000
            miga.save()

            return HttpResponseRedirect('/fabricacion/miga')
    else:
        formulario = MigaForm()

    return render_to_response('Fabricacion/GestionMiga.html',{'formulario':formulario,'migas':migas },
                              context_instance = RequestContext(request))

def GestionDetalleMiga(request,idmiga):
    miga = Miga.objects.get(pk = idmiga)
    detallesMiga = DetalleMiga.objects.filter(miga = idmiga)

    if request.method == 'POST':

        formulario = DetalleMigaForm(request.POST)
        if formulario.is_valid():
            detalle =  formulario.save()

            producto = Producto.objects.get(pk = detalle.productoMiga.codigoProducto)
            costoProducto = producto.costoProducto
            costoTotalmiga = (miga.cantidadFormulas * costoProducto )* (detalle.PesoProducto/1000)

            # Se resta la cantidad de producrto utilizado en las formulas de condimento y se graba el registro
            bodega = ProductoBodega.objects.get(bodega = 6, producto = detalle.productoMiga.codigoProducto)
            bodega.pesoProductoStock -= (detalle.PesoProducto * miga.cantidadFormulas)
            bodega.save()

            detalle.costoProducto = costoProducto
            detalle.costoTotalProducto = costoTotalmiga
            detalle.PesoProducto /= 1000
            detalle.save()


            return HttpResponseRedirect('/fabricacion/detallemiga/'+ idmiga)
    else:
        formulario = DetalleMigaForm(initial={'miga':idmiga})

    return render_to_response('Fabricacion/GestionDetalleMiga.html',{'formulario':formulario,'miga':miga,
                                                                           'detallesMiga':detallesMiga,'idmiga':idmiga },
                              context_instance = RequestContext(request))

def CostoMiga(request,idmiga):

    miga = Miga.objects.get(pk = idmiga)
    detallesMiga = DetalleMiga.objects.filter(miga = idmiga)
    formulario = DetalleMigaForm(initial={'miga':idmiga})

    pesoMigaProcesada = miga.PesoFormulaMiga / 1000
    costoInsumos = 0

    for costo in detallesMiga:
        costoInsumos += costo.costoTotalProducto

    mod = miga.mod
    cif = miga.cif
    costomigaProsecesada = costoInsumos + cif + mod
    costoKiloMiga = ceil(costomigaProsecesada/ pesoMigaProcesada)

    #Se graban todos los calculos realizados

    miga.costoKiloMigaProcesada = costoKiloMiga
    miga.costoFormulaMiga = ceil(costomigaProsecesada)
    miga.save()

    producto = Producto.objects.get(nombreProducto = 'Miga Preparada')
    producto.costoProducto = costoKiloMiga
    producto.save()

    return render_to_response('Fabricacion/GestionDetalleMiga.html',{'formulario':formulario,
                                                                   'miga': miga,'idmiga':idmiga,
                                                                   'detallesMiga':detallesMiga },
                              context_instance = RequestContext(request))

def existencias(request):
    # Metodo que verifica las existencias de un producto determinado
    idProducto = request.GET.get('producto')
    idBodega = request.GET.get('bodega')
    peso = request.GET.get('peso')

    bodega = ProductoBodega.objects.get(bodega =  int(idBodega),producto = int(idProducto))

    if Decimal(peso) <= bodega.pesoProductoStock:
        msj = ''
    else:
        msj = 'No se puede usar esa cantidad ; La cantidad disponible de %s es: %s' % (bodega.producto.nombreProducto,str(bodega.pesoProductoStock))

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionApanado(request):
    apanados = ProcesoApanado.objects.all()

    if request.method == 'POST':
        formulario = ApanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/apanados')
    else:
        formulario = ApanadoForm()

    return render_to_response('Fabricacion/GestionApanado.html',{'formulario':formulario,'apanados':apanados },
                              context_instance = RequestContext(request))
def GuardarApanado(request):

    idApanado = request.GET.get('idApanado')
    apanado = ProcesoApanado.objects.get(pk = int(idApanado))
    Filete = Producto.objects.get(pk = apanado.productoApanado.codigoProducto)

    bodegaFilete = ProductoBodega.objects.get(bodega = 5,producto = Filete.codigoProducto)
    bodegaMiga = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Miga Preparada')
    bodegaHuevos = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Huevos')
    bodegaFileteApanadoCerdo = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Filete Apanado Cerdo')
    bodegaFileteApanadoPollo = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Filete Apanado Pollo')

    #guardamos las cantidades utilizadas de cada producto
    bodegaFilete.pesoProductoStock -= apanado.pesoFilete
    bodegaMiga.pesoProductoStock -= apanado.miga
    bodegaHuevos.pesoProductoStock -= apanado.huevos

    #guardamos las cantidades de producto resultante
    if apanado.productoApanado.grupo.nombreGrupo == 'Cerdos' or apanado.productoApanado.grupo.nombreGrupo == 'Cerdas':
        bodegaFileteApanadoCerdo.pesoProductoStock += apanado.totalApanado
        bodegaFileteApanadoCerdo.save()
    else:
         bodegaFileteApanadoPollo.pesoProductoStock += apanado.totalApanado
         bodegaFileteApanadoPollo.save()

    bodegaFilete.save()
    bodegaMiga.save()
    bodegaHuevos.save()

    apanado.guardado =True
    apanado.save()

    msj = 'Guardado Exitoso!!'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')


def costeoApanado(request):
    idApanado = request.GET.get('idApanado')
    apanado = ProcesoApanado.objects.get(pk = int(idApanado))
    msj = ''
    # traemos todos los datos necsarios para el costeo

    Filete = Producto.objects.get(pk = apanado.productoApanado.codigoProducto)
    FileteApanadoCerdo = Producto.objects.get(nombreProducto = 'Filete Apanado Cerdo')
    FileteApanadoPollo = Producto.objects.get(nombreProducto = 'Filete Apanado Pollo')
    miga = Producto.objects.get(nombreProducto = 'Miga Preparada')
    Huevos = Producto.objects.get(nombreProducto = 'Huevos')
    pesoFilete = apanado.pesoFilete
    pesoMiga = apanado.miga
    cantHuevos = apanado.huevos
    costoFilete = Filete.costoProducto
    costoMiga = miga.costoProducto
    costoHuevos = Huevos.codigoProducto
    pesoApanado = apanado.totalApanado / 1000
    # se totaliza el costo de los insumos
    CostoTotalFilete = costoFilete * (pesoFilete / 1000)
    CostoTotalMiga = costoMiga * (pesoMiga / 1000)
    CostoTotalHuevos = costoHuevos * cantHuevos

    # se guarda el costo del kilo en el producto terminado

    if apanado.productoApanado.grupo.nombreGrupo == 'Cerdos' or apanado.productoApanado.grupo.nombreGrupo == 'Cerdas':
        mod = apanado.mod
        cif = apanado.cif
        CostoKiloApanado = (mod + cif + CostoTotalFilete + CostoTotalMiga + CostoTotalHuevos) / pesoApanado
        FileteApanadoCerdo.costoProducto = CostoKiloApanado
        FileteApanadoCerdo.save()
        msj = '!Costeo Exitoso¡'


    else:
        mod = apanado.mod
        cif = apanado.cif
        CostoKiloApanado = (mod + cif + CostoTotalFilete + CostoTotalMiga + CostoTotalHuevos) / pesoApanado
        FileteApanadoPollo.costoProducto = CostoKiloApanado
        FileteApanadoPollo.save()
        msj = '!Costeo Exitoso¡'

    apanado.costoKiloApanado = CostoKiloApanado
    apanado.save()

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionMolido(request):
    molidos = Molida.objects.all()

    if request.method == 'POST':
        formulario = MolidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/molida')
    else:
        formulario = MolidoForm()

    return render_to_response('Fabricacion/GestionMolida.html',{'formulario':formulario,'molidos':molidos },
                              context_instance = RequestContext(request))
def GuardarMolido(request):
    idMolido = request.GET.get('idMolido')
    molido = Molida.objects.get(pk = int(idMolido))
    bodegaProductoAMoler = ProductoBodega.objects.get(bodega = 5,producto = molido.productoMolido.codigoProducto)
    bodegaProductoMolido = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Carne Molida')

    bodegaProductoAMoler.pesoProductoStock -= molido.pesoAmoler
    bodegaProductoMolido.pesoProductoStock += molido.totalMolido

    bodegaProductoAMoler.save()
    bodegaProductoMolido.save()

    molido.guardado = True
    molido.save()

    msj = 'Guardado Exitoso'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')


def costeoMolido(request):
    idMolido = request.GET.get('idMolido')
    molido = Molida.objects.get(pk = int(idMolido))
    mod = molido.mod
    cif = molido.cif
    productoAMoler = Producto.objects.get(pk = molido.productoMolido.codigoProducto)
    carneMolida = Producto.objects.get(nombreProducto = 'Carne Molida')

    costoProducto = (molido.pesoAmoler / 1000) * productoAMoler.costoProducto
    costoTotal = costoProducto + cif + mod
    costoKiloMolida = costoTotal / (molido.totalMolido / 1000)

    carneMolida.costoProducto = costoKiloMolida
    carneMolida.save()
    molido.costoKilo = productoAMoler.costoProducto
    molido.costoKiloMolido = costoKiloMolida
    molido.save()
    msj = 'Costeo Exitoso'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

#**********************************************PROCESO CONDIMENTADO*****************************************************

def GestionCondimentado(request):
    condimentados = Condimentado.objects.all()
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    if request.method == 'POST':
        formulario = CondimentadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/condimentado')
    else:
        formulario = CondimentadoForm(initial={'costoCondimento':condimento.costoProducto})

    return render_to_response('Fabricacion/GestionCondimentado.html',{'formulario':formulario,'condimentados':condimentados },
                              context_instance = RequestContext(request))

def GuardarCondimentado(request):
    idCondimentado = request.GET.get('idCondimentado')
    condimentado = Condimentado.objects.get(pk = int(idCondimentado))
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    #productos a restar
    producto = Producto.objects.get(pk = condimentado.producto.codigoProducto)
    bodegaFilete = ProductoBodega.objects.get(bodega = 6, producto = producto.codigoProducto)
    bodegaFilete.pesoProductoStock -= condimentado.pesoACondimentar
    bodegaFilete.save()

    bodegaCondimento = ProductoBodega.objects.get(bodega = 6,producto = condimento.codigoProducto)
    bodegaCondimento.pesoProductoStock -= condimentado.condimento
    bodegaCondimento.save()

            #guardamos las cantidades producidas
    if condimentado.producto.grupo.nombreGrupo == 'Pollos':
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de Pollo Condimentado')
        FileteCondimentado.costoProducto = condimentado.costoFileteCond
        bodegaFileteCond = ProductoBodega.objects.get(bodega = 5,producto = FileteCondimentado.codigoProducto)
        bodegaFileteCond.pesoProductoStock += condimentado.pesoFileteCond
        bodegaFileteCond.save()
        msj ='Guardado exitoso!!'

    elif condimentado.producto.grupo.nombreGrupo == 'Cerdos':
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de cerdo Condimentado')
        FileteCondimentado.costoProducto = condimentado.costoFileteCond
        bodegaFileteCond = ProductoBodega.objects.get(bodega = 5,producto = FileteCondimentado.codigoProducto)
        bodegaFileteCond.pesoProductoStock += condimentado.pesoFileteCond
        bodegaFileteCond.save()
        msj ='Guardado exitoso!!'

    else:
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de cerda Condimentado')
        FileteCondimentado.costoProducto = condimentado.costoFileteCond
        bodegaFileteCond = ProductoBodega.objects.get(bodega = 5,producto = FileteCondimentado.codigoProducto)
        bodegaFileteCond.pesoProductoStock += condimentado.pesoFileteCond
        bodegaFileteCond.save()
        msj ='Guardado exitoso!!'

    condimentado.guardado = True
    condimentado.save()
    FileteCondimentado.save()

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')


def TraerCostoFilete(request):
    idProducto = request.GET.get('producto')
    producto = Producto.objects.get(pk = int(idProducto)).costoProducto
    respuesta = json.dumps(producto)
    return HttpResponse(respuesta,mimetype='application/json')

#**********************************************PROCESO TAJADO **********************************************************

def GestionTajado(request):
    fechainicio = date.today() - timedelta(days=20)
    fechafin = date.today()
    exito = True
    tajados = Tajado.objects.all().filter(fechaTajado__range = (fechainicio,fechafin))


    if request.method == 'POST':

        formulario = TajadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/tajado/')
    else:
        formulario = TajadoForm()

    return render_to_response('Fabricacion/GestionTajado.html',{'exito':exito,'formulario':formulario,'tajados':tajados},
                              context_instance = RequestContext(request))


def GestionDetalleTajado(request,idTajado):
    exito = True
    tajado = Tajado.objects.get(pk = idTajado)
    Detalletajados = DetalleTajado.objects.filter(tajado = idTajado)



    if request.method == 'POST':

        formulario = DetalleTajadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/detalleTajado/'+idTajado)
    else:
        formulario = DetalleTajadoForm(initial={'tajado':idTajado})

    return render_to_response('Fabricacion/DetalleTajado.html',{'exito':exito,'formulario':formulario,
                                                                'detalles':Detalletajados,'tajado':tajado},
                              context_instance = RequestContext(request))

def EditaDetalleTajado(request,idDetTajado):

    exito = True
    detalletajado = DetalleTajado.objects.get(pk = idDetTajado)
    tajado = Tajado.objects.get(pk = detalletajado.tajado.codigoTajado)
    Detalletajados = DetalleTajado.objects.filter(tajado = tajado.codigoTajado)




    if request.method == 'POST':

        formulario = DetalleTajadoForm(request.POST,instance=detalletajado)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/detalleTajado/'+str(tajado.codigoTajado))
    else:
        formulario = DetalleTajadoForm(initial={'tajado':tajado.codigoTajado},instance=detalletajado)

    return render_to_response('Fabricacion/DetalleTajado.html',{'exito':exito,'formulario':formulario,
                                                                'detalles':Detalletajados,'tajado':tajado},
                              context_instance = RequestContext(request))

def TraerCosto(request):
    idDesposte = request.GET.get('desposte')
    idProducto= request.GET.get(('producto'))
    desposte = DetallePlanilla.objects.get(planilla = int(idDesposte),producto = int(idProducto)).costoProducto

    respuesta = json.dumps(desposte)

    return HttpResponse(respuesta,mimetype='application/json')

def TraerCostoPollo(request):
    idCompra = request.GET.get('compra')
    idProducto= request.GET.get('producto')
    compra = DetalleCompra.objects.get(compra = int(idCompra),producto = int(idProducto)).vrKiloDescongelado

    respuesta = json.dumps(compra)

    return HttpResponse(respuesta,mimetype='application/json')

def costearTajado(request):
    idTajado = request.GET.get('idTajado')
    tipo = request.GET.get('tipo')
    detTajado = DetalleTajado.objects.filter(tajado = int(idTajado))
    tajado = Tajado.objects.get(pk = int(idTajado))
    mod = tajado.mod
    cif = tajado.cif
    costokilo = 0

    costoTotal = ((tajado.pesoProducto)/1000) * tajado.costoKiloFilete + mod + cif

    if tipo == 'Cerdos' or tipo == 'Cerdas':
        #milanesa 98.5% ,  Recortes 0,5% ,  Procesos 1%
        for tjdo in detTajado:
            producto = Producto.objects.get(pk = tjdo.producto.codigoProducto)

            if tjdo.producto.nombreProducto == 'Filete de Cerdo':
                tjdo.costoKilo = (costoTotal * Decimal(0.985))/(tjdo.pesoProducto /1000)
                costokilo = tjdo.costoKilo
                tajado.totalTajado = tjdo.pesoProducto
            elif tjdo.producto.nombreProducto == 'Filete de Cerda':
                tjdo.costoKilo = (costoTotal * Decimal(0.985))/(tjdo.pesoProducto /1000)
                costokilo = tjdo.costoKilo
                tajado.totalTajado = tjdo.pesoProducto
            elif tjdo.producto.nombreProducto == 'Recortes Cerdo' or tjdo.producto.nombreProducto == 'Recortes':
                tjdo.costoKilo = costoTotal * Decimal(0.005)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
            elif tjdo.producto.nombreProducto == 'Procesos Cerdo' or tjdo.producto.nombreProducto == 'Procesos Cerda':
                tjdo.costoKilo = costoTotal * Decimal(0.01)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo


            producto.costoProducto =  costokilo
            producto.save()
            tjdo.save()

        msj = 'Costeo Exitoso'

    else:
        for tjdo in detTajado:
            producto = Producto.objects.get(pk = tjdo.producto.codigoProducto)
            if tjdo.producto.nombreProducto == 'Filete de Pollo':
                tjdo.costoKilo = costoTotal * Decimal(0.953)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
                tajado.totalTajado = tjdo.pesoProducto
            elif tjdo.producto.nombreProducto == 'Hueso de pollo':
                tjdo.costoKilo = costoTotal * Decimal(0.016)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
            elif tjdo.producto.nombreProducto == 'Piel':
                tjdo.costoKilo = costoTotal * Decimal(0.019)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
            elif tjdo.producto.nombreProducto == 'Procesos de pollo':
                tjdo.costoKilo = costoTotal * Decimal(0.012)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
            producto.costoProducto =  costokilo
            producto.save()
            tjdo.save()

        msj = 'Costeo Exitoso'

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')


def GuardarTajado(request):
    idTajado = request.GET.get('idTajado')
    detTajado = DetalleTajado.objects.filter(tajado = int(idTajado))
    tajado = Tajado.objects.get(pk = int(idTajado))
    #guardamos el producto utilizado
    bodegaTajado = ProductoBodega.objects.get(bodega = 5, producto = tajado.producto.codigoProducto)
    bodegaTajado.pesoProductoStock -= tajado.pesoProducto
    bodegaTajado.save()

    movimiento = Movimientos()
    movimiento.tipo = 'TJD%d'%(tajado.codigoTajado)
    movimiento.productoMov = tajado.producto
    movimiento.fechaMov = tajado.fechaTajado
    movimiento.salida = tajado.pesoProducto
    movimiento.save()


    for det in detTajado:

        #Guardamos el producto resultante
        bodega = ProductoBodega.objects.get(bodega = 6,producto =  det.producto.codigoProducto)
        bodega.unidadesStock += det.unidades
        bodega.pesoProductoStock += det.pesoProducto
        bodega.save()
        movimiento = Movimientos()
        movimiento.tipo = 'TJD%d'%(tajado.codigoTajado)
        movimiento.productoMov = det.producto
        movimiento.fechaMov = tajado.fechaTajado
        movimiento.entrada = det.pesoProducto
        movimiento.save()

    tajado.guardado = True
    tajado.save()

    msj = 'Registro guardado exitosamente'

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

#***********************************************PLANILLA DESPOSTE*******************************************************

def GestionDesposte(request):
    despostes = PlanillaDesposte.objects.all()

    if request.method == 'POST':

        formulario = DesposteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/desposte')
    else:
        formulario =DesposteForm()

    return render_to_response('Fabricacion/GestionDesposte.html',{'formulario':formulario,'despostes':despostes},
                              context_instance = RequestContext(request))
def EditaDesposte(request,idDesposte):
    desposte = PlanillaDesposte.objects.get(pk = idDesposte)
    despostes = PlanillaDesposte.objects.all()

    if request.method == 'POST':

        formulario = DesposteForm(request.POST,instance=desposte)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/desposte')
    else:
        formulario =DesposteForm(instance=desposte)

    return render_to_response('Fabricacion/GestionDesposte.html',{'formulario':formulario,'despostes':despostes},
                              context_instance = RequestContext(request))

def GestionDesposteActualizado(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

    #Filtramos los despostes en grupos para su posterior costeo
    carnes = detalleDespostes.filter(grupo = 'Grupo Carnes')
    carnes2 = detalleDespostes.filter(grupo = 'Grupo Carnes 2')
    carnes3 = detalleDespostes.filter(grupo = 'Grupo Carnes 3')
    carnes4 = detalleDespostes.filter(grupo = 'Grupo Carnes 4')
    costillas = detalleDespostes.filter(grupo = 'Grupo Costillas')
    huesos = detalleDespostes.filter(grupo = 'Grupo Huesos')
    subProductos = detalleDespostes.filter(grupo = 'Grupo SubProductos')
    desechos = detalleDespostes.filter(grupo = 'Grupo Desechos')
    #extraemos el tipo de desposte que se esta haciendo
    tipoDesposte = ''
    for tipo in detalleDespostes:
        if tipo.grupo == 'Grupo Carnes':
            tipoDesposte = tipo.producto.grupo.nombreGrupo


    #calculamos el peso del grupo
    pesoCarnes = 0
    pesoCarnes2 = 0
    pesoCarnes3 = 0
    pesoCarnes4 = 0
    pesoCostillas = 0
    pesoHuesos = 0
    pesoSubProd = 0
    pesoDesecho = 0
    perdidaPeso= 0


    for peso in carnes:
        pesoCarnes += peso.PesoProducto
    for peso in carnes2:
        pesoCarnes2 += peso.PesoProducto
    for peso in carnes3:
        pesoCarnes3 += peso.PesoProducto
    for peso in carnes4:
        pesoCarnes4 += peso.PesoProducto
    for peso in costillas:
        pesoCostillas += peso.PesoProducto
    for peso in huesos:
        pesoHuesos += peso.PesoProducto
    for peso in subProductos:
        pesoSubProd += peso.PesoProducto
    for peso in desechos:
        if peso.producto.nombreProducto == 'Desecho':
            pesoDesecho += peso.PesoProducto
        if peso.producto.nombreProducto == 'Perdida peso':
            perdidaPeso = peso.PesoProducto



    # Extraemos el peso total de los canales a despostar ademas del valor del kilo del canal
    pesoCanales = 0
    codrecep = 0

    for cnl in canales :
        pesoCanales += cnl.pesoPorkilandia
        codrecep = cnl.recepcion.codigoRecepcion


    recep = PlanillaRecepcion.objects.get(pk = codrecep)
    vrKiloCanal = recep.vrKiloCanal

    #Calculamos el peso total de desposte

    pesoTotalDesposte = pesoCarnes +pesoCarnes2+pesoCarnes3+pesoCarnes4+ pesoCostillas + pesoHuesos + pesoSubProd + pesoDesecho

    #el valor total de los canales a despostar se calcula con el peso de canales y el valor del kilo en canal
    vrTotalCanales = pesoCanales * vrKiloCanal

    # calculamos el valor de cada grupo multiplicando el %Grupo por el vrTotalCanales
    if tipoDesposte == 'Cerdos':
        vrCarnes = ceil((vrTotalCanales * 43)/100)
        vrCarnes2 = ceil((vrTotalCanales * Decimal(28.5))/100)
        vrCarnes3 = 0
        vrCarnes4 = 0
        vrCostillas = ceil((vrTotalCanales * 11)/100)
        vrHuesos = ceil((vrTotalCanales * 4)/100)
        vrsubProd = ceil((vrTotalCanales * 11)/100)
        vrDesecho = ceil((vrTotalCanales * Decimal(2.5))/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido

    elif tipoDesposte == 'Cerdas':
        vrCarnes = ceil((vrTotalCanales * 37)/100)
        vrCarnes2 = ceil((vrTotalCanales * 32)/100)
        vrCarnes3 = 0
        vrCarnes4 = 0
        vrCostillas = ceil((vrTotalCanales * 11)/100)
        vrHuesos = ceil((vrTotalCanales * 3)/100)
        vrsubProd = ceil((vrTotalCanales * 15)/100)
        vrDesecho = ceil((vrTotalCanales * 2)/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido
    else:
        vrCarnes = ceil((vrTotalCanales * 6)/100)
        vrCarnes2 = ceil((vrTotalCanales * Decimal(32.5))/100)
        vrCarnes3 = ceil((vrTotalCanales * 30)/100)
        vrCarnes4 = ceil((vrTotalCanales * Decimal(6.5))/100)
        vrCostillas = ceil((vrTotalCanales * 9)/100)
        vrHuesos = ceil((vrTotalCanales * 7)/100)
        vrsubProd = ceil((vrTotalCanales * 6)/100)
        vrDesecho = ceil((vrTotalCanales * 2)/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido



    #calculamos el valor del kilo base en cada grupo
    if pesoCarnes == 0:
        vrKiloCarnes = 0
    else:
         vrKiloCarnes = Decimal(vrCarnes) / (pesoCarnes / 1000)

    if pesoCarnes2 == 0:
        vrKiloCarnes2 = 0
    else:
         vrKiloCarnes2 = Decimal(vrCarnes2) / (pesoCarnes2 / 1000)
    if pesoCarnes3 == 0:
        vrKiloCarnes3 = 0
    else:
         vrKiloCarnes3 = Decimal(vrCarnes3) / (pesoCarnes3 / 1000)
    if pesoCarnes4 == 0:
        vrKiloCarnes4 = 0
    else:
         vrKiloCarnes4 = Decimal(vrCarnes4) / (pesoCarnes4 / 1000)

    if pesoCostillas == 0:
        vrKiloCostillas = 0
    else:
         vrKiloCostillas = Decimal(vrCostillas) / (pesoCostillas / 1000)

    if pesoHuesos == 0:
        vrKiloHuesos = 0
    else:
         vrKiloHuesos = Decimal(vrHuesos) / (pesoHuesos/ 1000)

    if pesoSubProd == 0:
        vrKiloSubProd = 0
    else:
         vrKiloSubProd = Decimal(vrsubProd) / (pesoSubProd/ 1000)

    if pesoDesecho == 0:
        vrKiloDesecho = 0
    else:
         vrKiloDesecho = Decimal(vrDesecho) / ((pesoDesecho + perdidaPeso)/ 1000)


    #canalesMachos = Canal.objects.filter(planilla = idplanilla).filter(estado = True).filter(genero = 'Macho')

    #Actualizamos los valores de la planilla de desposte

    difCanalDesposte = (pesoCanales * 1000) - pesoTotalDesposte
    desposte.totalDespostado = pesoTotalDesposte
    desposte.difCanalADespostado = difCanalDesposte
    desposte.totalCanal = pesoCanales
    desposte.tipoDesposte = tipoDesposte
    desposte.resesADespostar = canales.count()
    desposte.save()

    if request.method == 'POST':
        formulario = DetalleDesposteForm(int(idplanilla),request.POST)

        if formulario.is_valid():
           detalles = formulario.save()

           #validamos las partes de las reses de limpieza de sacrificio
           idRecepcion = 0
           canalDesposte = Canal.objects.filter(planilla = idplanilla)
           for candesp in canalDesposte :
               idRecepcion = candesp.recepcion.codigoRecepcion
           recepcion = PlanillaRecepcion.objects.get(pk = idRecepcion)
           cantReses = recepcion.cantCabezas
           sacrificio = Sacrificio.objects.get(recepcion = recepcion.codigoRecepcion)
           productoEntrante = int(request.POST.get('producto'))
           prodEnt = str(Producto.objects.get(pk = productoEntrante).nombreProducto)
           pesoProducto = Decimal(request.POST.get('PesoProducto'))

           if prodEnt == 'Cola':
               detalles.PesoProducto = (sacrificio.cola / cantReses) * canales.count()
           elif prodEnt == 'Rinones':
               detalles.PesoProducto =(sacrificio.rinones / cantReses) * canales.count()
           elif prodEnt == 'Creadillas':
               detalles.PesoProducto =(sacrificio.creadillas / cantReses) * canales.count()
           elif prodEnt == 'Recortes Sacrificio':
               detalles.PesoProducto =(sacrificio.recortes / cantReses) * canales.count()
           elif prodEnt == 'Ubre':
               detalles.PesoProducto =(sacrificio.ubre / cantReses) * canales.count()
           else:
               detalles.PesoProducto =pesoProducto

           #guardamos todos los datos en el detalle del desposte
           detalles.vrKiloCarnes = vrKiloCarnes
           detalles.vrKiloCarnes2 = vrKiloCarnes2
           detalles.vrKiloCarnes3 = vrKiloCarnes3
           detalles.vrKiloCarnes4 = vrKiloCarnes4
           detalles.vrKiloCostilla = vrKiloCostillas
           detalles.vrKiloHuesos = vrKiloHuesos
           detalles.vrKiloSubProd = vrKiloSubProd
           detalles.vrKiloDesecho = vrKiloDesecho
           detalles.pesoCarne = pesoCarnes
           detalles.pesoCostilla = pesoCostillas
           detalles.pesoHueso = pesoHuesos
           detalles.pesoSubProd = pesoSubProd
           detalles.pesoDesecho = pesoDesecho
           detalles.save()


           return HttpResponseRedirect('/fabricacion/detalleDesposte/'+ idplanilla)
    else:
        formulario = DetalleDesposteForm(int(idplanilla),initial={'planilla':idplanilla})

    contexto = {'vrKiloCarnes2':vrKiloCarnes2,'vrKiloCarnes3':vrKiloCarnes3,'vrKiloCarnes4':vrKiloCarnes4,'vrKiloCarnes':vrKiloCarnes,
                'vrKiloCostillas':vrKiloCostillas,'vrKiloHuesos':vrKiloHuesos,
                'vrKiloSubProd':vrKiloSubProd,'vrKiloDesecho':vrKiloDesecho,'carnes4':carnes4,'carnes3':carnes3,'carnes2':carnes2,
                'carnes':carnes,'costillas':costillas,
                'huesos':huesos,'subProductos':subProductos,'desechos':desechos,'formulario':formulario,'desposte':desposte,
                'canales':canales,'detalleDespostes':detalleDespostes,'vrCarnes':vrCarnes,'vrCarnes2':vrCarnes2,
                'vrCarnes3':vrCarnes3,'vrCarnes4':vrCarnes4,'vrCostillas':vrCostillas,'vrHuesos':vrHuesos,'vrsubProd':vrsubProd,
                'vrDesecho':vrDesecho}

    return render_to_response('Fabricacion/GestionDeposteActualizado.html',
                              contexto,context_instance = RequestContext(request))

def costeoDesposte(request):
    idDesposte = request.GET.get('idDesposte')
    idDesposte = int(idDesposte)
    desposte = PlanillaDesposte.objects.get(pk = idDesposte)
    detalleDesposte = DetallePlanilla.objects.filter(planilla = desposte.codigoPlanilla)
    productosCosteados = detalleDesposte.count()


    #Evaluamos de que tipo de compra vienen los canales despostados para aplicar valores de CIF y MOD

    Idrecepcion = 0
    canales = Canal.objects.filter(planilla = desposte.codigoPlanilla)
    for cnl in canales:
        Idrecepcion = cnl.recepcion.codigoRecepcion
    recepcion = PlanillaRecepcion.objects.get(pk = Idrecepcion)
    compra = Compra.objects.get(pk = recepcion.compra.codigoCompra)
    tipoCompra = compra.tipo.nombreGrupo

    Mod = desposte.mod
    Cif = desposte.cif

    #traemos via JSON todas las variables de la plantilla
    pesoCanales = request.GET.get('pesoCanales')
    pesoCanales = int(pesoCanales)*1000
    cantProductos = detalleDesposte.count()
    cif = Cif / cantProductos
    costoKilo = 0


    kiloCarnes = request.GET.get('kiloCarnes')
    kiloCarnes2 = request.GET.get('kiloCarnes2')
    kiloCarnes3 = request.GET.get('kiloCarnes3')
    kiloCarnes4 = request.GET.get('kiloCarnes4')
    kiloCostilla = request.GET.get('kiloCostilla')
    kiloHueso = request.GET.get('kiloHueso')
    kiloSubProd = request.GET.get('kiloSubProd')
    kiloDesecho = request.GET.get('kiloDesecho')

    for detalle in detalleDesposte:
        #obtenemos el producto en cuestion
        producto = Producto.objects.get(pk = detalle.producto.codigoProducto)
        #Calculamos el % de trabajo
        porcentajeTrabajo = (detalle.PesoProducto * 100)/pesoCanales
        modProducto = (porcentajeTrabajo /100)*Mod

        if detalle.grupo == 'Grupo Carnes':
            costoKilo = int(kiloCarnes) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo Carnes 2':
            costoKilo = int(kiloCarnes2) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo Carnes 3':
            costoKilo = int(kiloCarnes3) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo Carnes 4':
            costoKilo = int(kiloCarnes4) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo Costillas':
            costoKilo = int(kiloCostilla) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo Huesos':
            costoKilo = int(kiloHueso) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo SubProductos':
            costoKilo = int(kiloSubProd) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        if detalle.grupo == 'Grupo Desechos':
            costoKilo = int(kiloDesecho) + ((cif + modProducto)/(detalle.PesoProducto/1000))
        # el costo del kilo del producto mas los gastos de administracion
        producto.costoProducto = costoKilo
        producto.save()
        # se guarda el costo actual para tener un historico del costo en ese desposte en especifico
        detalle.costoProducto = costoKilo
        detalle.costoAdtvo = costoKilo * Decimal(1.23)
        detalle.save()

         #Se guarda el cif y el mod actual
        desposte.cif = Cif
        desposte.mod = Mod
        desposte.save()

    exito = '%s productos Fueron Costeados exitosamente ¡¡'%productosCosteados
    respuesta = json.dumps(exito)
    return HttpResponse(respuesta,mimetype='application/json')

def GuardarDesposte(request):
    idDesposte = request.GET.get('idDesposte')
    idDesposte = int(idDesposte)
    desposte = PlanillaDesposte.objects.get(pk = idDesposte)
    detalleDesposte = DetallePlanilla.objects.filter(planilla = desposte.codigoPlanilla)
    productosGuardados = detalleDesposte.count()


    for detalle in detalleDesposte:
        #tomo el producto que voy a guardar en bodega
        producto = Producto.objects.get(pk = detalle.producto.codigoProducto)
        movimiento = Movimientos()

        #tomo la bodega a la cual quiero asignar ese producto
        bodega = ProductoBodega.objects.get(bodega = 5,producto = producto.codigoProducto)
        # si el producto que esta en la lista para ser guardado estan los productos de sacrificio
        # entonces se deja e inventario tal cual estaba
        if producto.nombreProducto == 'Cola':
            bodega.pesoProductoStock = bodega.pesoProductoStock
        elif producto.nombreProducto == 'Rinones':
            bodega.pesoProductoStock = bodega.pesoProductoStock
        elif producto.nombreProducto == 'Creadillas':
            bodega.pesoProductoStock = bodega.pesoProductoStock
        elif producto.nombreProducto == 'Ubre':
            bodega.pesoProductoStock = bodega.pesoProductoStock
        elif producto.nombreProducto == 'Recortes Sacrificio':
            bodega.pesoProductoStock = bodega.pesoProductoStock
        else:#Se guardan el peso y las unidades en inventario
            bodega.pesoProductoStock += detalle.PesoProducto
            bodega.unidadesStock += detalle.unidades

            movimiento.tipo = 'DSP%d'%(desposte.codigoPlanilla)
            movimiento.fechaMov = desposte.fechaDesposte
            movimiento.productoMov = detalle.producto
            movimiento.entrada = detalle.PesoProducto
            movimiento.save()

        bodega.save()

        desposte.guardado = True
        desposte.save()

    exito = '%s productos se guardaron exitosamente'%productosGuardados
    respuesta = json.dumps(exito)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionValorCostos(request):

    costos = ValoresCostos.objects.all()

    if request.method == 'POST':
        formulario = costoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/costos/')
    else:
        formulario = costoForm()

    return render_to_response('Fabricacion/GestionValoresCostos.html',{'costos':costos, 'formulario':formulario},
                              context_instance = RequestContext(request))

def EditaDetPlanilla(request,idDetalle):

    detalle  = DetallePlanilla.objects.get(pk = idDetalle)
    idplanilla = PlanillaDesposte.objects.get(pk = detalle.planilla.codigoPlanilla).codigoPlanilla
    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

    #Filtramos los despostes en grupos para su posterior costeo
    carnes = detalleDespostes.filter(grupo = 'Grupo Carnes')
    carnes2 = detalleDespostes.filter(grupo = 'Grupo Carnes 2')
    carnes3 = detalleDespostes.filter(grupo = 'Grupo Carnes 3')
    carnes4 = detalleDespostes.filter(grupo = 'Grupo Carnes 4')
    costillas = detalleDespostes.filter(grupo = 'Grupo Costillas')
    huesos = detalleDespostes.filter(grupo = 'Grupo Huesos')
    subProductos = detalleDespostes.filter(grupo = 'Grupo SubProductos')
    desechos = detalleDespostes.filter(grupo = 'Grupo Desechos')

    if request.method == 'POST':
        formulario = DetalleDesposteForm(idplanilla,request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/detalleDesposte/'+ str(idplanilla))
    else:
        formulario = DetalleDesposteForm(idplanilla,instance=detalle)

    contexto = {'carnes4':carnes4,'carnes3':carnes3,'carnes2':carnes2,'carnes':carnes,'costillas':costillas,'huesos':huesos,'subProductos':subProductos,
                'desechos':desechos,'formulario':formulario,'desposte':desposte,'canales':canales,
                'detalleDespostes':detalleDespostes}

    return render_to_response('Fabricacion/GestionDeposteActualizado.html',contexto,
                              context_instance = RequestContext(request))

def EditaCostos(request,idcosto):

    costos = ValoresCostos.objects.all()
    costo  = ValoresCostos.objects.get(pk = idcosto)

    if request.method == 'POST':
        formulario = costoForm(request.POST,instance=costo)
        if formulario.is_valid():
            costo = formulario.save()
            costo.fecha = date.today()
            costo.save()
            return HttpResponseRedirect('/fabricacion/costos/')
    else:
        formulario = costoForm(instance=costo)


    return render_to_response('Fabricacion/GestionValoresCostos.html',{'costos':costos, 'formulario':formulario},
                              context_instance = RequestContext(request))

def InformeCanalesPendientes(request):
    canalPendiente = Canal.objects.filter(estado = False).order_by('codigoCanal')
    return render_to_response('Fabricacion/InformeCanalesPendientes.html',{'canalesPendientes':canalPendiente},
                              context_instance = RequestContext(request))

def GestionDescarneCabeza(request):

    descarnes = DescarneCabeza.objects.all()
    costoCabeza = Producto.objects.filter(nombreProducto = 'Cabeza')

    # sacamos el costo de las cabezas de cerdo y cerda ppor separado
    costoCabezaCerdo = 0
    costoCabezaCerda = 0

    for costo in costoCabeza:
        if costo.grupo.nombreGrupo == 'Cerdos':
            costoCabezaCerdo = costo.costoProducto
        else:
            costoCabezaCerda = costo.costoProducto



    if request.method == 'POST':
        formulario = DescarneForm(request.POST)
        if formulario.is_valid():
            descarne = formulario.save()

            #validamos el tipo de cabeza que se quiere procesar

            if descarne.tipo == 'Cerdos':

                #traemos los valores de costo y cantidad de cabezas
                costoTotal =((descarne.pesoCabezas /descarne.cantidad)/1000) * costoCabezaCerdo

                cif = descarne.mod
                mod = descarne.cif
                #Sumamos el cif y el mod al costo total de cabezas
                costoDescarne = (costoTotal * descarne.cantidad) + cif + mod

                #Calculamos los costos de cada sub producto
                costoCaretas = Decimal(0.26) * costoDescarne
                vrKiloCareta = ceil(Decimal(costoCaretas) / (descarne.caretas/1000))

                costoLenguas = Decimal(0.05) * costoDescarne
                vrKiloLenguas = ceil(Decimal(costoLenguas) / (descarne.lenguas/1000))


                costoProcesos = Decimal(0.69) * costoDescarne
                vrKiloProcesos = ceil(Decimal(costoProcesos) / (descarne.procesos/1000))

                 #Guardamos los costos en la tabla Producto

                proceso = Producto.objects.get(nombreProducto = 'Procesos de Cabeza Cerdo')
                proceso.costoProducto = vrKiloProcesos
                proceso.save()

                careta = Producto.objects.get(nombreProducto = 'Careta Cerdo')
                careta.costoProducto = vrKiloCareta
                careta.save()

                lengua = Producto.objects.get(nombreProducto = 'Lengua Cerdo')
                lengua.costoProducto = vrKiloLenguas
                lengua.save()

                descarne.vrKiloProceso = vrKiloProcesos
                descarne.vrKiloLengua = vrKiloLenguas
                descarne.vrKiloCareta = vrKiloCareta
            else:
                #traemos los valores de costo y cantidad de cabezas

                costoTotal =((descarne.pesoCabezas /descarne.cantidad)/1000) * costoCabezaCerda

                cif = descarne.mod
                mod = descarne.cif
                #Sumamos el cif y el mod al costo total de cabezas
                costoDescarne = (costoTotal * descarne.cantidad) + cif + mod

                #Calculamos los costos de cada sub producto
                costoRecorte = Decimal(0.30) * costoDescarne
                #vrKiloRecorte = ceil(Decimal(costoRecorte) / (descarne.recortes/1000))
                costoUnidad = costoRecorte / descarne.cantRecosrtes

                costoProcesos = Decimal(0.70) * costoDescarne
                vrKiloProcesos = ceil(Decimal(costoProcesos) / (descarne.procesos/1000))

                #Guardamos los costos en la tabla Producto
                recorte = Producto.objects.get(nombreProducto = 'Recortes Cabeza Cerda')
                recorte.costoProducto = costoUnidad
                recorte.save()

                proceso = Producto.objects.get(nombreProducto = 'Procesos de Cabeza Cerda')
                proceso.costoProducto =vrKiloProcesos
                proceso.save()

                descarne.vrKiloProceso = vrKiloProcesos
                descarne.vrKiloRecor = costoUnidad


            descarne.save()

            return HttpResponseRedirect('/fabricacion/descarne/')
    else:
        formulario = DescarneForm()

    return render_to_response('Fabricacion/GestionDescarneCabezas.html',{'descarnes':descarnes, 'formulario':formulario},
                              context_instance = RequestContext(request))

def GuardaDescarne(request):
    idDescarne = request.GET.get('descarne')
    descarne = DescarneCabeza.objects.get(pk = int(idDescarne))

    if descarne.tipo == 'Cerdos':

        bodegaProcesos = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto = 'Procesos de Cabeza Cerdo')
        bodegaProcesos.pesoProductoStock += descarne.procesos
        bodegaProcesos.save()

        bodegaCareta = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto = 'Careta Cerdo')
        bodegaCareta.pesoProductoStock += descarne.caretas
        bodegaCareta.save()

        bodegaLenguas = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto = 'Lengua Cerdo')
        bodegaLenguas.pesoProductoStock += descarne.lenguas
        bodegaLenguas.save()

        msj = 'Guardado Exitoso'

        #se saca del inventario toda la cabeza
        cabeza = Producto.objects.get(nombreProducto = 'Cabeza',grupo__nombreGrupo = 'Cerdos')
        bodegaCabeza = ProductoBodega.objects.get(bodega = 5, producto = cabeza.codigoProducto)
        bodegaCabeza.pesoProductoStock -= descarne.pesoCabezas

    else:
        bodegaRecorte = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto = 'Recortes Cabeza Cerda')
        bodegaRecorte.unidadesStock += descarne.cantRecosrtes
        bodegaRecorte.save()

        bodegaProcesos = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto ='Procesos de Cabeza Cerda')
        bodegaProcesos.pesoProductoStock += descarne.procesos
        bodegaProcesos.save()

        #se saca del inventario toda la cabeza
        cabeza = Producto.objects.get(nombreProducto = 'Cabeza',grupo__nombreGrupo = 'Cerdas')
        bodegaCabeza = ProductoBodega.objects.get(bodega = 5, producto = cabeza.codigoProducto)
        bodegaCabeza.pesoProductoStock -= descarne.pesoCabezas

        msj = 'Guardado Exitoso'

    descarne.guardado = True
    descarne.save()

    respuesta  = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionEmpacadoApanados(request):
    empaques  = EmpacadoApanados.objects.all()

    if request.method == 'POST':

        formulario = EmpacadoApanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/empacadoApanado')
    else:
        formulario = EmpacadoApanadoForm(initial={'mod':1812})

    return render_to_response('Fabricacion/GestionEmpaqueApanado.html',{'formulario':formulario,'empaques':empaques },
                              context_instance = RequestContext(request))


def CostearEmpacado(request):
    idEmpaque = request.GET.get('idEmpaque')
    empaque = EmpacadoApanados.objects.get(pk = int(idEmpaque))
    pesoChuleta = empaque.pesoChuelta / 1000
    chuletaEmpacadaPollo = Producto.objects.get(nombreProducto = 'Chuleta Empacada Pollo')
    chuletaEmpacadaCerdo = Producto.objects.get(nombreProducto = 'Chuleta Empacada Cerdo')
    stiker = Producto.objects.get(nombreProducto = 'Stiker').costoProducto
    bandeja = Producto.objects.get(nombreProducto = 'Bandeja').costoProducto
    costoTotalAEmpacar = pesoChuleta * empaque.costoKiloChuleta

    costoTotal = (stiker * empaque.stikers)+(bandeja * empaque.cantBandejas)+ costoTotalAEmpacar + empaque.mod
    costoBandeja = costoTotal / empaque.cantBandejas
    pesoBandeja = pesoChuleta / empaque.cantBandejas

    empaque.costobandeja = costoBandeja
    empaque.pesoBandeja = pesoBandeja
    empaque.save()
    if empaque.productoAEmpacar.grupo.nombreGrupo == 'Pollos':
        chuletaEmpacadaPollo.costoProducto = costoBandeja
        chuletaEmpacadaPollo.save()
    elif empaque.productoAEmpacar.grupo.nombreGrupo == 'Cerdos' or empaque.productoAEmpacar.grupo.nombreGrupo == 'Cerdas':
        chuletaEmpacadaCerdo.costoProducto = costoBandeja
        chuletaEmpacadaCerdo.save()

    msj = 'Costeo Exitoso'
    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GuardarEmpacado(request):
    idEmpaque = request.GET.get('idEmpaque')
    empaque = EmpacadoApanados.objects.get(pk = int(idEmpaque))

    bodegaBandeja = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Bandeja')
    bodegaStiker = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Stiker')
    bodegaChuleta = ProductoBodega.objects.get(bodega = 6,producto = empaque.productoAEmpacar.codigoProducto)
    bodegaChuletaEmpacadaPollo = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Chuleta Empacada Pollo')
    bodegaChuletaEmpacadaCerdo = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Chuleta Empacada Cerdo')

    bodegaBandeja.unidadesStock -= empaque.cantBandejas
    bodegaBandeja.save()

    bodegaStiker.unidadesStock -= empaque.stikers
    bodegaStiker.save()

    bodegaChuleta.pesoProductoStock -= empaque.pesoChuelta
    bodegaChuleta.save()

    if empaque.productoAEmpacar.grupo.nombreGrupo == 'Pollos':
        bodegaChuletaEmpacadaPollo.pesoProductoStock += empaque.pesoChuelta
        bodegaChuletaEmpacadaPollo.save()
    elif empaque.productoAEmpacar.grupo.nombreGrupo == 'Cerdos' or empaque.productoAEmpacar.grupo.nombreGrupo == 'Cerdas':
        bodegaChuletaEmpacadaCerdo.pesoProductoStock += empaque.pesoChuelta
        bodegaChuletaEmpacadaCerdo.save()

    empaque.guardado = True
    empaque.save()

    msj = 'Guardado Exitoso'

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def ConsultaCostoChuleta(request):
    idProduccion = request.GET.get('produccion')
    produccion = ProcesoApanado.objects.get(pk = int(idProduccion)).costoKiloApanado
    respuesta = json.dumps(produccion)
    return HttpResponse(respuesta,mimetype='application/json')

def promedioCostoProducto(request):
    gr = Grupo.objects.filter(nombreGrupo = 'Reses')
    gcda = Grupo.objects.filter(nombreGrupo = 'Cerdas')
    gcdo = Grupo.objects.filter(nombreGrupo = 'Cerdos')
    grupos = gr | gcda | gcdo
    return render_to_response('Fabricacion/promedio.html',{'grupos':grupos},context_instance = RequestContext(request))



def CalcularPromedio(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    grupo = request.GET.get('grupo')
    grupos = Grupo.objects.get(pk = int(grupo))

    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()
    despostes = PlanillaDesposte.objects.filter(fechaDesposte__range = (finicio,ffin)).filter(tipoDesposte = grupos.nombreGrupo)
    ListaCosto = {}
    ListaPeso = {}
    promedioPerdida = despostes.aggregate(Avg('difCanalADespostado'))
    totalDespostado = {}
    totalDespostado['Total Despostado'] = 0


    cantDesp = 0
    cont = 0

    for pesos in despostes:
        totalDespostado['Total Despostado'] += ceil(pesos.totalDespostado /1000)

    for desposte in despostes:
        detalleDespostes = DetallePlanilla.objects.filter(planilla = desposte.codigoPlanilla)
        cantDesp = despostes.count()
        for detalle in detalleDespostes:
            ListaCosto[detalle.producto.nombreProducto] = 0
            ListaPeso[detalle.producto.nombreProducto] = 0



    for desposte in despostes:
        detalleDespostes = DetallePlanilla.objects.filter(planilla = desposte.codigoPlanilla)
        for detalle in detalleDespostes:
            ListaCosto[detalle.producto.nombreProducto] += detalle.costoProducto


    for desposte in despostes:
        detalleDespostes = DetallePlanilla.objects.filter(planilla = desposte.codigoPlanilla)
        for detalle in detalleDespostes:
            if detalle.producto.nombreProducto == 'Recortes Desposte':
                ListaPeso[detalle.producto.nombreProducto] += detalle.unidades
            else:
                ListaPeso[detalle.producto.nombreProducto] += ceil(detalle.PesoProducto)



    for llave,valor in ListaCosto.items():
        ListaCosto[llave] = valor/cantDesp

    listas = {'costos':ListaCosto,'pesos':ListaPeso,'promedioPerdida':promedioPerdida,'totalDespostado':totalDespostado}


    respuesta = json.dumps(listas)

    return HttpResponse(respuesta,mimetype='application/json')

def TemplatePromedioPechugaCond(request):
    return render_to_response('Fabricacion/PromedioPechugaCondPollo.html',context_instance = RequestContext(request))


def RepFiletePechugaCond(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    ListaCosto = {}
    ListaPeso = {}
    ListaPesoFilete = {}
    cantBandejas = {}
    cantBandejasCerdo = {}
    pesoChuletaCerdo = {}
    pesoChuletaPollo = {}
    pesoChuletaPollo['Chuleta Pollo'] = 0
    pesoChuletaCerdo['Chuleta Cerdo'] = 0
    ListaPesoFilete['Filete de Pollo Condimentado'] = 0
    cantBandejas['Bandejas Chuleta de Pollo'] = 0
    cantBandejasCerdo['Bandejas Chuleta de Cerdo'] = 0
    pesoTotal = 0

    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    q1 = ProcesoApanado.objects.filter(fechaApanado__range = (finicio,ffin)).filter(productoApanado__grupo__nombreGrupo = 'Cerdos' )
    q2 = ProcesoApanado.objects.filter(fechaApanado__range = (finicio,ffin)).filter(productoApanado__grupo__nombreGrupo = 'Cerdas' )
    chuletaCerdo = q1 | q2
    promedioChuletasCerdo = chuletaCerdo.aggregate(Avg('costoKiloApanado'))

    for chuleta in chuletaCerdo:
        pesoChuletaCerdo['Chuleta Cerdo'] += ceil(chuleta.totalApanado)


    chuletaPollo = ProcesoApanado.objects.filter(fechaApanado__range = (finicio,ffin)).filter(productoApanado__grupo__nombreGrupo = 'Pollos' )
    promedioChuletasPollo = chuletaPollo.aggregate(Avg('costoKiloApanado'))

    for chPollo in chuletaPollo:
        pesoChuletaPollo['Chuleta Pollo'] += ceil(chPollo.totalApanado)



    bandejasCerdo = EmpacadoApanados.objects.filter(fechaEmpacado__range = (finicio,ffin) ).filter(productoAEmpacar__grupo__nombreGrupo = 'Cerdos' )
    promedioBandejasCerdo = bandejasCerdo.aggregate(Avg('costobandeja'))

    for bandeja in bandejasCerdo:
        cantBandejasCerdo['Bandejas Chuleta de Cerdo'] += bandeja.cantBandejas


    bandejasPollo = EmpacadoApanados.objects.filter(fechaEmpacado__range = (finicio,ffin) ).filter(productoAEmpacar__grupo__nombreGrupo = 'Pollos' )
    promedioBandejasPollo = bandejasPollo.aggregate(Avg('costobandeja'))

    for bandeja in bandejasPollo:
        cantBandejas['Bandejas Chuleta de Pollo'] += bandeja.cantBandejas



    condimentado = Condimentado.objects.filter(fecha__range = (finicio,ffin) ).filter(producto__grupo__nombreGrupo = 'Pollos' )
    Promedio = condimentado.aggregate(Avg('costoFileteCond'))

    for cond in condimentado:
        ListaPesoFilete['Filete de Pollo Condimentado'] += ceil(cond.pesoFileteCond)



    tajados = Tajado.objects.filter(fechaTajado__range = (finicio,ffin)).filter(producto__grupo__nombreGrupo = 'Pollos' )
    cantReg = tajados.count()
    for tajado in tajados:
        detalleTajado = DetalleTajado.objects.filter(tajado = tajado.codigoTajado)

        for detalle in detalleTajado:
            ListaCosto[detalle.producto.nombreProducto] = 0
            ListaPeso[detalle.producto.nombreProducto] = 0


    for tajado in tajados:
        detalleTajado = DetalleTajado.objects.filter(tajado = tajado.codigoTajado)
        for detalle in detalleTajado:
            ListaCosto[detalle.producto.nombreProducto] += detalle.costoKilo

    for llave,valor in ListaCosto.items():
        ListaCosto[llave] = valor/cantReg


    for tajado in tajados:
        detalleTajado = DetalleTajado.objects.filter(tajado = tajado.codigoTajado)
        for detalle in detalleTajado:
            ListaPeso[detalle.producto.nombreProducto] += ceil(detalle.pesoProducto)


    listas = {'ListaPesoFilete':ListaPesoFilete,'Promedio':Promedio,'promedioBandejasPollo':promedioBandejasPollo,
              'cantBandejas':cantBandejas,'ListaCosto':ListaCosto,'ListaPeso':ListaPeso,
              'promedioBandejasCerdo':promedioBandejasCerdo,'cantBandejasCerdo':cantBandejasCerdo,
              'promedioChuletasCerdo':promedioChuletasCerdo,'pesoChuletaCerdo':pesoChuletaCerdo,
              'promedioChuletasPollo':promedioChuletasPollo,'pesoChuletaPollo':pesoChuletaPollo}


    respuesta = json.dumps(listas)
    print(listas)

    return HttpResponse(respuesta,mimetype='application/json')


def TemplateInsumos(request):
    return render_to_response('Fabricacion/ReporteInsumos.html',context_instance = RequestContext(request))
def ReporteInsumos(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    ListaCantMiga = {}
    ListaCantMiga['Miga Preparada'] = 0
    ListaCantCond = {}
    ListaCantCond['Condimento Preparado'] = 0
    ListaCantMolida = {}
    ListaCantMolida['Carne Molida'] = 0

    migas = Miga.objects.filter(fechaFabricacion__range = (finicio,ffin))
    promedioMiga = migas.aggregate(Avg('costoKiloMigaProcesada'))

    for miga in migas:
        ListaCantMiga['Miga Preparada'] += ceil(miga.PesoFormulaMiga)


    condimentos = Condimento.objects.filter(fecha__range = (finicio,ffin))
    promedioCondimento = condimentos.aggregate(Avg('costoLitroCondimento'))

    for cond in condimentos:
        ListaCantCond['Condimento Preparado'] += ceil(cond.pesoCondimento * 1000)


    molidas = Molida.objects.filter(fechaMolido__range = (finicio,ffin))
    promedioMolidas = molidas.aggregate(Avg('costoKiloMolido'))

    for molido in molidas:
        ListaCantMolida['Carne Molida'] += ceil(molido.totalMolido)

    Listas = {'promedioMiga':promedioMiga,'ListaCantMiga':ListaCantMiga,'promedioCondimento':promedioCondimento,
              'ListaCantCond':ListaCantCond,'promedioMolidas':promedioMolidas,'ListaCantMolida':ListaCantMolida}

    respuesta = json.dumps(Listas)
    return HttpResponse(respuesta,mimetype='application/json')

def TemplateDescrnes(request):
    gcda = Grupo.objects.filter(nombreGrupo = 'Cerdas')
    gcdo = Grupo.objects.filter(nombreGrupo = 'Cerdos')
    grupos = gcda | gcdo

    return render_to_response('Fabricacion/TemplateDesccarnes.html',{'grupos':grupos},context_instance = RequestContext(request))

def ReporteDescarnes(request):

    grupo = request.GET.get('grupo')
    grupos = Grupo.objects.get(pk = int(grupo))

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    ListaPesoCaretas = {}
    ListaPesoRecortes = {}
    ListaPesoLenguas = {}
    ListaPesoProcesos = {}

    ListaPesoCaretas['Caretas'] = 0
    ListaPesoRecortes['Recortes'] = 0
    ListaPesoLenguas['Lenguas'] = 0
    ListaPesoProcesos['Procesos'] = 0


    descarnes = DescarneCabeza.objects.filter(fecha__range = (finicio,ffin)).filter(tipo = grupos.nombreGrupo)
    promedioCaretas = descarnes.aggregate(Avg('vrKiloCareta'))
    promedioRecortes = descarnes.aggregate(Avg('vrKiloRecorte'))
    promedioLenguas = descarnes.aggregate(Avg('vrKiloLengua'))
    promedioProcesos = descarnes.aggregate(Avg('vrKiloProceso'))

    for descarne in descarnes:
        ListaPesoCaretas['Caretas'] += ceil(descarne.caretas)
        ListaPesoRecortes['Recortes'] += descarne.cantRecosrtes
        ListaPesoLenguas['Lenguas'] += ceil(descarne.lenguas)
        ListaPesoProcesos['Procesos'] += ceil(descarne.procesos)


    Listas = {'promedioCaretas':promedioCaretas,'promedioRecortes':promedioRecortes,'promedioLenguas':promedioLenguas,
              'promedioProcesos':promedioProcesos,'ListaPesoCaretas':ListaPesoCaretas,'ListaPesoRecortes':ListaPesoRecortes,
              'ListaPesoLenguas':ListaPesoLenguas,'ListaPesoProcesos':ListaPesoProcesos}

    respuesta = json.dumps(Listas)
    return HttpResponse(respuesta,mimetype='application/json')
