 # -*- coding: UTF-8 -*-
from decimal import Decimal
from math import ceil

from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View,TemplateView

import json
from Inventario.Forms.forms import *
from Fabricacion.Forms import *
from Inventario.models import *




#******************************************************CANAL***********************************************************
def GestionCanal(request,idrecepcion):

    canales = Canal.objects.filter(recepcion = idrecepcion).order_by('nroCanal')#para renderizar las listas
    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    compra = Compra.objects.get(pk = recepcion.compra.codigoCompra)
    sacrificio = Sacrificio.objects.get(recepcion = idrecepcion)
    cantidad = canales.count() +1
    kiloCanal = 0
    for can in canales :
        kiloCanal = can.vrKiloCanal

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
        formulario = CanalForm(initial={'recepcion':idrecepcion})

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
    sal = Producto.objects.get(nombreProducto = 'Sal')
    papaina = Producto.objects.get(nombreProducto = 'Papaina')

    salBodega = ProductoBodega.objects.get(bodega = 6 , producto__nombreProducto = 'Sal')
    PapainaBodega = ProductoBodega.objects.get(bodega = 6 , producto__nombreProducto = 'Papaina')



    if request.method == 'POST':
        formulario = EnsalinadoForm(request.POST)

        if formulario.is_valid():

            ensalinado = formulario.save()

            producto = Producto.objects.get(nombreProducto = ensalinado.producto.nombreProducto)

            costoSal = (ensalinado.pesoSal/ 1000) * sal.costoProducto
            costoPapaina = (ensalinado.pesoPapaina / 1000) * papaina.costoProducto
            costoProductoEnsalinado = (ensalinado.pesoProducto / 1000) * producto.costoProducto
            costoInsumos = costoSal + costoPapaina + costoProductoEnsalinado
            cif = 30 * (ensalinado.pesoProductoDespues / 1000)
            mod = 20 * (ensalinado.pesoProductoDespues / 1000)
            costoTotal = cif + mod + costoInsumos
            costoKilo = ceil(costoTotal / (ensalinado.pesoProductoDespues /1000))

            ensalinado.pesoProductoDespues /= 1000
            ensalinado.pesoProductoAntes /= 1000
            ensalinado.pesoProducto /= 1000
            ensalinado.costoTotal = costoTotal
            ensalinado.costoKilo = costoKilo
            ensalinado.save()

            # se guarda en el Producto el Costo del Kilo
            piernaEnsalinada = Producto.objects.get(nombreProducto = 'Pierna Ensalinada')
            piernaEnsalinada.costoProducto = costoKilo
            piernaEnsalinada.save()

            #Se guarda la cantidad final en la bodega de taller
            bodegaEnsalinado = ProductoBodega.objects.get(bodega = 6,producto = piernaEnsalinada.codigoProducto)
            bodegaEnsalinado.pesoProductoStock += ensalinado.pesoProductoDespues * 1000
            bodegaEnsalinado.save()

            #se resta la cantidad de Carne que se utilizo para el ensalinado
            bodegaProductoAntes = ProductoBodega.objects.get(bodega = 6, producto = producto.codigoProducto)
            bodegaProductoAntes.pesoProductoStock -= ensalinado.pesoProductoAntes * 1000
            bodegaProductoAntes.save()


            #Se guarda la cantidad a restar para la sal

            salBodega.pesoProductoStock -= ensalinado.pesoSal
            salBodega.save()

            #Se guarda la cantidad a restar para la Papaina

            PapainaBodega.pesoProductoStock -= ensalinado.pesoPapaina
            PapainaBodega.save()


            return HttpResponseRedirect('/fabricacion/ensalinados/')
    else:
        formulario = EnsalinadoForm()

    return render_to_response('Fabricacion/GestionEnsalinados.html',{'formulario':formulario,'ensalinados':ensalinados },
                              context_instance = RequestContext(request))

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

    mod = ValoresCostos.objects.get(nombreCosto = 'Costo Condimento').valorMod
    cif = ValoresCostos.objects.get(nombreCosto = 'Costo Condimento').valorCif
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

    pesoMigaProcesada = miga.PesoFormulaMiga
    costoInsumos = 0

    for costo in detallesMiga:
        costoInsumos += costo.costoTotalProducto

    mod = ValoresCostos.objects.get( nombreCosto= 'Costos Miga').valorMod
    cif = ValoresCostos.objects.get( nombreCosto= 'Costos Miga').valorCif
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


def GestionApanado(request,idprodbod):

    bodegaFilete = ProductoBodega.objects.get(pk = idprodbod)
    apanados = Apanado.objects.filter(producto = bodegaFilete.producto.codigoProducto )
    miga = Producto.objects.get(nombreProducto = 'Miga')
    Huevos = Producto.objects.get(nombreProducto = 'Huevos')
    filete = Producto.objects.get(nombreProducto = 'Filete Condimentado')
    fileteApanado =  Producto.objects.get(nombreProducto = 'Filete Apanado')
    bodegaHuevos = ProductoBodega.objects.get(bodega = 6, producto = Huevos.codigoProducto)
    bodegaMiga = ProductoBodega.objects.get(bodega = 6 , producto = miga.codigoProducto)
    bodegaFileteApanado = ProductoBodega.objects.get(bodega = 5 , producto = fileteApanado.codigoProducto)

    if request.method == 'POST':
        formulario = ApanadoForm(request.POST)
        if formulario.is_valid():
            apanado = formulario.save()

            CostoTotalMiga = miga.costoProducto * apanado.miga
            CostoTotalHuevos = Huevos.costoProducto * apanado.huevos
            CostoTotalFilete = filete.costoProducto * apanado.pesoFilete

            CostoFiletePorApanar = CostoTotalMiga + CostoTotalFilete + CostoTotalHuevos

            mod = Decimal(0.096) * apanado.totalApanado
            cif= Decimal(0.134) * apanado.totalApanado

            costoFileteApanado = CostoFiletePorApanar + mod + cif
            costoKiloApanado = costoFileteApanado / apanado.totalApanado

            #Guardamos  los calculos realizados
            apanado.costoKiloApanado = costoKiloApanado
            apanado.save()

            #Restamos la cantidad de productos usados en el proceso

            bodegaFilete.pesoProductoStock -= apanado.pesoFilete
            bodegaFilete.save()

            bodegaHuevos.unidadesStock -= apanado.huevos
            bodegaHuevos.save()

            bodegaMiga.pesoProductoStock -= apanado.miga
            bodegaMiga.save()

            #Guardamos el costo del Kilo del Filete Apanado
            fileteApanado.costoProducto = costoKiloApanado
            fileteApanado.save()

            #Guardamos la cantidad de filete apanado
            bodegaFileteApanado.pesoProductoStock = apanado.totalApanado
            bodegaFileteApanado.save()

            return HttpResponseRedirect('/fabricacion/apanado/'+idprodbod)
    else:
        #Se Setea el valor inicial del formulario con las cantidades existentes
        formulario = ApanadoForm(initial={'producto':bodegaFilete.producto.codigoProducto,
                                          'pesoFilete':bodegaFilete.pesoProductoStock,
                                          'huevos':bodegaHuevos.unidadesStock,
                                          'miga':bodegaMiga.pesoProductoStock})

    return render_to_response('Fabricacion/GestionApanado.html',{'formulario':formulario, 'apanados': apanados},
                              context_instance = RequestContext(request))

def GestionarTajadoCondPechugas(request,idprodbod):
    bodegaPechuga = ProductoBodega.objects.get(pk = idprodbod)
    registros = CondimentadoTajadoPechuga.objects.filter(producto = bodegaPechuga.producto.codigoProducto)
    fileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de Pollo Condimentado')
    hueso = Producto.objects.get(nombreProducto = 'Hueso de pollo')
    piel = Producto.objects.get(nombreProducto = 'Piel')
    procesos = Producto.objects.get(nombreProducto = 'Procesos de pollo')
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    if request.method == 'POST':
        formulario = CondTajPechugasForm(request.POST)
        if formulario.is_valid():
            tajado = formulario.save()

            compra = Compra.objects.get(pk = tajado.compra)
            costoKiloDescongelado = (tajado.PesoDescongelado / 1000) / compra.vrCompra
            costoPechugaAProcesar = costoKiloDescongelado * tajado.PesoDescongelado
            mod = Decimal(0.161) * tajado.PesoDescongelado
            cif = Decimal(0.131) * tajado.PesoDescongelado
            costoTotalPechuga = costoPechugaAProcesar + mod + cif
            totalFileteTajado = tajado.fileteACond + tajado.fileteAApanar

            costoFilete = costoTotalPechuga * Decimal(0.95)
            costoHueso = costoTotalPechuga * hueso.porcentajeCalidad
            costoPiel = costoTotalPechuga * piel.porcentajeCalidad
            costoProcesos = costoTotalPechuga * procesos.porcentajeCalidad
            costoTotalCondimento = tajado.condimento * condimento.costoProducto
            costoTotalCondimentoApanar = tajado.condimentoAP * condimento.costoProducto

            #calculamos el costo por kilo de cada producto obtenido
            costoKiloFilete = costoFilete / totalFileteTajado
            costoKiloHueso = costoHueso / tajado.huesos
            costoKiloPiel = costoPiel / tajado.piel
            costoKiloProcesos = costoProcesos/ tajado.procesos

            #Calculamos el filete que se va a condimentar
            costoFileteACondimentar = costoKiloFilete * tajado.fileteACond
            costoFileteCondimentado = costoFileteACondimentar + costoTotalCondimento
            costoKiloFileteCondimentado = costoFileteCondimentado / tajado.fileteACond

            #Calculamos el Filete que se va a Apanar

            costoFileteAcondApanado = costoFilete * tajado.fileteAApanar
            costoFileteCondimentadoApanar = costoFileteAcondApanado + costoTotalCondimentoApanar
            costoKiloFileteCondApanar = costoFileteCondimentadoApanar / tajado.tajado.fileteAApanar


            #Guardamos los costo del filete condimentado para venta
            fileteCondimentado.costoProducto = costoKiloFileteCondimentado
            fileteCondimentado.save()

            #guardamos la cantidad de filete condimetado para la venta
            bodegaFileteCondimentado = ProductoBodega.objects.get(bodega = 5, producto = fileteCondimentado.codigoProducto )
            bodegaFileteCondimentado.pesoProductoStock = tajado.fileteACond + tajado.condimento
            bodegaFileteCondimentado.save()

            #obtenemos las bodegas de los subproductos
            bodegaHueso = ProductoBodega.objects.get(bodega = 5,producto = hueso.codigoProducto)
            bodegaPiel = ProductoBodega.objects.get(bodega = 5,producto = piel.codigoProducto)
            bodegaProcesos = ProductoBodega.objects.get(bodega = 5,producto = procesos.codigoProducto)

            #guardamos el costo y la cantidad de los  subproductos
            hueso.costoProducto = costoKiloHueso
            bodegaHueso.pesoProductoStock = tajado.huesos
            bodegaHueso.save()
            hueso.save()

            piel.costoProducto = costoKiloPiel
            bodegaPiel.pesoProductoStock = tajado.piel
            bodegaPiel.save()
            piel.save()

            procesos.costoProducto = costoKiloProcesos
            bodegaProcesos.pesoProductoStock = tajado.procesos
            bodegaProcesos.save()
            procesos.save()

            #Restamos la cantidad de pechuga utilizada
            bodegaPechuga.pesoProductoStock -= tajado.PesoDescongelado
            bodegaPechuga.save()

            #restamos la cantidad de condimento utilizada
            bodegaCondimento = ProductoBodega.objects.get(bodega = 6 , producto = condimento.codigoProducto)
            bodegaCondimento.pesoProductoStock -= tajado.condimento + tajado.condimentoAP
            bodegaCondimento.save()

            #pendiente  la vista para el apanado delFilete Condimentado

            return HttpResponseRedirect('/fabricacion/pechugas/'+idprodbod)
    else:
        formulario = CondTajPechugasForm(initial={'producto':bodegaPechuga.producto.codigoProducto})

    return render_to_response('Fabricacion/GestionTajaddoCondPechugas.html',{'formulario':formulario,'registros':registros}
                              ,context_instance = RequestContext(request))
#**********************************************PROCESO TAJADO **********************************************************

'''
def GestionCondTajado(request, idprodbod):
    condTajados  = CondimentadoTajado.objects.all()
    prodBod = ProductoBodega.objects.get(pk = idprodbod )
    producto = Producto.objects.get(pk = prodBod.producto.codigoProducto)
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    if request.method == 'POST':

        formulario = CondTajadoForm(request.POST)
        if formulario.is_valid():
            proceso = formulario.save()

            mod = Decimal(0.139) * prodBod.pesoProductoStock
            cif = Decimal(0.143) * prodBod.pesoProductoStock
            costoTotalACondimentar = producto.costoProducto + mod + cif

            costoFilete = costoTotalACondimentar * Decimal(0.973)
            costoRecortes = costoTotalACondimentar * Decimal(0.007)#Pendiente guardar en inventario
            costoProcesos = costoTotalACondimentar * Decimal(0.02)#Pendiente guardar en inventario

            costoKiloFilete = costoFilete / proceso.filete
            costoTotalFilete = proceso.filete * costoKiloFilete
            costoTotalCondimento = proceso.condimento * condimento.costoProducto
            costoFileteCondimentado = costoTotalFilete +  costoTotalCondimento
            pesoFileteCondimentado = proceso.filete + proceso.condimento
            costoKiloFileteCondimentado = costoFileteCondimentado / pesoFileteCondimentado


            #Promediamos el costo del filete y lo guardamos
            filete = Producto.objects.get(nombreProducto = 'Filete Condimentado')
            if filete.costoProducto == 0:
                filete.costoProducto = costoKiloFileteCondimentado
            else:
                costoKiloFiletePromedio = (costoKiloFileteCondimentado + filete.costoProducto)/2
                filete.costoProducto = costoKiloFiletePromedio

            filete.save()

            # Guardamos el la cantidad de producto condimentado en la bodega de la planta de procesos
            bodegaFilete = ProductoBodega.objects.get(bodega = 6 , producto = filete.codigoProducto)
            bodegaFilete.pesoProductoStock += pesoFileteCondimentado
            bodegaFilete.save()

            #Restamos la cantidad utilizada a la cantidad ensalinada
            prodBod.pesoProductoStock -= proceso.pesoProductoEnsalinado
            prodBod.save()


            return HttpResponseRedirect('/fabricacion/condtaj/'+ idprodbod)
    else:
        formulario = CondTajadoForm(initial={'producto':producto.codigoProducto,'pesoProductoEnsalinado':prodBod.pesoProductoStock})

    return render_to_response('Fabricacion/GestionCondTajado.html',{'formulario':formulario,'condTajados':condTajados },
                              context_instance = RequestContext(request))
'''

def GestionTajado(request):
    exito = True
    tajados = Tajado.objects.all()

    if request.method == 'POST':

        formulario = TajadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            #guardar cantidad de producto en bodega producto tajado
            #restar la cantidad de producto utilizada
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

def TraerCosto(request):
    idDesposte = request.GET.get('desposte')
    idProducto= request.GET.get(('producto'))
    desposte = DetallePlanilla.objects.get(planilla = int(idDesposte),producto = int(idProducto)).costoProducto

    respuesta = json.dumps(desposte)

    return HttpResponse(respuesta,mimetype='application/json')

def costearTajado(request):
    idTajado = request.GET.get('idTajado')
    tipo = request.GET.get('tipo')
    detTajado = DetalleTajado.objects.filter(tajado = int(idTajado))
    tajado = Tajado.objects.get(pk = int(idTajado) )
    mod = 0
    cif = 0
    costokilo = 0
    if tipo == 'Cerdos':
        mod = ValoresCostos.objects.get(nombreCosto = 'Costo Tajado Cerdo').valorMod
        cif = ValoresCostos.objects.get(nombreCosto = 'Costo Tajado Cerdo').valorCif
    elif tipo == 'Cerdas':
        mod = ValoresCostos.objects.get(nombreCosto = 'Costo Tajado Cerda').valorMod
        cif = ValoresCostos.objects.get(nombreCosto = 'Costo Tajado Cerda').valorCif
    elif tipo == 'Pollo':
        mod = ValoresCostos.objects.get(nombreCosto = 'Costo Tajado Pollo').valorMod
        cif = ValoresCostos.objects.get(nombreCosto = 'Costo Tajado Pollo').valorCif

    tajado.cif = cif
    tajado.mod = mod
    tajado.save()


    costoTotal = ((tajado.pesoProducto)/1000) * tajado.costoKiloFilete + mod + cif

    if tipo == 'Cerdos' or tipo == 'Cerdas':
        #milanesa 98.5% ,  Recortes 0,5% ,  Procesos 1%
        for tjdo in detTajado:
            producto = Producto.objects.get(pk = tjdo.producto.codigoProducto)

            if tjdo.producto.nombreProducto == 'Filete de Cerd@':
                tjdo.costoKilo = (costoTotal * Decimal(0.985))/(tjdo.pesoProducto /1000)
                costokilo = tjdo.costoKilo
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
    bodegaTajado = ProductoBodega.objects.get(bodega = 5, producto = tajado.producto.codigoProducto)
    bodegaTajado.pesoProductoStock -= tajado.pesoProducto
    bodegaTajado.save()



    for det in detTajado:

        #Guardamos el producto resultante
        bodega = ProductoBodega.objects.get(bodega = 6,producto =  det.producto.codigoProducto)
        bodega.unidadesStock += det.unidades
        bodega.pesoProductoStock += det.pesoProducto
        bodega.save()

    tajado.guardado = True

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

def GestionDesposteActualizado(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

    #Filtramos los despostes en grupos para su posterior costeo
    carnes = detalleDespostes.filter(grupo = 'Grupo Carnes')
    carnes2 = detalleDespostes.filter(grupo = 'Grupo Carnes 2')
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
    pesoCostillas = 0
    pesoHuesos = 0
    pesoSubProd = 0
    pesoDesecho = 0
    perdidaPeso= 0


    for peso in carnes:
        pesoCarnes += peso.PesoProducto
    for peso in carnes2:
        pesoCarnes2 += peso.PesoProducto
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

    pesoTotalDesposte = pesoCarnes +pesoCarnes2+ pesoCostillas + pesoHuesos + pesoSubProd + pesoDesecho

    #el valor total de los canales a despostar se calcula con el peso de canales y el valor del kilo en canal
    vrTotalCanales = pesoCanales * vrKiloCanal

    # calculamos el valor de cada grupo multiplicando el %Grupo por el vrTotalCanales
    if tipoDesposte == 'Cerdos':
        vrCarnes = ceil((vrTotalCanales * 57)/100)
        vrCarnes2 = ceil((vrTotalCanales * 17)/100)
        vrCostillas = ceil((vrTotalCanales * 15)/100)
        vrHuesos = 0
        vrsubProd = ceil((vrTotalCanales * 10)/100)
        vrDesecho = ceil((vrTotalCanales * 1)/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido

    elif tipoDesposte == 'Cerdas':
        vrCarnes = ceil((vrTotalCanales * 49)/100)
        vrCarnes2 = ceil((vrTotalCanales * 22)/100)
        vrCostillas = ceil((vrTotalCanales * 11)/100)
        vrHuesos = ceil((vrTotalCanales * 6)/100)
        vrsubProd = ceil((vrTotalCanales * 8)/100)
        vrDesecho = ceil((vrTotalCanales * 2)/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido
    else:
        vrCarnes = ceil((vrTotalCanales * 42)/100)
        vrCarnes2 = ceil((vrTotalCanales * 33)/100)
        vrCostillas = ceil((vrTotalCanales * 10)/100)
        vrHuesos = ceil((vrTotalCanales * 6)/100)
        vrsubProd = ceil((vrTotalCanales * 7)/100)
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
        formulario = DetalleDesposteForm(request.POST)

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
        formulario = DetalleDesposteForm(initial={'planilla':idplanilla})

    contexto = {'vrKiloCarnes2':vrKiloCarnes2,'vrKiloCarnes':vrKiloCarnes,'vrKiloCostillas':vrKiloCostillas,'vrKiloHuesos':vrKiloHuesos,
                'vrKiloSubProd':vrKiloSubProd,'vrKiloDesecho':vrKiloDesecho,'carnes2':carnes2,'carnes':carnes,'costillas':costillas,
                'huesos':huesos,'subProductos':subProductos,'desechos':desechos,'formulario':formulario,'desposte':desposte,
                'canales':canales,'detalleDespostes':detalleDespostes,'vrCarnes':vrCarnes,'vrCarnes2':vrCarnes2,'vrCostillas':vrCostillas,
                'vrHuesos':vrHuesos,'vrsubProd':vrsubProd,'vrDesecho':vrDesecho}

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

    Mod = 0
    Cif = 0


    if tipoCompra == 'Reses':
        Cif = ValoresCostos.objects.get(nombreCosto = 'Costo Desposte Reses').valorCif
        Mod = ValoresCostos.objects.get(nombreCosto = 'Costo Desposte Reses').valorMod

    if tipoCompra == 'Cerdos':
        Cif = ValoresCostos.objects.get(nombreCosto = 'Costo Desposte Cerdo').valorCif
        Mod = ValoresCostos.objects.get(nombreCosto = 'Costo Desposte Cerdo').valorMod
    if tipoCompra == 'Cerdas':
        Cif = ValoresCostos.objects.get(nombreCosto = 'Costos Cerdas').valorCif
        Mod = ValoresCostos.objects.get(nombreCosto = 'Costos Cerdas').valorMod



    #traemos via JSON todas las variables de la plantilla
    pesoCanales = request.GET.get('pesoCanales')
    pesoCanales = int(pesoCanales)*1000
    cantProductos = detalleDesposte.count()
    cif = Cif / cantProductos
    costoKilo = 0


    kiloCarnes = request.GET.get('kiloCarnes')
    kiloCarnes2 = request.GET.get('kiloCarnes2')
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
    costillas = detalleDespostes.filter(grupo = 'Grupo Costillas')
    huesos = detalleDespostes.filter(grupo = 'Grupo Huesos')
    subProductos = detalleDespostes.filter(grupo = 'Grupo SubProductos')
    desechos = detalleDespostes.filter(grupo = 'Grupo Desechos')

    if request.method == 'POST':
        formulario = DetalleDesposteForm(request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/detalleDesposte/'+ str(idplanilla))
    else:
        formulario = DetalleDesposteForm(instance=detalle)

    contexto = {'carnes2':carnes2,'carnes':carnes,'costillas':costillas,'huesos':huesos,'subProductos':subProductos,
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

                cif = ValoresCostos.objects.get(nombreCosto = 'Costos Descarne Cerdo').valorCif
                mod = ValoresCostos.objects.get(nombreCosto = 'Costos Descarne Cerdo').valorMod
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

                cif = ValoresCostos.objects.get(nombreCosto = 'Costos Descarne Cerda').valorCif
                mod = ValoresCostos.objects.get(nombreCosto = 'Costos Descarne Cerda').valorMod
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

            descarne.cif = cif
            descarne.mod = mod
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

    respuesta  = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')
