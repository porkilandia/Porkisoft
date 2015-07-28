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
from Ventas.models import *

def configuracionDesposteTemplate(request):
    grupos = Grupo.objects.select_related()

    return render_to_response('Fabricacion/configuracionDespostes.html',{'grupos':grupos},context_instance = RequestContext(request))

def configuracionDespostes (request):
    pass

#******************************************************CANAL***********************************************************
def GestionCanal(request,idrecepcion):

    canales = Canal.objects.select_related().filter(recepcion = idrecepcion).order_by('nroCanal')#para renderizar las listas
    recepcion = PlanillaRecepcion.objects.select_related().get(pk = idrecepcion)
    #compra = Compra.objects.get(pk = recepcion.compra.codigoCompra)
    #sacrificio = Sacrificio.objects.get(recepcion = idrecepcion)
    cantidad = canales.count() +1
    kiloCanal = 0

    nroCanal = 0 #Representa el numero de canal actual
    for can in canales :
        kiloCanal = can.vrKiloCanal
        nroCanal = can.nroCanal

    canalMuestra = Canal.objects.filter(recepcion = idrecepcion)
    PesoTotalCanales= 0

    for cnl in canalMuestra:#Calcula en cada ingreso el peso total hasta el momento
        PesoTotalCanales += cnl.pesoPorkilandia

    recepcion.pesoCanales = PesoTotalCanales
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

            for canale in canales:#Calcula en cada ingreso el peso total hasta el momento
                    pesoCanales += canale.pesoPorkilandia

            canal = Canal()
            canal.recepcion = recepcion
            #canal.planilla = planilla
            canal.pesoFrigovito = request.POST.get('pesoFrigovito')
            canal.pesoPorkilandia = request.POST.get('pesoPorkilandia')
            canal.difPesos = request.POST.get('difPesos')
            canal.genero = request.POST.get('genero')
            canal.nroCanal = request.POST.get('nroCanal')

            #Se calculan datos adicionales para eliminar el sacrificio
            #recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
            cantCabezas = recepcion.cantCabezas
            menudo = cantCabezas * 90000
            deguello = cantCabezas * 90150
            if recepcion.transporte == 'Particular':
                trans = 0
            else:
                trans = cantCabezas * 8000

            if recepcion.compra.tipo.nombreGrupo == 'Reses':

                vrKiloCanal = ((recepcion.compra.vrCompra + deguello + trans))/ (pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))

                vrArrobaCanal = vrKiloCanal * Decimal(12.5)

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal
                vrFactura = recepcion.compra.vrCompra
                transporte = trans

            elif recepcion.compra.tipo.nombreGrupo == 'Cerdos':

                menudo = 7000 * cantidad
                flete = 500000
                transporte = trans * cantidad
                deguello = 39500 * cantidad

                if pesoCanales == 0:#para cuando se ingresa la primera vez
                    pesoCanales = 1000


                pesoPorkilandia = Decimal(request.POST.get('pesoPorkilandia'))
                costoKilocerdo = ValoresCostos.objects.get(nombreCosto = 'Costo Cerdo')
                vrFactura = (pesoCanales + pesoPorkilandia) * costoKilocerdo.valorKiloPie #--> 6050 es el valor establecido por granjas el paraiso
                pesoPie = Decimal(ceil(pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))) / (Decimal(0.82))
                vrFactPie = (vrFactura - deguello - flete) + menudo
                costoCanales = (vrFactPie + deguello + flete + transporte) - menudo
                vrKiloCanal = ceil(costoCanales / (pesoCanales + pesoPorkilandia))
                vrArrobaCanal = vrKiloCanal * 12.5

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal

            else:
                menudo = 12000 * cantidad
                transporte = 9000* cantidad
                deguello = 51700 * cantidad
                pesoPorkilandia = Decimal(request.POST.get('pesoPorkilandia'))
                cantidadCanalCerdasGrandes = Canal.objects.filter(recepcion = idrecepcion,pesoPorkilandia__gt = 0)# busca registros que el peso sea mayor o igual a 150
                costosCerdas = ValoresCostos.objects.get(nombreCosto = 'Costos Cerdas')

                incrementoCG = costosCerdas.valorMod * cantidadCanalCerdasGrandes.count()

                if pesoPorkilandia >= 0:
                    incrementoCG += costosCerdas.valorMod

                if pesoCanales == 0:#para cuando se ingresa la primera vez
                    pesoCanales = 1

                pesoPie = pesoCanales + pesoPorkilandia + Decimal(incrementoCG) # + incrementoCP
                vrFactura = pesoPie * costosCerdas.valorKiloPie
                costoCanales = (vrFactura + deguello + transporte) - menudo
                vrKiloCanal = ceil(costoCanales / (pesoCanales + pesoPorkilandia))
                vrArrobaCanal = vrKiloCanal * 12.5

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal

            #Se graba el vr del transporte
            recepcion.vrTransporte = transporte

            #se graba el valor de la factura
            recepcion.compra.vrCompra = vrFactura
            recepcion.compra.save()
            # se guarda el canal
            canal.save()

            # Se guarda informacion adicional en el modelo recepcion

            PesoTotalCanales = 0
            TotalPesoPie = 0
            canal = Canal.objects.filter(recepcion = idrecepcion)
            detCompra = DetalleCompra.objects.filter(compra = recepcion.compra.codigoCompra)

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

def BorrarCanal(request, idcanal):

    canal = Canal.objects.get(pk=idcanal)
    recepcion = PlanillaRecepcion.objects.get(pk = canal.recepcion.codigoRecepcion)
    canales = Canal.objects.filter(recepcion = recepcion.codigoRecepcion)
    canal.delete()
    return HttpResponseRedirect('/fabricacion/canal/'+ str(recepcion.codigoRecepcion))

def MarcarCanalDesposte(request, idcanal):

    canal = Canal.objects.get(pk=idcanal)
    recepcion = PlanillaRecepcion.objects.get(pk = canal.recepcion.codigoRecepcion)
    desposte = PlanillaDesposte.objects.get(tipoDesposte = '')

    if canal.estado == True:
        canal.planilla = None
        canal.estado = False
        canal.save()
    else:
        canal.planilla = desposte
        canal.estado = True
        canal.save()

    return HttpResponseRedirect('/fabricacion/canal/'+ str(recepcion.codigoRecepcion))


def GestionSacrificio(request,idrecepcion):

    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    sacrificios = Sacrificio.objects.filter(recepcion = idrecepcion)
    detCompra = DetalleCompra.objects.filter(compra = recepcion.compra.codigoCompra)

    #totalPieles = 0

    for det in detCompra:
        ganado = Ganado.objects.get(pk = det.ganado.codigoGanado)
        #totalPieles += ganado.piel

    if request.method == 'POST':
        formSacrificio = SacrificioForm(request.POST)

        if formSacrificio.is_valid():
            sacrificio = formSacrificio.save()

            cantCabezas = recepcion.cantCabezas

            menudo = cantCabezas * 90000
            deguello = cantCabezas * 90150
            if recepcion.transporte == 'Particular':
                transporte = 0
            else:
                transporte = cantCabezas * 8000

            sacrificio.recepcion = recepcion
            sacrificio.piel = 0
            sacrificio.vrMenudo = menudo
            sacrificio.vrDeguello = deguello
            sacrificio.vrTransporte = transporte
            sacrificio.save()

            prodLimpieza = ['Cola','Rinones','Creadillas','Recortes Sacrificio','Ubre' ]
            item = ['cola','rinones','creadillas','recortes','ubre']
            cont = 0

            for productos  in prodLimpieza:

                producto = Producto.objects.get(nombreProducto = productos )
                existencia = ProductoBodega.objects.get(producto = producto.codigoProducto , bodega = 5)

                existencia.producto = producto
                existencia.pesoProductoStock += existencia.pesoProductoStock + Decimal(request.POST.get(item[cont]))
                existencia.save()

                cont += 1
            return HttpResponseRedirect('/fabricacion/sacrificio/'+idrecepcion)

    else:
        formSacrificio = SacrificioForm(initial={'recepcion':idrecepcion})

    return render_to_response('Fabricacion/GestionSacrificio.html',{'formSacrificio':formSacrificio,
                                                                   'sacrificios':sacrificios},
                              context_instance = RequestContext(request))

def GestionEnsalinado(request):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    ensalinados = Ensalinado.objects.filter(fechaEnsalinado__range =(fechainicio,fechafin))
    #ensalinados = Ensalinado.objects.all()
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

    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    ensalinados = Ensalinado.objects.filter(fechaEnsalinado__range =(fechainicio,fechafin))
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
    movimientos = Movimientos()
    movimientos.tipo = 'ENS%d'%(ensalinado.codigoEnsalinado)
    movimientos.fechaMov = ensalinado.fechaEnsalinado

    if producto.grupo.nombreGrupo == 'Cerdas':
        piernaEnsalinada = Producto.objects.get(nombreProducto = 'Pierna Ensalinada')
        piernaEnsalinada.costoProducto = costoKilo
        piernaEnsalinada.save()
        bodegaEnsalinado = ProductoBodega.objects.get(bodega = 6,producto = piernaEnsalinada.codigoProducto)
        bodegaEnsalinado.pesoProductoStock += ensalinado.pesoProductoDespues
        movimientos.productoMov = piernaEnsalinada
        movimientos.nombreProd = piernaEnsalinada.nombreProducto
    else:
        BolaEnsalinada = Producto.objects.get(nombreProducto = 'Bola Ensalinada')
        BolaEnsalinada.costoProducto = costoKilo
        BolaEnsalinada.save()
        bodegaEnsalinado = ProductoBodega.objects.get(bodega = 6,producto = BolaEnsalinada.codigoProducto)
        movimientos.productoMov = BolaEnsalinada
        movimientos.nombreProd = BolaEnsalinada.nombreProducto

    movimientos.entrada = ensalinado.pesoProductoDespues
    movimientos.save()
    bodegaEnsalinado.pesoProductoStock += ensalinado.pesoProductoDespues
    bodegaEnsalinado.save()

    #se resta la cantidad de Carne que se utilizo para el ensalinado
    movimientos = Movimientos()
    movimientos.tipo = 'ENS%d'%(ensalinado.codigoEnsalinado)
    movimientos.fechaMov = ensalinado.fechaEnsalinado
    movimientos.productoMov = producto
    movimientos.nombreProd = producto.nombreProducto
    movimientos.salida = ensalinado.pesoProducto
    movimientos.save()

    bodegaProductoAntes = ProductoBodega.objects.get(bodega = 5, producto = producto.codigoProducto)
    bodegaProductoAntes.pesoProductoStock -= ensalinado.pesoProductoAntes
    bodegaProductoAntes.save()


    #Se guarda la cantidad a restar para la sal
    movimientos = Movimientos()
    movimientos.tipo = 'ENS%d'%(ensalinado.codigoEnsalinado)
    movimientos.fechaMov = ensalinado.fechaEnsalinado
    movimientos.productoMov = sal
    movimientos.nombreProd = sal.nombreProducto
    movimientos.salida = ensalinado.pesoSal
    movimientos.save()

    salBodega.pesoProductoStock -= ensalinado.pesoSal
    salBodega.save()

    #Se guarda la cantidad a restar para la Papaina
    movimientos = Movimientos()
    movimientos.tipo = 'ENS%d'%(ensalinado.codigoEnsalinado)
    movimientos.fechaMov = ensalinado.fechaEnsalinado
    movimientos.productoMov = papaina
    movimientos.nombreProd = papaina.nombreProducto
    movimientos.salida = ensalinado.pesoPapaina
    movimientos.save()

    PapainaBodega.pesoProductoStock -= ensalinado.pesoPapaina
    PapainaBodega.save()

    respuesta = json.dumps('Guardado Exitoso!!')
    return HttpResponse(respuesta,mimetype='application/json')

def GestionVerduras(request):

    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    verduras = LimpiezaVerduras.objects.filter(fechaLimpieza__range =(fechainicio,fechafin))

    if request.method == 'POST':

        formulario = LimpiezaVerdurasForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/verduras/')
    else:
        formulario = LimpiezaVerdurasForm()

    return render_to_response('Fabricacion/GestionVerduras.html',{'formulario':formulario,'verduras':verduras},
                              context_instance = RequestContext(request))

def borrarVerduras(request,idVerduras):
    verduras = LimpiezaVerduras.objects.select_related().get(pk = idVerduras)
    verduras.delete()
    return HttpResponseRedirect('/fabricacion/verduras/')

def ValorVerduras(request):
    idCompra = request.GET.get('idCompra')
    idProducto = request.GET.get('idProducto')
    compra = Compra.objects.get(pk = int(idCompra))
    detalleCompra = DetalleCompra.objects.get(compra = compra.codigoCompra,producto = int(idProducto))
    valorProducto = {}
    valorTransporte = {}
    valorProducto['Valor Producto'] = detalleCompra.subtotal
    valorTransporte['Valor Transporte'] = compra.vrTransporte
    lista = {'valorProducto':valorProducto,'valorTransporte':valorTransporte}
    respuesta = json.dumps(lista)
    return HttpResponse(respuesta,mimetype='application/json')

def CostearVerduras(request):
    idLimpieza = request.GET.get('idVerdura')
    limpieza = LimpiezaVerduras.objects.get(pk = int(idLimpieza))
    detalleCompra = DetalleCompra.objects.filter(compra = limpieza.compra.codigoCompra)
    pesoTotal = 0

    for detalle in detalleCompra:
        pesoTotal += detalle.pesoProducto

    producto = Producto.objects.get(pk = limpieza.productoLimpiar.codigoProducto)

    vrCompra = limpieza.valorProducto
    porcentajeTransporte = ((limpieza.pesoProducto * 100) /pesoTotal)/100
    transporte = limpieza.valorTransporte * porcentajeTransporte
    mod = limpieza.mod
    cif = limpieza.cif
    costo = vrCompra + cif + mod + transporte
    costoKilo = ceil(costo / (limpieza.pesoProducto / 1000 ))

    #Se guarda el costo de la verdura limpia
    limpieza.vrKilo = costoKilo
    limpieza.save()
    #guardamos el costo del producto
    producto.costoProducto = costoKilo
    producto.save()

    msj = 'Costeado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GuardarVerduras(request):
    idLimpieza = request.GET.get('idVerdura')
    limpieza = LimpiezaVerduras.objects.get(pk = int(idLimpieza))

    productoAntes = ProductoBodega.objects.get(bodega = 6,producto = limpieza.productoLimpiar.codigoProducto)
    productoLimpio = ProductoBodega.objects.get(bodega = 6,producto = limpieza.productoLimpiar.codigoProducto)

    productoAntes.pesoProductoStock -= limpieza.pesoProducto
    productoAntes.save()

    productoLimpio.pesoProductoStock += limpieza.pesoDespues
    productoLimpio.save()

    limpieza.guardado = True
    limpieza.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionCondimento(request):

    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    condimentos = Condimento.objects.filter(fecha__range =(fechainicio,fechafin))

    if request.method == 'POST':

        formulario = CondimentoForm(request.POST)
        if formulario.is_valid():
            condimento = formulario.save()

            #Guardamos el condimento producido en Bodega
            bodega = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto = 'Condimento Natural')
            bodega.pesoProductoStock += condimento.pesoCondimento
            bodega.save()

            movimientos = Movimientos()
            movimientos.tipo = 'COND%d'%(condimento.codigoCondimento)
            movimientos.fechaMov = condimento.fecha
            movimientos.productoMov = bodega.producto
            movimientos.nombreProd = bodega.producto.nombreProducto
            movimientos.Hasta = bodega.bodega.nombreBodega
            movimientos.save()

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

            movimientos = Movimientos()
            movimientos.tipo = 'COND%d'%(condimento.codigoCondimento)
            movimientos.fechaMov = condimento.fecha
            movimientos.productoMov = producto
            movimientos.nombreProd = producto.nombreProducto
            movimientos.salida = detalle.pesoProducto * condimento.cantFormulas
            movimientos.desde = bodega.bodega.nombreBodega
            movimientos.save()


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
    condimento.guardado = True
    condimento.save()

    producto = Producto.objects.get(nombreProducto = 'Condimento Natural')
    producto.costoProducto = costoLitroCond
    producto.save()

    return render_to_response('Fabricacion/GestionDetalleCondimento.html',{'formulario':formulario,
                                                                   'condimento': condimento,'idcondimento':idcondimento,
                                                                   'detalleCondimentos':detalleCondimentos },
                              context_instance = RequestContext(request))



#******************************************************* MIGA***********************************************************

def GestionMiga(request):
    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    migas  = Miga.objects.filter(fechaFabricacion__range =(fechainicio,fechafin))

    if request.method == 'POST':

        formulario = MigaForm(request.POST)
        if formulario.is_valid():
            miga = formulario.save()

            #miga.PesoFormulaMiga /= 1000
            #miga.save()

            return HttpResponseRedirect('/fabricacion/miga')
    else:
        formulario = MigaForm()

    return render_to_response('Fabricacion/GestionMiga.html',{'formulario':formulario,'migas':migas },
                              context_instance = RequestContext(request))
def EditaMiga(request,idMiga):
    migas  = Miga.objects.all()
    miga = Miga.objects.get(pk = idMiga)

    if request.method == 'POST':

        formulario = MigaForm(request.POST,instance=miga)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/miga')
    else:
        formulario = MigaForm(instance=miga)

    return render_to_response('Fabricacion/GestionMiga.html',{'formulario':formulario,'migas':migas },
                              context_instance = RequestContext(request))
def BorrarMiga(request,idMiga):
    miga = Miga.objects.get(pk = idMiga)
    miga.delete()
    return HttpResponseRedirect('/fabricacion/miga')


def GestionDetalleMiga(request,idmiga):
    miga = Miga.objects.get(pk = idmiga)
    detallesMiga = DetalleMiga.objects.filter(miga = idmiga)

    if request.method == 'POST':

        formulario = DetalleMigaForm(request.POST)
        if formulario.is_valid():
            detalle =  formulario.save()

            return HttpResponseRedirect('/fabricacion/detallemiga/'+ idmiga)
    else:
        formulario = DetalleMigaForm(initial={'miga':idmiga})

    return render_to_response('Fabricacion/GestionDetalleMiga.html',{'formulario':formulario,'miga':miga,
                                                                           'detallesMiga':detallesMiga,'idmiga':idmiga },
                              context_instance = RequestContext(request))

def GuardarMiga(request):
    idMiga = request.GET.get('IdMiga')
    miga = Miga.objects.get(pk = int(idMiga))
    detalleMiga = DetalleMiga.objects.filter(miga = int(idMiga))

    #Guardamos la cantidad de producto procesado en la bodega de planta de procesos
    bodegaMiga = ProductoBodega.objects.get(bodega = 5, producto__nombreProducto = 'Miga Preparada' )
    bodegaMiga.pesoProductoStock += miga.PesoFormulaMiga
    bodegaMiga.save()

    movimientos = Movimientos()
    movimientos.tipo = 'MGA%d'%(miga.codigoMiga)
    movimientos.fechaMov = miga.fechaFabricacion
    movimientos.nombreProd = bodegaMiga.producto.nombreProducto
    movimientos.productoMov = bodegaMiga.producto
    movimientos.entrada = miga.PesoFormulaMiga
    movimientos.save()

    for detalle in detalleMiga:
        # Se resta la cantidad de producrto utilizado en las formulas de condimento y se graba el registro
        bodega = ProductoBodega.objects.get(bodega = 6, producto = detalle.productoMiga.codigoProducto)
        bodega.pesoProductoStock -= (detalle.PesoProducto * miga.cantidadFormulas)
        bodega.save()

        movimientos = Movimientos()
        movimientos.tipo = 'MGA%d'%(miga.codigoMiga)
        movimientos.fechaMov = miga.fechaFabricacion
        movimientos.productoMov = detalle.productoMiga
        movimientos.nombreProd = detalle.productoMiga.nombreProducto
        movimientos.salida = detalle.PesoProducto
        movimientos.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')


def CostoMiga(request,idmiga):

    miga = Miga.objects.get(pk = idmiga)
    detallesMiga = DetalleMiga.objects.filter(miga = idmiga)
    formulario = DetalleMigaForm(initial={'miga':idmiga})

    pesoMigaProcesada = miga.PesoFormulaMiga / 1000
    costoInsumos = 0

    for costo in detallesMiga:
        costo.costoProducto = costo.productoMiga.costoProducto
        costo.costoTotalProducto = costo.productoMiga.costoProducto * (costo.PesoProducto/1000)
        costo.save()
        costoInsumos += costo.costoTotalProducto

    mod = miga.mod
    cif = miga.cif
    costomigaProsecesada = (costoInsumos * miga.cantidadFormulas) + cif + mod
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

def existenciasUnd(request):
    # Metodo que verifica las existencias de un producto determinado
    idProducto = request.GET.get('producto')
    idBodega = request.GET.get('bodega')
    unidades = request.GET.get('unidades')

    bodega = ProductoBodega.objects.get(bodega =  int(idBodega),producto = int(idProducto))

    if int(unidades) <= bodega.unidadesStock:
        msj = ''
    else:
        msj = 'No se puede usar esa cantidad ; La cantidad disponible de %s es: %s' % (bodega.producto.nombreProducto,str(bodega.unidadesStock))

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GestionApanado(request):

    fechainicio = date.today() - timedelta(days=8)
    fechafin = date.today()
    apanados = ProcesoApanado.objects.filter(fechaApanado__range =(fechainicio,fechafin))
    #apanados = ProcesoApanado.objects.all()

    if request.method == 'POST':
        formulario = ApanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/apanados')
    else:
        formulario = ApanadoForm()

    return render_to_response('Fabricacion/GestionApanado.html',{'formulario':formulario,'apanados':apanados },
                              context_instance = RequestContext(request))
def EditaApanado(request,idApanado):
    apanado = ProcesoApanado.objects.get(pk = idApanado)
    fechainicio = date.today() - timedelta(days=8)
    fechafin = date.today()
    apanados = ProcesoApanado.objects.filter(fechaApanado__range =(fechainicio,fechafin))
    #apanados = ProcesoApanado.objects.all()

    if request.method == 'POST':
        formulario = ApanadoForm(request.POST,instance=apanado)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/apanados')
    else:
        formulario = ApanadoForm(instance=apanado)

    return render_to_response('Fabricacion/GestionApanado.html',{'formulario':formulario,'apanados':apanados },
                              context_instance = RequestContext(request))
def GuardarApanado(request):

    idApanado = request.GET.get('idApanado')
    apanado = ProcesoApanado.objects.get(pk = int(idApanado))
    Filete = Producto.objects.get(pk = apanado.productoApanado.codigoProducto)

    bodegaFilete = ProductoBodega.objects.get(bodega = 5,producto = Filete.codigoProducto)
    bodegaMiga = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Miga Preparada')
    bodegaHuevos = ProductoBodega.objects.get(bodega = 6,producto__nombreProducto = 'Huevos')
    bodegaFileteApanadoCerdo = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Filete Apanado Cerdo')
    bodegaFileteApanadoPollo = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Filete Apanado Pollo')

    #guardamos las cantidades utilizadas de cada producto
    movimiento = Movimientos()
    movimiento.tipo = 'APA%d'%(apanado.id)
    movimiento.fechaMov = apanado.fechaApanado
    movimiento.productoMov = apanado.productoApanado
    movimiento.nombreProd = apanado.productoApanado.nombreProducto
    movimiento.salida = apanado.pesoFilete
    movimiento.save()
    bodegaFilete.pesoProductoStock -= apanado.pesoFilete

    movimiento = Movimientos()
    movimiento.tipo = 'APA%d'%(apanado.id)
    movimiento.fechaMov = apanado.fechaApanado
    movimiento.productoMov = bodegaMiga.producto
    movimiento.nombreProd = bodegaMiga.producto.nombreProducto
    movimiento.salida = apanado.miga
    movimiento.save()
    bodegaMiga.pesoProductoStock -= apanado.miga

    movimiento = Movimientos()
    movimiento.tipo = 'APA%d'%(apanado.id)
    movimiento.fechaMov = apanado.fechaApanado
    movimiento.productoMov = bodegaHuevos.producto
    movimiento.nombreProd = bodegaHuevos.producto.nombreProducto
    movimiento.salida = apanado.huevos
    movimiento.save()
    bodegaHuevos.pesoProductoStock -= apanado.huevos

    #guardamos las cantidades de producto resultante
    if apanado.productoApanado.grupo.nombreGrupo == 'Cerdos' or apanado.productoApanado.grupo.nombreGrupo == 'Cerdas':
        bodegaFileteApanadoCerdo.pesoProductoStock += apanado.totalApanado
        bodegaFileteApanadoCerdo.save()
        movimiento = Movimientos()
        movimiento.tipo = 'APA%d'%(apanado.id)
        movimiento.fechaMov = apanado.fechaApanado
        movimiento.productoMov = bodegaFileteApanadoCerdo.producto
        movimiento.nombreProd = bodegaFileteApanadoCerdo.producto.nombreProducto
        movimiento.entrada= apanado.totalApanado
        movimiento.save()
    else:
         bodegaFileteApanadoPollo.pesoProductoStock += apanado.totalApanado
         bodegaFileteApanadoPollo.save()
         movimiento = Movimientos()
         movimiento.tipo = 'APA%d'%(apanado.id)
         movimiento.fechaMov = apanado.fechaApanado
         movimiento.productoMov = bodegaFileteApanadoPollo.producto
         movimiento.nombreProd = bodegaFileteApanadoPollo.producto.nombreProducto
         movimiento.entrada= apanado.totalApanado
         movimiento.save()

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
    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    molidos = Molida.objects.filter(fechaMolido__range =(fechainicio,fechafin))
    #molidos = Molida.objects.all()

    if request.method == 'POST':
        formulario = MolidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/molida')
    else:
        formulario = MolidoForm()

    return render_to_response('Fabricacion/GestionMolida.html',{'formulario':formulario,'molidos':molidos },
                              context_instance = RequestContext(request))

def borrarMolida(request,idMolido):
    molido = Molida.objects.select_related().get(pk = idMolido)
    molido.delete()
    return HttpResponseRedirect('/fabricacion/molida')

def GuardarMolido(request):
    idMolido = request.GET.get('idMolido')
    molido = Molida.objects.get(pk = int(idMolido))
    bodegaProductoAMoler = ProductoBodega.objects.get(bodega = 5,producto = molido.productoMolido.codigoProducto)

    carneMolida = Producto.objects.get(nombreProducto = 'Carne Molida')
    carneMolidaCerdo = Producto.objects.get(nombreProducto = 'Carne molida cerdo')
    carneMolidaCerda = Producto.objects.get(nombreProducto = 'Carne molida cerda')

    bodegaProductoMolido = ProductoBodega.objects.get(bodega = 5,producto = carneMolida.codigoProducto)
    bodegaProductoMolidoCerdo = ProductoBodega.objects.get(bodega = 5,producto = carneMolidaCerdo.codigoProducto)
    bodegaProductoMolidoCerda = ProductoBodega.objects.get(bodega = 5,producto = carneMolidaCerda.codigoProducto)

    movimiento = Movimientos()
    movimiento.tipo = 'MOL%d'%(molido.id)
    movimiento.fechaMov = molido.fechaMolido
    movimiento.productoMov = molido.productoMolido
    movimiento.nombreProd = molido.productoMolido.nombreProducto
    movimiento.desde = bodegaProductoAMoler.bodega.nombreBodega
    movimiento.salida = molido.pesoAmoler
    movimiento.save()

    bodegaProductoAMoler.pesoProductoStock -= molido.pesoAmoler

    movimiento = Movimientos()
    movimiento.tipo = 'MOL%d'%(molido.id)
    movimiento.fechaMov = molido.fechaMolido

    if(molido.productoMolido.grupo.nombreGrupo == 'Cerdos'):
        bodegaProductoMolidoCerdo.pesoProductoStock +=  molido.totalMolido
        movimiento.productoMov = carneMolidaCerdo
        movimiento.nombreProd =carneMolidaCerdo.nombreProducto
        movimiento.Hasta = bodegaProductoMolidoCerdo.bodega.nombreBodega
        movimiento.entrada = molido.totalMolido
        bodegaProductoMolidoCerdo.save()

    elif(molido.productoMolido.grupo.nombreGrupo == 'Cerdas'):
        bodegaProductoMolidoCerda.pesoProductoStock +=  molido.totalMolido
        movimiento.productoMov = carneMolida
        movimiento.nombreProd = carneMolidaCerda.nombreProducto
        movimiento.Hasta = bodegaProductoMolidoCerda.bodega.nombreBodega
        movimiento.entrada = molido.totalMolido
        bodegaProductoMolidoCerda.save()

    else:
        bodegaProductoMolido.pesoProductoStock += molido.totalMolido
        movimiento.productoMov = carneMolida
        movimiento.nombreProd = carneMolida.nombreProducto
        movimiento.Hasta = bodegaProductoMolido.bodega.nombreBodega
        movimiento.entrada = molido.totalMolido
        bodegaProductoMolido.save()

    movimiento.save()
    bodegaProductoAMoler.save()
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
    carneMolidaCerdo = Producto.objects.get(nombreProducto = 'Carne molida cerdo')
    carneMolidaCerda = Producto.objects.get(nombreProducto = 'Carne molida cerda')

    costoProducto = (molido.pesoAmoler / 1000) * productoAMoler.costoProducto
    costoTotal = costoProducto + cif + mod
    costoKiloMolida = costoTotal / (molido.totalMolido / 1000)

    if(molido.productoMolido.grupo.nombreGrupo == 'Cerdos'):
        carneMolidaCerdo.costoProducto = costoKiloMolida
        carneMolidaCerdo.save()

    elif(molido.productoMolido.grupo.nombreGrupo == 'Cerdas'):
        carneMolidaCerda.costoProducto = costoKiloMolida
        carneMolidaCerda.save()
    else:
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
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    condimentados = Condimentado.objects.filter(fecha__range =(fechainicio,fechafin))
    #condimentados = Condimentado.objects.all()
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


def CostearCondimentado(request):
    idCondimentado = request.GET.get('idCondimentado')
    condimentado = Condimentado.objects.get(pk = int(idCondimentado))
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')
    resPollo = Producto.objects.get(nombreProducto = 'Sabor pollo asado')
    saborLonganiza = Producto.objects.get(nombreProducto = 'Sabor longaniza')
    ablandacarnes = Producto.objects.get(nombreProducto = 'Ablandacarnes')

    pesofilete = condimentado.pesoFileteCond
    pesocondimento = condimentado.condimento
    pesoresaltador = condimentado.resPollo
    pesosaborlonganiza = condimentado.saborLonganiza
    pesoablanda = condimentado.ablandaCarnes

    costoFilete = condimentado.producto.costoProducto *  (pesofilete / 1000)
    costoCondimento = condimento.costoProducto * (pesocondimento/1000)
    costoResPollo = resPollo.costoProducto * (pesoresaltador / 1000)
    costoSaborLonganiza = saborLonganiza.costoProducto * (pesosaborlonganiza / 1000)
    costoAblanda = ablandacarnes.costoProducto * (pesoablanda / 1000)
    mod = condimentado.mod
    cif = condimentado.cif

    costoParcial = costoFilete + costoCondimento + costoResPollo + costoSaborLonganiza + costoAblanda + mod +cif
    costoKiloCondimentado = costoParcial /(condimentado.pesoFileteCond / 1000)

    condimentado.costoFileteCond = costoKiloCondimentado
    condimentado.save()

    if condimentado.producto.grupo.nombreGrupo == 'Pollos':
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de Pollo Condimentado')
        FileteCondimentado.costoProducto = condimentado.costoFileteCond
        msj ='Guardado exitoso!!'

    elif condimentado.producto.grupo.nombreGrupo == 'Cerdos':
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de cerdo Condimentado')
        FileteCondimentado.costoProducto = condimentado.costoFileteCond
        msj ='Guardado exitoso!!'

    else:
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de cerda Condimentado')
        FileteCondimentado.costoProducto = condimentado.costoFileteCond
        msj ='Guardado exitoso!!'

    FileteCondimentado.save()

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def borrarCondimentado(request,idCondimentado):
    condimentado = Condimentado.objects.get(pk = idCondimentado)
    condimentado.delete()
    return HttpResponseRedirect('/fabricacion/condimentado')


def GuardarCondimentado(request):
    idCondimentado = request.GET.get('idCondimentado')
    condimentado = Condimentado.objects.get(pk = int(idCondimentado))
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')
    resPollo = Producto.objects.get(nombreProducto = 'Sabor pollo asado')
    saborLonganiza = Producto.objects.get(nombreProducto = 'Sabor longaniza')
    ablandacarnes = Producto.objects.get(nombreProducto = 'Ablandacarnes')

    #******************************SALIDA PRODUCTO**********************************************

    #productos a restar
    producto = Producto.objects.get(pk = condimentado.producto.codigoProducto)
    bodegaFilete = ProductoBodega.objects.get(bodega = 6, producto = producto.codigoProducto)
    bodegaFilete.pesoProductoStock -= condimentado.pesoACondimentar
    bodegaFilete.save()

    movimientos = Movimientos()
    movimientos.tipo = 'CND%d'%(condimentado.codigo)
    movimientos.fechaMov = condimentado.fecha
    movimientos.productoMov = producto
    movimientos.nombreProd = producto.nombreProducto
    movimientos.salida = condimentado.pesoACondimentar
    movimientos.save()

    #******************************SALIDA CONDIMENTO**********************************************

    bodegaCondimento = ProductoBodega.objects.get(bodega = 5,producto = condimento.codigoProducto)
    bodegaCondimento.pesoProductoStock -= condimentado.condimento
    bodegaCondimento.save()

    movimientos = Movimientos()
    movimientos.tipo = 'CND%d'%(condimentado.codigo)
    movimientos.fechaMov = condimentado.fecha
    movimientos.productoMov = condimento
    movimientos.nombreProd = condimento.nombreProducto
    movimientos.salida = condimentado.condimento
    movimientos.save()

    bodegaResPollo = ProductoBodega.objects.get(bodega = 5,producto = resPollo.codigoProducto)
    bodegaResPollo.pesoProductoStock -= condimentado.resPollo
    bodegaResPollo.save()

    movimientos = Movimientos()
    movimientos.tipo = 'CND%d'%(condimentado.codigo)
    movimientos.fechaMov = condimentado.fecha
    movimientos.productoMov = resPollo
    movimientos.nombreProd = resPollo.nombreProducto
    movimientos.salida = condimentado.resPollo
    movimientos.save()

    bodegaSaborLong = ProductoBodega.objects.get(bodega = 5,producto = saborLonganiza.codigoProducto)
    bodegaSaborLong.pesoProductoStock -= condimentado.saborLonganiza
    bodegaSaborLong.save()

    movimientos = Movimientos()
    movimientos.tipo = 'CND%d'%(condimentado.codigo)
    movimientos.fechaMov = condimentado.fecha
    movimientos.productoMov = saborLonganiza
    movimientos.nombreProd = saborLonganiza.nombreProducto
    movimientos.salida = condimentado.saborLonganiza
    movimientos.save()

    bodegaAblanda = ProductoBodega.objects.get(bodega = 5,producto = ablandacarnes.codigoProducto)
    bodegaAblanda.pesoProductoStock -= condimentado.ablandaCarnes
    bodegaAblanda.save()

    movimientos = Movimientos()
    movimientos.tipo = 'CND%d'%(condimentado.codigo)
    movimientos.fechaMov = condimentado.fecha
    movimientos.productoMov = ablandacarnes
    movimientos.nombreProd = ablandacarnes.nombreProducto
    movimientos.salida = condimentado.ablandaCarnes
    movimientos.save()


            #guardamos las cantidades producidas
    if condimentado.producto.grupo.nombreGrupo == 'Pollos':
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de Pollo Condimentado')
        #FileteCondimentado.costoProducto = condimentado.costoFileteCond
        bodegaFileteCond = ProductoBodega.objects.get(bodega = 5,producto = FileteCondimentado.codigoProducto)
        bodegaFileteCond.pesoProductoStock += condimentado.pesoFileteCond
        bodegaFileteCond.save()
        msj ='Guardado exitoso!!'

    elif condimentado.producto.grupo.nombreGrupo == 'Cerdos':
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de cerdo Condimentado')
        #FileteCondimentado.costoProducto = condimentado.costoFileteCond
        bodegaFileteCond = ProductoBodega.objects.get(bodega = 5,producto = FileteCondimentado.codigoProducto)
        bodegaFileteCond.pesoProductoStock += condimentado.pesoFileteCond
        bodegaFileteCond.save()
        msj ='Guardado exitoso!!'

    else:
        FileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de cerda Condimentado')
        #FileteCondimentado.costoProducto = condimentado.costoFileteCond
        bodegaFileteCond = ProductoBodega.objects.get(bodega = 5,producto = FileteCondimentado.codigoProducto)
        bodegaFileteCond.pesoProductoStock += condimentado.pesoFileteCond
        bodegaFileteCond.save()
        msj ='Guardado exitoso!!'

    #******************************ENTRADA FILETE CONDIMENTADO**********************************************
    movimientos = Movimientos()
    movimientos.tipo = 'CND%d'%(condimentado.codigo)
    movimientos.fechaMov = condimentado.fecha
    movimientos.productoMov = FileteCondimentado
    movimientos.nombreProd = FileteCondimentado.nombreProducto
    movimientos.entrada = condimentado.pesoFileteCond
    movimientos.save()

    condimentado.guardado = True
    condimentado.save()
    #FileteCondimentado.save()

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')


def TraerCostoFilete(request):
    idProducto = request.GET.get('producto')
    producto = Producto.objects.get(pk = int(idProducto)).costoProducto
    respuesta = json.dumps(producto)
    return HttpResponse(respuesta,mimetype='application/json')

#**********************************************PROCESO TAJADO **********************************************************

def GestionTajado(request):
    fechainicio = date.today() - timedelta(days=10)
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

def EditaTajado(request,idTajado):
    tajado = Tajado.objects.get(pk = idTajado)
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    exito = True
    tajados = Tajado.objects.all().filter(fechaTajado__range = (fechainicio,fechafin))

    if request.method == 'POST':
        formulario = TajadoForm(request.POST,instance=tajado)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/tajado/')
    else:
        formulario = TajadoForm(instance=tajado)

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
                tjdo.costoKilo = costoTotal * Decimal(0.970)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
                tajado.totalTajado = tjdo.pesoProducto
            elif tjdo.producto.nombreProducto == 'Hueso de pollo':
                tjdo.costoKilo = costoTotal * Decimal(0.01)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
            elif tjdo.producto.nombreProducto == 'Piel':
                tjdo.costoKilo = costoTotal * Decimal(0.01)/(tjdo.pesoProducto/1000)
                costokilo = tjdo.costoKilo
            elif tjdo.producto.nombreProducto == 'Procesos de pollo':
                tjdo.costoKilo = costoTotal * Decimal(0.01)/(tjdo.pesoProducto/1000)
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
    if tajado.producto.nombreProducto == 'Pierna Ensalinada':
        bodegaTajado = ProductoBodega.objects.get(bodega = 6, producto = tajado.producto.codigoProducto)
        bodegaTajado.pesoProductoStock -= tajado.pesoProducto
        bodegaTajado.save()
    else:
        bodegaTajado = ProductoBodega.objects.get(bodega = 5, producto = tajado.producto.codigoProducto)
        bodegaTajado.pesoProductoStock -= tajado.pesoProducto
        bodegaTajado.save()


    movimiento = Movimientos()
    movimiento.tipo = 'TJD%d'%(tajado.codigoTajado)
    movimiento.productoMov = tajado.producto
    movimiento.nombreProd = tajado.producto.nombreProducto
    movimiento.fechaMov = tajado.fechaTajado
    movimiento.salida = tajado.pesoProducto
    movimiento.save()


    for det in detTajado:

        #Guardamos el producto resultante
        bodega = ProductoBodega.objects.get(bodega = 5,producto =  det.producto.codigoProducto)
        bodega.unidadesStock += det.unidades
        bodega.pesoProductoStock += det.pesoProducto
        bodega.save()
        movimiento = Movimientos()
        movimiento.tipo = 'TJD%d'%(tajado.codigoTajado)
        movimiento.productoMov = det.producto
        movimiento.nombreProd = det.producto.nombreProducto
        movimiento.fechaMov = tajado.fechaTajado
        movimiento.entrada = det.pesoProducto
        movimiento.save()

    tajado.guardado = True
    tajado.save()

    msj = 'Registro guardado exitosamente'

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

#***********************************************PLANILLA DESPOSTE*******************************************************
def TemplateListaDesposte(request):
    grupos = Grupo.objects.all()
    return render_to_response('Fabricacion/TemplateListaDesposte.html',{'grupos':grupos},context_instance = RequestContext(request))
def ReporteListaDesposte(request):
    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    grupo = request.GET.get('grupo')

    nombreGrupo = Grupo.objects.get(pk = int(grupo)).nombreGrupo


    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    desposte = PlanillaDesposte.objects.filter(fechaDesposte__range = (finicio,ffin)).filter(tipoDesposte = nombreGrupo)
    respuesta = serializers.serialize('json',desposte)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionDesposte(request,tipo):
    fechainicio = date.today() - timedelta(days=15)
    fechafin = date.today()
    despostes = ''
    if int(tipo) == 2:
        q1 = despostes = PlanillaDesposte.objects.select_related().filter(fechaDesposte__range =(fechainicio,fechafin),tipoDesposte = 'Cerdos')
        q2 = despostes = PlanillaDesposte.objects.select_related().filter(fechaDesposte__range =(fechainicio,fechafin),tipoDesposte = 'Cerdas')
        q3 = despostes = PlanillaDesposte.objects.select_related().filter(fechaDesposte__range =(fechainicio,fechafin),tipoDesposte = '')
        despostes = q1 | q2 | q3
    elif int(tipo) == 1:
        q1 = despostes = PlanillaDesposte.objects.select_related().filter(fechaDesposte__range =(fechainicio,fechafin),tipoDesposte = 'Reses')
        q2 = despostes = PlanillaDesposte.objects.select_related().filter(fechaDesposte__range =(fechainicio,fechafin),tipoDesposte = '')
        despostes = q1 | q2


    #despostes = PlanillaDesposte.objects.all()

    if request.method == 'POST':

        formulario = DesposteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/desposte/'+tipo)
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

def borrarDesposte(request,idDesp):
    desposte = PlanillaDesposte.objects.get(pk = idDesp)
    desposte.delete()
    return HttpResponseRedirect('/fabricacion/desposte')

def GestionDesposteActualizado(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = ''
    if Canal.objects.filter(planilla = idplanilla).filter(estado = True).exists():
        canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
    else:
        return HttpResponseRedirect('/inventario/compra')

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
        vrCarnes = ceil((vrTotalCanales * Decimal(38.5))/100)
        vrCarnes2 = ceil((vrTotalCanales * Decimal(28))/100)
        vrCarnes3 = 0
        vrCarnes4 = 0
        vrCostillas = ceil((vrTotalCanales * 16)/100)
        vrHuesos = ceil((vrTotalCanales *Decimal(2.5))/100)
        vrsubProd = ceil((vrTotalCanales * Decimal(4))/100)
        vrDesecho = ceil((vrTotalCanales * Decimal(1))/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido

    elif tipoDesposte == 'Cerdas':
        vrCarnes = ceil((vrTotalCanales * Decimal(34.5))/100)
        vrCarnes2 = ceil((vrTotalCanales * 32)/100)
        vrCarnes3 = 0
        vrCarnes4 = 0
        vrCostillas = ceil((vrTotalCanales * 13)/100)
        vrHuesos = ceil((vrTotalCanales * 4)/100)
        vrsubProd = ceil((vrTotalCanales * 12)/100)
        vrDesecho = ceil((vrTotalCanales * 2)/100)
        pesoAsumido =Decimal(vrDesecho) + perdidaPeso
        vrCarnes =Decimal(vrCarnes) + pesoAsumido
    else:
        vrCarnes = ceil((vrTotalCanales * Decimal(7))/100)
        vrCarnes2 = ceil((vrTotalCanales * Decimal(29))/100)
        vrCarnes3 = ceil((vrTotalCanales * Decimal(33))/100)
        vrCarnes4 = ceil((vrTotalCanales * Decimal(5))/100)
        vrCostillas = ceil((vrTotalCanales * Decimal(3.5))/100)
        vrHuesos = ceil((vrTotalCanales * 11)/100)
        vrsubProd = ceil((vrTotalCanales * Decimal(0.5))/100)
        vrDesecho = ceil((vrTotalCanales * Decimal(0.5))/100)
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
           #sacrificio = Sacrificio.objects.get(recepcion = recepcion.codigoRecepcion)
           productoEntrante = int(request.POST.get('producto'))
           prodEnt = str(Producto.objects.get(pk = productoEntrante).nombreProducto)
           pesoProducto = Decimal(request.POST.get('PesoProducto'))

           '''if prodEnt == 'Cola':
               detalles.PesoProducto = (sacrificio.cola / cantReses) * canales.count()
           elif prodEnt == 'Rinones':
               detalles.PesoProducto =(sacrificio.rinones / cantReses) * canales.count()
           elif prodEnt == 'Creadillas':
               detalles.PesoProducto =(sacrificio.creadillas / cantReses) * canales.count()
           elif prodEnt == 'Recortes Sacrificio':
               detalles.PesoProducto =(sacrificio.recortes / cantReses) * canales.count()
           elif prodEnt == 'Ubre':
               detalles.PesoProducto =(sacrificio.ubre / cantReses) * canales.count()
           else:'''
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
           detalles.pesoCarne = pesoCarnes + pesoCarnes2 + pesoCarnes3 + pesoCarnes4
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

def borrarDetDesposte(request,idDesp):
    detalle = DetallePlanilla.objects.get(pk = idDesp)
    desposte = PlanillaDesposte.objects.get(pk = detalle.planilla.codigoPlanilla)
    detalle.delete()
    return HttpResponseRedirect('/fabricacion/detalleDesposte/'+ str(desposte.codigoPlanilla))

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
        '''if producto.nombreProducto == 'Cola':
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

            '''
        bodega.pesoProductoStock += detalle.PesoProducto
        bodega.unidadesStock += detalle.unidades

        movimiento.tipo = 'DSP%d'%(desposte.codigoPlanilla)
        movimiento.fechaMov = desposte.fechaDesposte
        movimiento.productoMov = detalle.producto
        movimiento.nombreProd = detalle.producto.nombreProducto
        movimiento.Hasta = bodega.bodega.nombreBodega
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
    fechainicio = date.today() - timedelta(days=40)
    fechafin = date.today()
    canalPendiente = Canal.objects.select_related().filter(estado = False, recepcion__compra__fechaCompra__range =(fechainicio,fechafin)).order_by('codigoCanal')
    return render_to_response('Fabricacion/InformeCanalesPendientes.html',{'canalesPendientes':canalPendiente},
                              context_instance = RequestContext(request))

def verCanal(request,idCanal):
    canal = Canal.objects.get(pk = idCanal)
    recepcion = PlanillaRecepcion.objects.get(pk = canal.recepcion.codigoRecepcion)
    return HttpResponseRedirect('/fabricacion/canal/'+ str(recepcion.codigoRecepcion))

def GestionDescarneCabeza(request):
    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    descarnes = DescarneCabeza.objects.filter(fecha__range =(fechainicio,fechafin))
    #descarnes = DescarneCabeza.objects.all()
    costoCabeza = Producto.objects.filter(nombreProducto = 'Cabeza')
    cabezaCerda = Producto.objects.filter(nombreProducto = 'Cabeza Cerda')

    # sacamos el costo de las cabezas de cerdo y cerda ppor separado
    costoCabezaCerdo = 0
    costoCabezaCerda = 0

    for costo in costoCabeza:
        costoCabezaCerdo = costo.costoProducto

    for costo in cabezaCerda:
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
                if descarne.lenguas == 0:
                    vrKiloLenguas = 0
                else:
                    vrKiloLenguas = ceil(Decimal(costoLenguas) / (descarne.lenguas/1000))


                costoProcesos = Decimal(0.69) * costoDescarne
                if descarne.procesos == 0:
                    vrKiloProcesos = 0
                else:
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
                if descarne.procesos == 0:
                    vrKiloProcesos = 0
                else:
                    vrKiloProcesos = ceil(Decimal(costoProcesos) / (descarne.procesos/1000))

                #Guardamos los costos en la tabla Producto
                recorte = Producto.objects.get(nombreProducto = 'Recortes Cabeza Cerda')
                recorte.costoProducto = costoUnidad
                recorte.save()

                proceso = Producto.objects.get(nombreProducto = 'Procesos de Cabeza Cerda')
                proceso.costoProducto =vrKiloProcesos
                proceso.save()

                descarne.vrKiloProceso = vrKiloProcesos
                descarne.vrKiloRecorte = costoUnidad


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
        cabeza = Producto.objects.get(nombreProducto = 'Cabeza Cerda',grupo__nombreGrupo = 'Cerdas')
        bodegaCabeza = ProductoBodega.objects.get(bodega = 5, producto = cabeza.codigoProducto)
        bodegaCabeza.pesoProductoStock -= descarne.pesoCabezas

        msj = 'Guardado Exitoso'

    descarne.guardado = True
    descarne.save()

    respuesta  = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')
def borrarDescarne(request,idDesc):
    descarne = DescarneCabeza.objects.get(pk = idDesc)
    descarne.delete()
    return HttpResponseRedirect('/fabricacion/descarne/')


def GestionEmpacadoApanados(request):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    empaques  = EmpacadoApanados.objects.filter(fechaEmpacado__range =(fechainicio,fechafin))
    #empaques  = EmpacadoApanados.objects.all()

    if request.method == 'POST':

        formulario = EmpacadoApanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/empacadoApanado')
    else:
        formulario = EmpacadoApanadoForm(initial={'mod':1812})

    return render_to_response('Fabricacion/GestionEmpaqueApanado.html',{'formulario':formulario,'empaques':empaques },
                              context_instance = RequestContext(request))

def EditaEmpacadoApanados(request,idEmpacado):
    empaque = EmpacadoApanados.objects.get(pk = idEmpacado)
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    empaques  = EmpacadoApanados.objects.filter(fechaEmpacado__range =(fechainicio,fechafin))
    #empaques  = EmpacadoApanados.objects.all()

    if request.method == 'POST':

        formulario = EmpacadoApanadoForm(request.POST,instance=empaque)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/empacadoApanado')
    else:
        formulario = EmpacadoApanadoForm(initial={'mod':1812},instance=empaque)

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
    #bodegaChuleta = ProductoBodega.objects.get(bodega = 6,producto = empaque.productoAEmpacar.codigoProducto)
    #bodegaChuletaEmpacadaPollo = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Chuleta Empacada Pollo')
    #bodegaChuletaEmpacadaCerdo = ProductoBodega.objects.get(bodega = 5,producto__nombreProducto = 'Chuleta Empacada Cerdo')

    movimiento = Movimientos()
    movimiento.tipo = 'EMP%d'%(empaque.id)
    movimiento.fechaMov = empaque.fechaEmpacado
    movimiento.productoMov = bodegaBandeja.producto
    movimiento.nombreProd = bodegaBandeja.producto.nombreProducto
    movimiento.salida = empaque.cantBandejas
    movimiento.save()

    bodegaBandeja.unidadesStock -= empaque.cantBandejas
    bodegaBandeja.save()

    movimiento = Movimientos()
    movimiento.tipo = 'EMP%d'%(empaque.id)
    movimiento.fechaMov = empaque.fechaEmpacado
    movimiento.productoMov = bodegaStiker.producto
    movimiento.nombreProd = bodegaStiker.producto.nombreProducto
    movimiento.salida = empaque.stikers
    movimiento.save()

    bodegaStiker.unidadesStock -= empaque.stikers
    bodegaStiker.save()

    empaque.guardado = True
    empaque.save()

    msj = 'Guardado Exitoso'

    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')
'''
    movimiento = Movimientos()
    movimiento.tipo = 'EMP%d'%(empaque.id)
    movimiento.fechaMov = empaque.fechaEmpacado
    movimiento.productoMov = bodegaChuleta.producto
    movimiento.nombreProd = bodegaChuleta.producto.nombreProducto
    movimiento.salida = empaque.pesoChuelta
    movimiento.save()

    bodegaChuleta.pesoProductoStock -= empaque.pesoChuelta
    bodegaChuleta.save()

    if empaque.productoAEmpacar.grupo.nombreGrupo == 'Pollos':
        bodegaChuletaEmpacadaPollo.pesoProductoStock += empaque.pesoChuelta
        bodegaChuletaEmpacadaPollo.save()
        movimiento = Movimientos()
        movimiento.tipo = 'EMP%d'%(empaque.id)
        movimiento.fechaMov = empaque.fechaEmpacado
        movimiento.productoMov = bodegaChuletaEmpacadaPollo.producto
        movimiento.nombreProd = bodegaChuletaEmpacadaPollo.producto.nombreProducto
        movimiento.entrada = empaque.pesoChuelta
        movimiento.save()
    elif empaque.productoAEmpacar.grupo.nombreGrupo == 'Cerdos' or empaque.productoAEmpacar.grupo.nombreGrupo == 'Cerdas':
        bodegaChuletaEmpacadaCerdo.pesoProductoStock += empaque.pesoChuelta
        bodegaChuletaEmpacadaCerdo.save()
        movimiento = Movimientos()
        movimiento.tipo = 'EMP%d'%(empaque.id)
        movimiento.fechaMov = empaque.fechaEmpacado
        movimiento.productoMov = bodegaChuletaEmpacadaCerdo.producto
        movimiento.nombreProd = bodegaChuletaEmpacadaCerdo.producto.nombreProducto
        movimiento.entrada = empaque.pesoChuelta
        movimiento.save()'''



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

    cantidadMiga = {}
    cantidadCondimento = {}
    cantidadMiga['Miga Pollo'] = 0
    cantidadCondimento['Condimento Pollo'] = 0
    cantidadMiga['Miga Cerdo'] = 0


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
        cantidadMiga['Miga Cerdo'] += ceil(chuleta.miga)


    chuletaPollo = ProcesoApanado.objects.filter(fechaApanado__range = (finicio,ffin)).filter(productoApanado__grupo__nombreGrupo = 'Pollos' )
    promedioChuletasPollo = chuletaPollo.aggregate(Avg('costoKiloApanado'))

    for chPollo in chuletaPollo:
        pesoChuletaPollo['Chuleta Pollo'] += ceil(chPollo.totalApanado)
        cantidadMiga['Miga Pollo'] += ceil(chPollo.miga)


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
        cantidadCondimento['Condimento Pollo'] += ceil(cond.condimento)



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


    listas = {'cantidadMiga':cantidadMiga,'ListaPesoFilete':ListaPesoFilete,'Promedio':Promedio,
              'promedioBandejasPollo':promedioBandejasPollo,'cantidadCondimento':cantidadCondimento,
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


def TemplateMenChicharrones(request):
    return render_to_response('Fabricacion/TemplateMenChicharrones.html',context_instance = RequestContext(request))

def ReporteMenChicharrones(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    ListaCantMenudo = {}
    ListaCantMenudo['Menudo'] = 0
    ListaCantChicharrones = {}
    ListaCantChicharrones['Chicharrones'] = 0
    ListaCantGrasa = {}
    ListaCantGrasa['Grasa'] = 0


    menudos = Menudos.objects.select_related().filter(fechaMenudo__range = (finicio,ffin))
    promediomenudos = menudos.aggregate(Avg('costoKiloPicadillo'))

    for menudo in menudos:
        ListaCantMenudo['Menudo'] += ceil(menudo.pesoPicadillo)


    chicharrones = TallerChicharron.objects.select_related().filter(fechaChicharron__range = (finicio,ffin))
    promedioChicharrones = chicharrones.aggregate(Avg('costoUndChicharron'))
    promedioGrasa = chicharrones.aggregate(Avg('costoUndGrasa'))

    for chicharron in chicharrones:
        ListaCantChicharrones['Chicharrones'] += chicharron.undChicharron

    for grasas in chicharrones:
       ListaCantGrasa['Grasa'] += grasas.undGrasa



    Listas = {'promediomenudos':promediomenudos,'promedioChicharrones':promedioChicharrones,'promedioGrasa':promedioGrasa,
              'ListaCantMenudo':ListaCantMenudo,'ListaCantChicharrones':ListaCantChicharrones,'ListaCantGrasa':ListaCantGrasa}

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

def GestionLenguas(request):

    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    lenguas = TallerLenguas.objects.filter(fechaLenguas__range =(fechainicio,fechafin))

    if request.method == 'POST':

        formulario = LenguasForm(request.POST)
        if formulario.is_valid():
            datos = formulario.save()

            pesoAntes = datos.pesoAntes
            pesoDespues = datos.pesoDespues
            costoLenguas = Producto.objects.select_related().get(nombreProducto = 'Lengua Cerdo').costoProducto
            cif = datos.cif
            mod = datos.mod
            costoTotal = (costoLenguas * (pesoAntes/1000)) + cif + mod
            costoKiloPicadillo = costoTotal /(pesoDespues/1000)
            datos.costoKiloPicadillo = costoKiloPicadillo
            datos.save()

            picadillo = Producto.objects.get(nombreProducto = 'Picadillo')
            costoAnterior = picadillo.costoProducto
            picadillo.costoProducto = (costoKiloPicadillo + costoAnterior)/2
            picadillo.save()

            return HttpResponseRedirect('/fabricacion/lenguas')
    else:
        formulario = LenguasForm()

    return render_to_response('Fabricacion/GestionLenguas.html',{'formulario':formulario,'lenguas':lenguas },
                              context_instance = RequestContext(request))

def GuardarLenguas(request):

    idLenguas = request.GET.get('idLenguas')
    lengua = TallerLenguas.objects.get(pk = int(idLenguas))
    picadillo = Producto.objects.get(nombreProducto = 'Picadillo')
    ProdLengua = Producto.objects.select_related().get(nombreProducto = 'Lengua Cerdo')

    bodegaLengua = ProductoBodega.objects.get(bodega = 5,producto = ProdLengua.codigoProducto )
    bodegaLengua.pesoProductoStock -= lengua.pesoAntes

    movimiento = Movimientos()
    movimiento.tipo = 'LGA%d'%(lengua.id)
    movimiento.fechaMov = lengua.fechaLenguas
    movimiento.productoMov = ProdLengua
    movimiento.nombreProd = ProdLengua.nombreProducto
    movimiento.salida = lengua.pesoAntes

    bodegaLengua.save()
    movimiento.save()

    bodegaPicadillo = ProductoBodega.objects.get(bodega = 5,producto = picadillo.codigoProducto )
    bodegaPicadillo.pesoProductoStock += lengua.pesoDespues


    movimiento = Movimientos()
    movimiento.tipo = 'LGA%d'%(lengua.id)
    movimiento.fechaMov = lengua.fechaLenguas
    movimiento.productoMov = picadillo
    movimiento.nombreProd = picadillo.nombreProducto
    movimiento.entrada = lengua.pesoDespues
    movimiento.Hasta = bodegaPicadillo.bodega.nombreBodega

    bodegaPicadillo.save()
    movimiento.save()

    lengua.guardado = True
    lengua.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def borrarLenguas(request,idLengua):
    lengua = TallerLenguas.objects.get(pk = idLengua)
    lengua.delete()
    return HttpResponseRedirect('/fabricacion/lenguas')


def GestionMenudos(request):

    fechainicio = date.today() - timedelta(days=30)
    fechafin = date.today()
    menudos = Menudos.objects.filter(fechaMenudo__range =(fechainicio,fechafin))


    if request.method == 'POST':

        formulario = MenudoForm(request.POST)
        if formulario.is_valid():
            datos = formulario.save()

            escaldado = datos.costoEscaldado * datos.cantMenudos
            costoMenudos = datos.cantMenudos * datos.costoMenudo
            costoTotal = costoMenudos + datos.cif + datos.mod + escaldado
            costoKiloPicadillo = costoTotal /(datos.pesoPicadillo /1000)

            datos.costoKiloPicadillo = costoKiloPicadillo
            datos.save()

            picadillo = Producto.objects.get(nombreProducto = 'Picadillo')
            picadillo.costoProducto = costoKiloPicadillo
            picadillo.save()

            return HttpResponseRedirect('/fabricacion/menudos')
    else:
        formulario = MenudoForm(initial={'costoMenudo':12000,'costoEscaldado':3500})

    return render_to_response('Fabricacion/GestionMenudos.html',{'formulario':formulario,'menudos':menudos },
                              context_instance = RequestContext(request))

def GuardarMenudos(request):
    idMenudos = request.GET.get('idMenudo')
    menudo = Menudos.objects.get(pk = int(idMenudos))
    picadillo = Producto.objects.get(nombreProducto = 'Picadillo')

    bodegaPicadillo = ProductoBodega.objects.get(bodega = 5,producto = picadillo.codigoProducto )
    bodegaPicadillo.pesoProductoStock += menudo.pesoPicadillo
    bodegaPicadillo.save()

    movimiento = Movimientos()
    movimiento.tipo = 'MDO%d'%(menudo.id)
    movimiento.fechaMov = menudo.fechaMenudo
    movimiento.productoMov = picadillo
    movimiento.nombreProd = picadillo.nombreProducto
    movimiento.entrada = menudo.pesoPicadillo
    movimiento.save()

    menudo.guardado = True
    menudo.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionFrito(request):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    usuario = request.user
    emp = Empleado.objects.get(usuario = usuario.username)
    if usuario.is_staff:
        plantilla = 'base.html'
        fritos = TallerFrito.objects.filter(fechaFrito__range =(fechainicio,fechafin))

    else:
        plantilla = 'PuntoVentaNorte.html'
        fritos = TallerFrito.objects.filter(fechaFrito__range =(fechainicio,fechafin),punto = emp.punto.codigoBodega)

    #fritos = TallerFrito.objects.all()

    if request.method == 'POST':

        formulario = FritoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/fritos')
    else:
        formulario = FritoForm(initial={'punto':emp.punto.codigoBodega})

    return render_to_response('Fabricacion/GestionFritos.html',{'plantilla':plantilla,'formulario':formulario,'fritos':fritos},
                              context_instance = RequestContext(request))

def borrarFrito(request,idFrito):
    frito = TallerFrito.objects.get(pk = idFrito)
    frito.delete()
    return HttpResponseRedirect('/fabricacion/fritos')

def CostearFrito(request):
    idFrito = request.GET.get('idFrito')
    frito = TallerFrito.objects.get(pk = int(idFrito))

    producto = Producto.objects.get(pk = frito.productoFrito.codigoProducto)
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')
    pesoProducto = frito.pesoProducto
    pesoCondimento = frito.condimento
    costoCondimento = condimento.costoProducto * (pesoCondimento /1000)
    costoProducto = producto.costoProducto * (pesoProducto/1000)
    costoTotal = (costoCondimento + costoProducto)/((pesoCondimento+pesoProducto)/1000)

    frito.pesoTotalFrito = pesoCondimento + pesoProducto
    frito.costoKiloFrito = costoTotal
    frito.save()


    if frito.productoFrito.grupo.nombreGrupo == 'Cerdos':
        fritoProcesado = Producto.objects.get(nombreProducto = 'Frito de Cerdo Condimentado')
        fritoProcesado.costoProducto = costoTotal
        fritoProcesado.save()
    else:
        fritoProcesado = Producto.objects.get(nombreProducto = 'Frito de Cerda Condimentado')
        fritoProcesado.costoProducto = costoTotal
        fritoProcesado.save()

    msj = 'Costeo exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')


def GuardarFrito(request):
    idFrito = request.GET.get('idFrito')
    frito = TallerFrito.objects.get(pk = int(idFrito))

    producto = Producto.objects.get(pk = frito.productoFrito.codigoProducto)
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    bodegaProducto = ProductoBodega.objects.get(bodega = frito.punto.codigoBodega,producto = producto.codigoProducto)
    bodegaProducto.pesoProductoStock -= frito.pesoProducto
    bodegaProducto.save()

    bodegaCondimento = ProductoBodega.objects.get(bodega = frito.punto.codigoBodega,producto = condimento.codigoProducto)
    bodegaCondimento.pesoProductoStock -= frito.condimento
    bodegaCondimento.save()


    movimiento = Movimientos()
    movimiento.tipo = 'FRT%d'%(frito.id)
    movimiento.fechaMov = frito.fechaFrito
    movimiento.productoMov = condimento
    movimiento.nombreProd = condimento.nombreProducto
    movimiento.salida = frito.condimento
    movimiento.desde = bodegaCondimento.bodega.nombreBodega
    movimiento.save()

    movimiento = Movimientos()
    movimiento.tipo = 'FRT%d'%(frito.id)
    movimiento.fechaMov = frito.fechaFrito
    movimiento.productoMov = producto
    movimiento.nombreProd = producto.nombreProducto
    movimiento.salida = frito.pesoProducto
    movimiento.desde = bodegaProducto.bodega.nombreBodega
    movimiento.save()



    if frito.productoFrito.grupo.nombreGrupo == 'Cerdos':
        fritoProcesado = Producto.objects.get(nombreProducto = 'Frito de Cerdo Condimentado')
        bodegaFritoCerdo = ProductoBodega.objects.get(bodega = frito.punto.codigoBodega, producto = fritoProcesado.codigoProducto)
        bodegaFritoCerdo.pesoProductoStock += frito.pesoTotalFrito
        bodegaFritoCerdo.save()

        movimiento = Movimientos()
        movimiento.tipo = 'FRT%d'%(frito.id)
        movimiento.fechaMov = frito.fechaFrito
        movimiento.productoMov = fritoProcesado
        movimiento.nombreProd = fritoProcesado.nombreProducto
        movimiento.entrada = frito.pesoTotalFrito
        movimiento.Hasta = bodegaFritoCerdo.bodega.nombreBodega
        movimiento.save()
    else:
        fritoProcesado = Producto.objects.get(nombreProducto = 'Frito de Cerda Condimentado')
        bodegaFritoCerda = ProductoBodega.objects.get(bodega = frito.punto.codigoBodega, producto = fritoProcesado.codigoProducto)
        bodegaFritoCerda.pesoProductoStock += frito.pesoTotalFrito
        bodegaFritoCerda.save()

        movimiento = Movimientos()
        movimiento.tipo = 'FRT%d'%(frito.id)
        movimiento.fechaMov = frito.fechaFrito
        movimiento.productoMov = fritoProcesado
        movimiento.nombreProd = fritoProcesado.nombreProducto
        movimiento.entrada = frito.pesoTotalFrito
        movimiento.Hasta = bodegaFritoCerda.bodega.nombreBodega
        movimiento.save()

    frito.guardado =True
    frito.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionCarneCond(request):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    usuario = request.user
    emp = Empleado.objects.get(usuario = usuario.username)
    if usuario.is_staff:
        plantilla = 'base.html'
        carnes = TallerCarneCondimentada.objects.filter(fechaCarCond__range =(fechainicio,fechafin))

    else:
        plantilla = 'PuntoVentaNorte.html'
        carnes = TallerCarneCondimentada.objects.filter(fechaCarCond__range =(fechainicio,fechafin),puntoCond = emp.punto.codigoBodega)

    if request.method == 'POST':

        formulario = CarneCondForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/carneCondimentada')
    else:
        formulario = CarneCondForm(initial={'puntoCond':emp.punto.codigoBodega})

    return render_to_response('Fabricacion/GestionCarneCond.html',{'plantilla':plantilla,'formulario':formulario,'carnes':carnes },
                              context_instance = RequestContext(request))
def borrarTallerCondimentado(request,idCondimentado):
    condimentado = TallerCarneCondimentada.objects.get(pk = idCondimentado)
    condimentado.delete()
    return HttpResponseRedirect('/fabricacion/carneCondimentada')


def CostearCarneCond(request):
    idCarne = request.GET.get('idCarne')
    carne = TallerCarneCondimentada.objects.get(pk = int(idCarne))
    producto = Producto.objects.get(pk = carne.productoCond.codigoProducto)
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')
    if carne.productoCond.nombreProducto == 'Bola':
        carneCondimentada = Producto.objects.get(nombreProducto = 'Bola Condimentada')
    elif carne.productoCond.nombreProducto == 'Agujas' or carne.productoCond.nombreProducto == 'Brazos Enteros':
        carneCondimentada = Producto.objects.get(nombreProducto = 'Aguja Condimentada')
    else:
        carneCondimentada = carne.productoCond

    pesoProducto = carne.pesoProducto
    pesoCondimento = carne.condimento

    costoProducto = producto.costoProducto * (pesoProducto / 1000)
    costoCondimento = condimento.costoProducto * (pesoCondimento / 1000)

    costoTotal = (costoProducto + costoCondimento)/((pesoProducto + pesoCondimento)/1000)

    carneCondimentada.costoProducto = costoTotal
    carneCondimentada.save()

    carne.costoKiloCond = costoTotal
    carne.pesoTotalCond = pesoProducto + pesoCondimento
    carne.save()

    msj = 'Costeo exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GuardarCarneCond(request):

    idCarne = request.GET.get('idCarne')
    carne = TallerCarneCondimentada.objects.select_related().get(pk = int(idCarne))
    #xproducto = Producto.objects.get(pk = carne.productoCond.codigoProducto)
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    if carne.productoCond.nombreProducto == 'Bola':
        carneCondimentada = Producto.objects.get(nombreProducto = 'Bola Condimentada')
    elif carne.productoCond.nombreProducto == 'Agujas' or carne.productoCond.nombreProducto == 'Brazos Enteros':
        carneCondimentada = Producto.objects.get(nombreProducto = 'Aguja Condimentada')
    else:
        carneCondimentada = carne.productoCond

    # Quito el Producto utilizado

    bodegaProducto = ProductoBodega.objects.get(bodega = carne.puntoCond.codigoBodega,producto = carne.productoCond.codigoProducto)
    bodegaProducto.pesoProductoStock -= carne.pesoProducto
    bodegaProducto.save()

    movimiento = Movimientos()
    movimiento.tipo = 'CCON%d'%(carne.id)
    movimiento.fechaMov = carne.fechaCarCond
    movimiento.productoMov = carne.productoCond
    movimiento.nombreProd = carne.productoCond.nombreProducto
    movimiento.salida = carne.pesoProducto
    movimiento.save()

    #Quito el Condimento utilizado

    bodegaCondimento = ProductoBodega.objects.get(bodega = carne.puntoCond.codigoBodega,producto = condimento.codigoProducto)
    bodegaCondimento.pesoProductoStock -= carne.condimento
    bodegaCondimento.save()

    movimiento = Movimientos()
    movimiento.tipo = 'CCON%d'%(carne.id)
    movimiento.fechaMov = carne.fechaCarCond
    movimiento.productoMov = condimento
    movimiento.nombreProd = condimento.nombreProducto
    movimiento.salida = carne.condimento
    movimiento.save()

    bodegaCarneCond = ProductoBodega.objects.get(bodega =  carne.puntoCond.codigoBodega,producto = carneCondimentada.codigoProducto)
    bodegaCarneCond.pesoProductoStock += carne.pesoTotalCond
    bodegaCarneCond.save()

    movimiento = Movimientos()
    movimiento.tipo = 'CCON%d'%(carne.id)
    movimiento.fechaMov = carne.fechaCarCond
    movimiento.productoMov = carneCondimentada
    movimiento.nombreProd = carneCondimentada.nombreProducto
    movimiento.entrada = carne.pesoTotalCond
    movimiento.save()

    carne.guardado = True
    carne.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionCroqueta(request):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    usuario = request.user
    emp = Empleado.objects.get(usuario = usuario.username)
    if usuario.is_staff:
        plantilla = 'base.html'
        croquetas = TallerCroquetas.objects.filter(fechaCroqueta__range =(fechainicio,fechafin))

    else:
        plantilla = 'PuntoVentaNorte.html'
        croquetas = TallerCroquetas.objects.filter(fechaCroqueta__range =(fechainicio,fechafin),puntoCroq = emp.punto.codigoBodega)

    if request.method == 'POST':

        formulario = CroquetaFrom(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/croquetas')
    else:
        formulario = CroquetaFrom(initial={'puntoCroq':emp.punto.codigoBodega})

    return render_to_response('Fabricacion/GestionCroquetas.html',{'plantilla':plantilla,'formulario':formulario,'croquetas':croquetas },
                              context_instance = RequestContext(request))

def borrarCroqueta(request,idCroqueta):
    croqueta = TallerCroquetas.objects.get(pk = idCroqueta)
    croqueta.delete()
    return HttpResponseRedirect('/fabricacion/croquetas')

def CostearCroqueta(request):
    idCorqueta = request.GET.get('idCroqueta')
    regCroqueta = TallerCroquetas.objects.get(pk = int(idCorqueta))

    if regCroqueta.puntoCroq.nombreBodega == 'Norte':
        croquetaApanada = Producto.objects.get(nombreProducto = 'Croqueta Apanada')
    else:
        croquetaApanada = Producto.objects.get(nombreProducto = 'Pollo Molido')

    croquetaCocida = Producto.objects.get(nombreProducto = 'Croqueta Cocinada')
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')
    miga = Producto.objects.get(nombreProducto = 'Miga Preparada')


    pesoCroqueta = regCroqueta.croqueta
    pesoCondimento = regCroqueta.condimento
    pesoMiga = regCroqueta.pesoTotalCroqueta - (pesoCroqueta + pesoCondimento)

    costoMiga = miga.costoProducto * (pesoMiga /1000)
    costoCroqueta = croquetaCocida.costoProducto * (pesoCroqueta/1000)
    costoCondimento = condimento.costoProducto * (pesoCondimento/1000)

    pesoTotal = regCroqueta.pesoTotalCroqueta/1000
    costoTotal = costoMiga + costoCroqueta + costoCondimento

    costoKilo = costoTotal / pesoTotal

    croquetaApanada.costoProducto = costoKilo
    croquetaApanada.save()

    regCroqueta.costoKiloCroqueta = costoKilo
    regCroqueta.miga = pesoMiga
    regCroqueta.save()

    msj = 'Costeado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')



def GuardarCroqueta(request):
    idCorqueta = request.GET.get('idCroqueta')
    regCroqueta = TallerCroquetas.objects.get(pk = int(idCorqueta))

    if regCroqueta.puntoCroq.nombreBodega == 'Norte':
        croquetaApanada = Producto.objects.get(nombreProducto = 'Croqueta Apanada')
    else:
        croquetaApanada = Producto.objects.get(nombreProducto = 'Pollo Molido')

    croquetaCocida = Producto.objects.get(nombreProducto = 'Croqueta Cocinada')
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')
    miga = Producto.objects.get(nombreProducto = 'Miga Preparada')

    bodegaMiga = ProductoBodega.objects.get(bodega = regCroqueta.puntoCroq.codigoBodega,producto = miga.codigoProducto)
    bodegaCroquetaCocida = ProductoBodega.objects.get(bodega = regCroqueta.puntoCroq.codigoBodega,producto = croquetaCocida.codigoProducto)
    bodegaCroquetaApanada = ProductoBodega.objects.get(bodega = regCroqueta.puntoCroq.codigoBodega,producto = croquetaApanada.codigoProducto)
    bodegaCondimento = ProductoBodega.objects.get(bodega = regCroqueta.puntoCroq.codigoBodega,producto = condimento.codigoProducto)

    #*********************************************SALIDAS***********************************************************

    bodegaCroquetaCocida.pesoProductoStock -= regCroqueta.croqueta
    bodegaCroquetaCocida.save()

    movimiento = Movimientos()
    movimiento.tipo = 'CRQ%d'%(regCroqueta.id)
    movimiento.fechaMov = regCroqueta.fechaCroqueta
    movimiento.productoMov = croquetaCocida
    movimiento.nombreProd = croquetaCocida.nombreProducto
    movimiento.salida = regCroqueta.croqueta
    movimiento.desde = bodegaCroquetaCocida.bodega.nombreBodega
    movimiento.save()

    bodegaCondimento.pesoProductoStock -= regCroqueta.condimento
    bodegaCondimento.save()

    movimiento = Movimientos()
    movimiento.tipo = 'CRQ%d'%(regCroqueta.id)
    movimiento.fechaMov = regCroqueta.fechaCroqueta
    movimiento.productoMov = condimento
    movimiento.nombreProd = condimento.nombreProducto
    movimiento.salida = regCroqueta.condimento
    movimiento.desde = bodegaCondimento.bodega.nombreBodega
    movimiento.save()

    bodegaMiga.pesoProductoStock -= regCroqueta.miga
    bodegaMiga.save()

    movimiento = Movimientos()
    movimiento.tipo = 'CRQ%d'%(regCroqueta.id)
    movimiento.fechaMov = regCroqueta.fechaCroqueta
    movimiento.productoMov = miga
    movimiento.nombreProd = miga.nombreProducto
    movimiento.salida = regCroqueta.miga
    movimiento.desde = bodegaMiga.bodega.nombreBodega
    movimiento.save()

    #*************************************************ENTRADAS**********************************************************
    bodegaCroquetaApanada.pesoProductoStock += regCroqueta.pesoTotalCroqueta
    bodegaCroquetaApanada.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CRQ%d'%(regCroqueta.id)
    movimiento.fechaMov = regCroqueta.fechaCroqueta
    movimiento.productoMov = croquetaApanada
    movimiento.nombreProd = croquetaApanada.nombreProducto
    movimiento.entrada = regCroqueta.pesoTotalCroqueta
    movimiento.Hasta = bodegaCroquetaApanada.bodega.nombreBodega
    movimiento.save()

    regCroqueta.guardado = True
    regCroqueta.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionReApanado(request):

    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    usuario = request.user
    emp = Empleado.objects.select_related().get(usuario = usuario.username)
    if usuario.is_staff:
        plantilla = 'base.html'
        reApanado = TallerReapanado.objects.filter(fechaReApanado__range =(fechainicio,fechafin))

    else:
        plantilla = 'PuntoVentaNorte.html'
        reApanado = TallerReapanado.objects.filter(fechaReApanado__range =(fechainicio,fechafin), puntoReApanado= emp.punto.codigoBodega )


    if request.method == 'POST':

        formulario = ReapanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/fabricacion/tallerReApanado')
    else:
        formulario = ReapanadoForm(initial={'puntoReApanado':emp.punto.codigoBodega})

    return render_to_response('Fabricacion/GestionReApanado.html',{'plantilla':plantilla,'formulario':formulario,'reApanado':reApanado },
                              context_instance = RequestContext(request))

def borrarReapanado(request,idReApanado):
    reApanado = TallerReapanado.objects.select_related().get(pk = idReApanado)
    reApanado.delete()
    return HttpResponseRedirect('/fabricacion/tallerReApanado')

def GuardarReApanado(request):
    idReApanado = request.GET.get('idReApanado')
    reApanado = TallerReapanado.objects.get(pk = int(idReApanado))
    miga = Producto.objects.get(nombreProducto = 'Miga Preparada')
    chuletaCerdo = Producto.objects.get(nombreProducto = 'Filete Apanado Cerdo')
    chuletaPollo = Producto.objects.get(nombreProducto = 'Filete Apanado Pollo')
    pesoReapanado = reApanado.pesoTotalReApanado
    pesoChuleta = reApanado.pesoChuleta

    bodegaMiga = ProductoBodega.objects.get(bodega = reApanado.puntoReApanado.codigoBodega,producto = miga.codigoProducto)
    bodegaChuleta = ProductoBodega.objects.get(bodega = reApanado.puntoReApanado.codigoBodega,producto = reApanado.chuelta.codigoProducto)
    bodegaChuletaCerdo = ProductoBodega.objects.get(bodega = reApanado.puntoReApanado.codigoBodega,producto = chuletaCerdo.codigoProducto)
    bodegaChuletaPollo = ProductoBodega.objects.get(bodega = reApanado.puntoReApanado.codigoBodega,producto = chuletaPollo  .codigoProducto)

    migaUtilizada = pesoReapanado - pesoChuleta

    #bodegaChuleta.pesoProductoStock -= pesoChuleta
    #bodegaChuleta.save()
    movimiento = Movimientos()
    movimiento.tipo = 'RAP%d'%(reApanado.id)
    movimiento.fechaMov = reApanado.fechaReApanado
    movimiento.productoMov = reApanado.chuelta
    movimiento.nombreProd = reApanado.chuelta.nombreProducto
    movimiento.salida = reApanado.pesoChuleta
    movimiento.desde = bodegaChuleta.bodega.nombreBodega
    movimiento.save()

    bodegaMiga.pesoProductoStock -= migaUtilizada
    bodegaMiga.save()

    movimiento = Movimientos()
    movimiento.tipo = 'RAP%d'%(reApanado.id)
    movimiento.fechaMov = reApanado.fechaReApanado
    movimiento.productoMov = miga
    movimiento.nombreProd = miga.nombreProducto
    movimiento.desde = bodegaMiga.bodega.nombreBodega
    movimiento.salida = migaUtilizada
    movimiento.save()

    if reApanado.chuelta.grupo.nombreGrupo == 'Cerdos':

        #entra
        bodegaChuletaCerdo.pesoProductoStock += migaUtilizada
        bodegaChuletaCerdo.save()
        movimiento = Movimientos()
        movimiento.tipo = 'RAP%d'%(reApanado.id)
        movimiento.fechaMov = reApanado.fechaReApanado
        movimiento.productoMov = chuletaCerdo
        movimiento.nombreProd = chuletaCerdo.nombreProducto
        movimiento.entrada = pesoReapanado
        movimiento.Hasta = bodegaChuletaCerdo.bodega.nombreBodega
        movimiento.save()
    else:
        bodegaChuletaPollo.pesoProductoStock += migaUtilizada
        bodegaChuletaPollo.save()
        movimiento = Movimientos()
        movimiento.tipo = 'RAP%d'%(reApanado.id)
        movimiento.fechaMov = reApanado.fechaReApanado
        movimiento.productoMov = chuletaPollo
        movimiento.nombreProd = chuletaPollo.nombreProducto
        movimiento.entrada = pesoReapanado
        movimiento.Hasta = bodegaChuletaPollo.bodega.nombreBodega
        movimiento.save()

    reApanado.guardado = True
    reApanado.miga = migaUtilizada
    reApanado.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GestionConversiones(request):
    fechainicio = date.today() - timedelta(days=5)
    fechafin = date.today()
    usuario = request.user
    emp = Empleado.objects.select_related().get(usuario = usuario.username)
    if usuario.is_staff:
        conversiones = Conversiones.objects.filter(fechaConversion__range =(fechainicio,fechafin))
        plantilla = 'base.html'
    else:
        conversiones = Conversiones.objects.filter(fechaConversion__range =(fechainicio,fechafin)).filter(puntoConversion = emp.punto.codigoBodega)
        plantilla = 'PuntoVentaNorte.html'

    #conversiones = Conversiones.objects.all()

    if request.method == 'POST':
        formulario = ConversionesForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/conversiones')
    else:
        formulario = ConversionesForm(initial={'puntoConversion':emp.punto.codigoBodega})

    return render_to_response('Fabricacion/GestionReConversiones.html',{'plantilla':plantilla,'formulario':formulario,'conversiones':conversiones },
                              context_instance = RequestContext(request))


def BorrarConversiones(request,idConversion):
    conversion = Conversiones.objects.get(pk = idConversion)
    conversion.delete()
    return HttpResponseRedirect('/fabricacion/conversiones')


def GuardarConversion(request):
    idConversion = request.GET.get('idConversion')
    conversion = Conversiones.objects.get(pk = int(idConversion))
    #Separamos la cadena donde esta el nombre del producto
    pro1 = str(conversion.productoUno)
    pro2 = str(conversion.productoDos)

    nombre1 = pro1.split(' ,')
    nombre2 = pro2.split(' ,')
    producto1 = Producto.objects.get(nombreProducto = nombre1[1])
    producto2 = Producto.objects.get(nombreProducto = nombre2[1])

    bodegaP1 = ProductoBodega.objects.get(bodega = conversion.puntoConversion.codigoBodega,producto = producto1.codigoProducto)
    bodegaP2 = ProductoBodega.objects.get(bodega = conversion.puntoConversion.codigoBodega,producto = producto2.codigoProducto)

    costoP1 = producto1.costoProducto
    costoP2 = producto2.costoProducto



    #****************************************************SALIDA********************************************************

    bodegaP1.pesoProductoStock -= conversion.pesoConversion
    bodegaP1.unidadesStock -= conversion.unidades
    bodegaP1.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CON%d'%(conversion.id)
    movimiento.fechaMov = conversion.fechaConversion
    movimiento.productoMov = producto1
    movimiento.nombreProd = producto1.nombreProducto
    movimiento.desde = conversion.puntoConversion.nombreBodega
    if conversion.pesoConversion == 0:
        movimiento.salida = conversion.unidades
    else:
        movimiento.salida = conversion.pesoConversion
    movimiento.save()

    #****************************************************ENTRADA********************************************************

    bodegaP2.pesoProductoStock += conversion.pesoConversion
    bodegaP2.unidadesStock += conversion.unidades
    bodegaP2.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CON%d'%(conversion.id)
    movimiento.fechaMov = conversion.fechaConversion
    movimiento.productoMov = producto2
    movimiento.nombreProd = producto2.nombreProducto
    movimiento.Hasta = conversion.puntoConversion.nombreBodega
    if conversion.pesoConversion == 0:
        movimiento.entrada = conversion.unidades
    else:
        movimiento.entrada = conversion.pesoConversion
    movimiento.save()

    conversion.costoP1 = costoP1
    conversion.costoP2 = costoP2
    conversion.guardado = True
    conversion.save()

    msj = 'Guardado exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def TemplateRepoConversiones(request):
    bodegas = Bodega.objects.all()
    return render_to_response('Fabricacion/TemplateRepoConversiones.html',{'bodegas':bodegas},context_instance = RequestContext(request))

def RepoConversiones(request):
    idPorducto = request.GET.get('producto')
    idBodega = request.GET.get('bodega')

    bodega = Bodega.objects.get(pk = int(idBodega))

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    conversiones = Conversiones.objects.select_related().filter(fechaConversion__range = (finicio,ffin) , puntoConversion = bodega.codigoBodega).order_by('productoUno')

    respuesta = serializers.serialize('json',conversiones)

    return HttpResponse(respuesta,mimetype='application/json')

def TemplateTraslados(request):
    productos = Producto.objects.all()
    bodegas = Bodega.objects.all()

    return render_to_response('Fabricacion/TemplateFiltroTraslado.html',{'productos':productos,'bodegas':bodegas },
                              context_instance = RequestContext(request))

def ReporteTraslados(request):
    idPorducto = request.GET.get('producto')
    idBodega = request.GET.get('bodega')

    bodega = Bodega.objects.get(pk = int(idBodega))

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    traslados = DetalleTraslado.objects.filter(traslado__fechaTraslado__range = (finicio,ffin))\
        .filter(productoTraslado = int(idPorducto)).filter(traslado__bodegaDestino = bodega.nombreBodega)

    respuesta = serializers.serialize('json',traslados)

    return HttpResponse(respuesta,mimetype='application/json')

#************************************************REPORTE TRASLADO POR BODEGA*******************************************
def TemplateTrasladosBodega(request):
    bodegas = Bodega.objects.all()
    return render_to_response('Fabricacion/TemplateTrasladoBodega.html',{'bodegas':bodegas },
                              context_instance = RequestContext(request))

def ReporteTrasladosBodega(request):
    idBodega = request.GET.get('bodega')

    bodega = Bodega.objects.get(pk = int(idBodega))

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    traslados = Traslado.objects.filter(fechaTraslado__range = (finicio,ffin)).filter(bodegaDestino = bodega.nombreBodega)

    ListaTraslado = {}

    for traslado in traslados:
        detalleTraslados = DetalleTraslado.objects.filter(traslado = traslado.codigoTraslado)
        for detalle in detalleTraslados:
            ListaTraslado[detalle.productoTraslado.nombreProducto] = 0

    for traslado in traslados:
        detalleTraslados = DetalleTraslado.objects.filter(traslado = traslado.codigoTraslado)
        for detalle in detalleTraslados:
            ListaTraslado[detalle.productoTraslado.nombreProducto] += ceil(detalle.pesoTraslado)


    lista = {'traslado':ListaTraslado}

    respuesta = json.dumps(lista)

    return HttpResponse(respuesta,mimetype='application/json')

def  TemplateUtilidadPorLote(request):
    fechainicio = date.today() - timedelta(days=80)
    fechafin = date.today()

    q1 = Compra.objects.select_related().filter(tipo__nombreGrupo = 'Reses',bodegaCompra__nombreBodega = 'General',fechaCompra__range =(fechainicio,fechafin)).order_by('fechaCompra')
    q2 = Compra.objects.select_related().filter(tipo__nombreGrupo = 'Cerdas',bodegaCompra__nombreBodega = 'General',fechaCompra__range =(fechainicio,fechafin)).order_by('fechaCompra')
    q3 = Compra.objects.select_related().filter(tipo__nombreGrupo = 'Cerdos',bodegaCompra__nombreBodega = 'General',fechaCompra__range =(fechainicio,fechafin)).order_by('fechaCompra')
    compras = q1 | q2 | q3

    return render_to_response('Fabricacion/TemplateUtilidadPorLote.html',{'compras':compras},
                              context_instance = RequestContext(request))

def ReporteUtilidadPorLote(request):
    idCompra = request.GET.get('idCompra')
    idLista = request.GET.get('idLista')
    compra = Compra.objects.get(pk = int(idCompra))
    canales = Canal.objects.select_related().filter(recepcion__compra = int(idCompra)).order_by('planilla')
    ListaPesos = {}
    ListaCosto = {}
    ListaVenta = {}
    costoOperativo = {}
    pesoCanal = {}
    TotalDespostadoSinDesecho = {}
    TotalDespostadoSinDesecho['Total despostado'] = 0
    pesoCanal['Peso Canales'] = 0
    costoOperativo['Costo Operativo'] = 0
    vrKiloCanal = {}
    vrKiloCanal['Vr. Kilo Canal'] = 0
    costoProducto = {}


    vrCompra = compra.vrCompra

    carnes = 0
    costillas =0
    huesos = 0
    subproductos = 0
    desechos = 0

    #inicializamos la lista
    for canal in canales:
        if canal.planilla != '' and canal.planilla != None:
            detalleDespostes = DetallePlanilla.objects.filter(planilla__codigoPlanilla = canal.planilla.codigoPlanilla)

            for detalle in detalleDespostes:
                ListaPesos[detalle.producto.nombreProducto] = 0
                ListaCosto[detalle.producto.nombreProducto] = 0
                ListaVenta[detalle.producto.nombreProducto] = 0
                costoProducto[detalle.producto.nombreProducto] = 0


    planillaAnterior = 0
    planillaActual = 0
    cont = 0
    perdidaPC = 0


    for canal in canales:
        if canal.planilla != '' and canal.planilla != None:
            planillaActual = canal.planilla.codigoPlanilla
            detalleDespostes = DetallePlanilla.objects.filter(planilla__codigoPlanilla = canal.planilla.codigoPlanilla)
            recepcion = PlanillaRecepcion.objects.get(pk = canal.recepcion.codigoRecepcion)
            perdidaPC = recepcion.difPieCanal
            cont = 0
            pesoCanal['Peso Canales'] += ceil(canal.pesoPorkilandia)
            vrKiloCanal['Vr. Kilo Canal'] = canal.recepcion.vrKiloCanal

            if planillaAnterior != planillaActual:

                pln = PlanillaDesposte.objects.get(pk = planillaActual)
                costoOperativo['Costo Operativo'] += (pln.mod + pln.cif)
                for detalle in detalleDespostes:
                    ListaPesos[detalle.producto.nombreProducto] += ceil(detalle.PesoProducto)
                    costoProducto[detalle.producto.nombreProducto] = detalle.costoProducto
                    if cont == 0:
                        carnes += ceil(detalle.pesoCarne)
                        costillas += ceil(detalle.pesoCostilla)
                        subproductos += ceil(detalle.pesoSubProd)
                        huesos += ceil(detalle.pesoHueso)
                        desechos += ceil(detalle.pesoDesecho)
                        cont += 1

            planillaAnterior = planillaActual

    for key ,value in ListaPesos.items():
        producto = Producto.objects.get(nombreProducto = key)
        ListaCosto[key] = (value /1000) * producto.costoProducto

    for key ,value in ListaPesos.items():
        producto = Producto.objects.get(nombreProducto = key)
        ListaVenta[key] = (value /1000) * (producto.costoProducto * 1.23)

    tocino = 0

    for key ,value in ListaPesos.items():
        if key == 'Tocino' or key == 'Tocino Cerda':
            tocino = value


    subproductos = subproductos - tocino
    TotalDespostado = carnes + costillas + subproductos + huesos + tocino + desechos
    TotalDespostadoSinDesecho['Total despostado'] = carnes + costillas + subproductos + huesos + tocino

    adicionales = {}
    adicionales['Carne'] = (carnes * 100)/TotalDespostado
    adicionales['Costilla'] = (costillas * 100)/TotalDespostado
    adicionales['SubProducto'] = (subproductos * 100)/TotalDespostado
    adicionales['Hueso'] = (huesos * 100)/TotalDespostado
    adicionales['Grasa'] = (tocino * 100)/TotalDespostado
    adicionales['Desecho'] = (desechos * 100)/TotalDespostado

    perdida = {}
    perdida['Perdida de Peso'] = ceil(perdidaPC)

    compras = {}
    compras['Total Compra'] = vrCompra


    listas = {'costoProducto':costoProducto,'vrKiloCanal':vrKiloCanal,'TotalDespostadoSinDesecho':TotalDespostadoSinDesecho,'pesoCanal':pesoCanal,'costoOperativo':costoOperativo,'Pesos':ListaPesos,'adicionales':adicionales,'perdida':perdida,
              'costo':ListaCosto,'compras':compras,'ListaVenta':ListaVenta}

    print(costoOperativo)


    respuesta = json.dumps(listas)

    return HttpResponse(respuesta,mimetype='application/json')


def GestionEnsBola(request):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    ensBolas = TallerBolaEnsalinada.objects.filter(fechaBolaCondimentada__range =(fechainicio,fechafin))
    #conversiones = Conversiones.objects.all()

    if request.method == 'POST':
        formulario = EnsBolaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/ensBola')
    else:
        formulario = EnsBolaForm()

    return render_to_response('Fabricacion/GestionEnsBola.html',{'formulario':formulario,'ensBolas':ensBolas },
                              context_instance = RequestContext(request))
def EditaEnsBola(request,idEns):
    fechainicio = date.today() - timedelta(days=10)
    fechafin = date.today()
    ensBolas = TallerBolaEnsalinada.objects.filter(fechaBolaCondimentada__range =(fechainicio,fechafin))
    ensBola = TallerBolaEnsalinada.objects.get(pk = idEns)
    #conversiones = Conversiones.objects.all()

    if request.method == 'POST':
        formulario = EnsBolaForm(request.POST,instance=ensBola)
        if formulario.is_valid():
            dato = formulario.save()
            #Guardamos el producto Ensalinado
            bolaEns =  Producto.objects.get(nombreProducto = 'Bola')
            bodega = ProductoBodega.objects.get(bodega = dato.puntoBodega.codigoBodega,producto = bolaEns.codigoProducto)
            bodega.pesoProductoStock += dato.pesoDespues
            bodega.save()

            return HttpResponseRedirect('/fabricacion/ensBola')
    else:
        formulario = EnsBolaForm(instance=ensBola)

    return render_to_response('Fabricacion/GestionEnsBola.html',{'formulario':formulario,'ensBolas':ensBolas },
                              context_instance = RequestContext(request))

def CostearEnsBola(request):

    idEnsalinado = request.GET.get('idEnsalinado')
    ensBola = TallerBolaEnsalinada.objects.get(pk = int(idEnsalinado))
    bolaEns =  Producto.objects.get(nombreProducto = 'Bola Ensalinada')

    pesoCarne= ensBola.pesoBola
    pesoSal = ensBola.sal
    pesoPapaina = ensBola.papaina

    costoSal = Producto.objects.get(nombreProducto = 'Sal').costoProducto * (pesoSal/1000)
    costoPapaina = Producto.objects.get(nombreProducto = 'Papaina').costoProducto * (pesoPapaina/1000)
    costoCarne = Producto.objects.get(nombreProducto = 'Bola').costoProducto * (pesoCarne/1000)

    costoTotal = costoSal + costoPapaina + costoCarne
    pesoTotal = pesoCarne + pesoSal + pesoPapaina
    costoKilo = costoTotal/(ensBola.pesoDespues/1000)

    bolaEns.costoProducto = costoKilo
    bolaEns.save()

    ensBola.costoKiloEns = costoKilo
    ensBola.pesoTotal = pesoTotal
    ensBola.save()

    msj = 'Costeado Exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def GuardarEnsBola(request):

    idEnsalinado = request.GET.get('idEnsalinado')
    ensBola = TallerBolaEnsalinada.objects.get(pk = int(idEnsalinado))

    bolaEns =  Producto.objects.get(nombreProducto = 'Bola Ensalinada')
    pesoAntes = ensBola.pesoBola
    pesoSal = ensBola.sal
    pesoPapaina = ensBola.papaina

    sal = Producto.objects.get(nombreProducto = 'Sal')
    papaina = Producto.objects.get(nombreProducto = 'Papaina')
    carne = Producto.objects.get(nombreProducto = 'Bola')

    bodegaSal = ProductoBodega.objects.get(bodega = 6,producto = sal.codigoProducto)
    bodegaSal.pesoProductoStock -= pesoSal
    bodegaSal.save()

    bodegaPapaina = ProductoBodega.objects.get(bodega = 6,producto = papaina.codigoProducto)
    bodegaPapaina.pesoProductoStock -= pesoPapaina
    bodegaPapaina.save()

    bodegaCarne = ProductoBodega.objects.get(bodega = ensBola.puntoBodega.codigoBodega,producto = carne.codigoProducto)
    bodegaCarne.pesoProductoStock -= pesoAntes
    bodegaCarne.save()

    ensBola.guardado = True
    ensBola.save()

    msj = 'Guardado Exitoso'
    respuesta = json.dumps(msj)
    return HttpResponse(respuesta,mimetype='application/json')

def TemplateTalleresPuntos(request):
    bodegas = Bodega.objects.filter(codigoBodega__range = (1,4))
    return render_to_response('Fabricacion/TemplateTalleresPuntos.html',{'bodegas':bodegas},
                              context_instance = RequestContext(request))

def ReporteTallerPunto(request):

    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')
    bodega = request.GET.get('bodega')


    pesoFrito = {}
    pesoFrito['Frito Condimentado'] = 0

    pesoCroqueta = {}
    pesoCroqueta['Croqueta Apanada'] = 0

    pesoBolaCond = {}
    pesoBolaCond['Bola Condimentada'] = 0

    pesoAgujaCond = {}
    pesoAgujaCond['Aguja Condimentada'] = 0

    pesoRecortesPollo = {}
    pesoRecortesPollo['Recortes de Pollo'] = 0

    pesoPernilesPollo = {}
    pesoPernilesPollo['Perniles de Pollo'] = 0

    pesoBolaEns = {}
    pesoBolaEns['Carne Ensalinada'] = 0

    pesoMolida = {}
    pesoMolida['Carne Molida'] = 0




    fechaInicio = str(inicio)
    fechaFin = str(fin)
    formatter_string = "%d/%m/%Y"
    fi = datetime.strptime(fechaInicio, formatter_string)
    ff = datetime.strptime(fechaFin, formatter_string)
    finicio = fi.date()
    ffin = ff.date()

    frito = TallerFrito.objects.filter(fechaFrito__range = (finicio,ffin)).filter(punto = int(bodega))
    promedioFrito = frito.aggregate(Avg('costoKiloFrito'))

    for fr in frito:
        pesoFrito['Frito Condimentado'] += ceil(fr.pesoTotalFrito)


    croquetas = TallerCroquetas.objects.filter(fechaCroqueta__range = (finicio,ffin)).filter(puntoCroq = int(bodega))
    promedioCroqueta = croquetas.aggregate(Avg('costoKiloCroqueta'))

    for croqueta in croquetas:
        pesoCroqueta['Croqueta Apanada'] += ceil(croqueta.pesoTotalCroqueta)

#************************************************************************************************
    BolaCond = TallerCarneCondimentada.objects.select_related().filter(productoCond__nombreProducto = 'Bola',fechaCarCond__range = (finicio,ffin), puntoCond = int(bodega))
    promedioBolaCond = BolaCond.aggregate(Avg('costoKiloCond'))

    for bCond in BolaCond:
        pesoBolaCond['Bola Condimentada'] += ceil(bCond.pesoTotalCond)


    AgujaCond = TallerCarneCondimentada.objects.select_related().filter(productoCond__nombreProducto = 'Agujas',fechaCarCond__range = (finicio,ffin), puntoCond = int(bodega))
    promedioAgujaCond = AgujaCond.aggregate(Avg('costoKiloCond'))

    for aCond in AgujaCond:
        pesoAgujaCond['Aguja Condimentada'] += ceil(aCond.pesoTotalCond)

    RecortCond = TallerCarneCondimentada.objects.select_related().filter(productoCond__nombreProducto = 'Recortes de pollo',fechaCarCond__range = (finicio,ffin), puntoCond = int(bodega))
    promedioRecorteCond = RecortCond.aggregate(Avg('costoKiloCond'))

    for rCond in RecortCond:
        pesoRecortesPollo['Recortes de Pollo'] += ceil(rCond.pesoTotalCond)


    PernilCond = TallerCarneCondimentada.objects.select_related().filter(productoCond__nombreProducto = 'Pernil pollo',fechaCarCond__range = (finicio,ffin), puntoCond = int(bodega))
    promedioPernilCond = PernilCond.aggregate(Avg('costoKiloCond'))

    for pCond in PernilCond:
        pesoPernilesPollo['Perniles de Pollo'] += ceil(pCond .pesoTotalCond)

#************************************************************************************************

    bolaEns = TallerBolaEnsalinada.objects.filter(fechaBolaCondimentada__range = (finicio,ffin)).filter(puntoBodega = int(bodega))
    promedioBolaEns = bolaEns.aggregate(Avg('costoKiloEns'))

    for bEns in bolaEns:
        pesoBolaEns['Carne Ensalinada'] += ceil(bEns.pesoDespues)


    carneMolida = Conversiones.objects.filter(fechaConversion__range = (finicio,ffin)).\
        filter(puntoConversion = int(bodega)).filter(productoUno = 'Cogotes , (Reses)').\
        filter(productoDos = 'Carne Molida , (Reses)')

    promedioMolida = carneMolida.aggregate(Avg('costoP1'))

    for cMolida in carneMolida:
        pesoMolida['Carne Molida'] += ceil(cMolida.pesoConversion)


    listas = {'promedioFrito':promedioFrito,'pesoFrito':pesoFrito,'promedioCroqueta':promedioCroqueta,
              'pesoCroqueta':pesoCroqueta,
              'promedioBolaCond':promedioBolaCond,'pesoBolaCond':pesoBolaCond,
              'promedioAgujaCond':promedioAgujaCond,'pesoAgujaCond':pesoAgujaCond,
              'promedioPernilCond':promedioPernilCond,'pesoPernilesPollo':pesoPernilesPollo,
              'promedioRecorteCond':promedioRecorteCond,'pesoRecortesPollo':pesoRecortesPollo,
              'promedioBolaEns':promedioBolaEns,'pesoBolaEns':pesoBolaEns,'promedioMolida':promedioMolida,'pesoMolida':pesoMolida}


    respuesta = json.dumps(listas)

    return HttpResponse(respuesta,mimetype='application/json')


def GestionChicharron(request):
    fechainicio = date.today() - timedelta(days=20)
    fechafin = date.today()
    chicharrones = TallerChicharron.objects.filter(fechaChicharron__range =(fechainicio,fechafin))



    if request.method == 'POST':

        formulario = ChicharronForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/fabricacion/chicharrones')
    else:
        formulario = ChicharronForm()

    return render_to_response('Fabricacion/GestionChicharron.html',{'formulario':formulario,'chicharrones':chicharrones },
                              context_instance = RequestContext(request))

def CostearChicharoones(request):
    idChicharron = request.GET.get('idChicharron')
    chicharron = TallerChicharron.objects.get(pk = int(idChicharron))

    producto = Producto.objects.get(pk = chicharron.productoCh.codigoProducto)
    sal = Producto.objects.get(nombreProducto = 'Sal')
    tocino = 0
    if producto.grupo.nombreGrupo == 'Cerdos':
        tocino = Producto.objects.get(nombreProducto = 'Tocino')
    else:
        tocino = Producto.objects.get(nombreProducto = 'Tocino Cerda')

    costoSal = sal.costoProducto
    costoTocino = tocino.costoProducto
    pesoSal = chicharron.Sal
    pesoTocino = chicharron.Tocino
    pesochicharron = chicharron.chicharron
    pesoGrasa = chicharron.grasa
    undChicharron = chicharron.undChicharron
    undGrasa = chicharron.undGrasa
    costoTarrina = Producto.objects.get(nombreProducto = 'Tarrinas').costoProducto

    costoTotalTocino = (pesoTocino /1000) * costoTocino
    costoTotalSal = (pesoSal /1000) * costoSal

    CostoTotalChicharron = costoTotalTocino + chicharron.cif + chicharron.mod + costoTotalSal
    CostoKiloProcesado = CostoTotalChicharron / ((pesochicharron/1000) + (pesoGrasa/1000))

    pesoUnitarioChichcarron = pesochicharron / undChicharron
    pesoUnitarioGrasa = pesoGrasa / undGrasa

    costoUnitarioChicharron = (pesoUnitarioChichcarron /1000) * CostoKiloProcesado + 13
    costoUnitarioGrasa = (pesoUnitarioGrasa /1000) * CostoKiloProcesado + costoTarrina

    chicharron.costoUndChicharron = costoUnitarioChicharron
    chicharron.costoUndGrasa = costoUnitarioGrasa
    chicharron.save()

    msj = 'Costeo Exitoso'

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')

def GuardarChicharron(request):
    idChicharron = request.GET.get('idChicharron')
    chicharron = TallerChicharron.objects.get(pk = int(idChicharron))
    producto = Producto.objects.get(pk = chicharron.productoCh.codigoProducto)
    sal = Producto.objects.get(nombreProducto = 'Sal')
    tocino = 0
    if producto.grupo.nombreGrupo == 'Cerdos':
        tocino = Producto.objects.get(nombreProducto = 'Tocino')
    else:
        tocino = Producto.objects.get(nombreProducto = 'Tocino Cerda')

    tarrina = Producto.objects.get(nombreProducto = 'Tarrinas')
    grasaEnTarro = Producto.objects.get(nombreProducto = 'Grasa En Tarro')
    chicharronProd = Producto.objects.get(nombreProducto = 'Chicharrones')

    BodegaSal = ProductoBodega.objects.get(bodega = 6,producto = sal.codigoProducto)
    BodegaTocino = ProductoBodega.objects.get(bodega = 5 , producto = tocino.codigoProducto)
    BodegaTarrina = ProductoBodega.objects.get(bodega = 5 , producto = tarrina.codigoProducto)
    BodegagrasaEnTarro = ProductoBodega.objects.get(bodega = 5 , producto = grasaEnTarro.codigoProducto)
    BodegachicharronProd = ProductoBodega.objects.get(bodega = 5 , producto = chicharronProd.codigoProducto)

    BodegaSal.pesoProductoStock -= chicharron.Sal
    BodegaSal.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CHI%d'%(chicharron.id)
    movimiento.fechaMov = chicharron.fechaChicharron
    movimiento.productoMov = sal
    movimiento.nombreProd = sal.nombreProducto
    movimiento.desde = BodegaSal.bodega.nombreBodega
    movimiento.salida = chicharron.Sal
    movimiento.save()

    BodegaTocino.pesoProductoStock -= chicharron.Tocino
    BodegaTocino.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CHI%d'%(chicharron.id)
    movimiento.fechaMov = chicharron.fechaChicharron
    movimiento.productoMov = tocino
    movimiento.nombreProd = tocino.nombreProducto
    movimiento.desde = BodegaTocino.bodega.nombreBodega
    movimiento.salida = chicharron.Tocino
    movimiento.save()


    BodegaTarrina.unidadesStock -= chicharron.undGrasa
    BodegaTarrina.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CHI%d'%(chicharron.id)
    movimiento.fechaMov = chicharron.fechaChicharron
    movimiento.productoMov = tarrina
    movimiento.nombreProd = tarrina.nombreProducto
    movimiento.desde = BodegaTarrina.bodega.nombreBodega
    movimiento.salida = chicharron.undGrasa
    movimiento.save()

    BodegagrasaEnTarro.unidadesStock += chicharron.undGrasa
    BodegagrasaEnTarro.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CHI%d'%(chicharron.id)
    movimiento.fechaMov = chicharron.fechaChicharron
    movimiento.productoMov = grasaEnTarro
    movimiento.nombreProd = grasaEnTarro.nombreProducto
    movimiento.Hasta = BodegagrasaEnTarro.bodega.nombreBodega
    movimiento.entrada = chicharron.undGrasa
    movimiento.save()

    BodegachicharronProd.unidadesStock += chicharron.undChicharron
    BodegachicharronProd.save()
    movimiento = Movimientos()
    movimiento.tipo = 'CHI%d'%(chicharron.id)
    movimiento.fechaMov = chicharron.fechaChicharron
    movimiento.productoMov = chicharronProd
    movimiento.nombreProd = chicharronProd.nombreProducto
    movimiento.Hasta = BodegachicharronProd.bodega.nombreBodega
    movimiento.entrada = chicharron.undChicharron
    movimiento.save()

    chicharron.guardado = True
    chicharron.save()

    msj = 'Guardado Exitoso'

    respuesta = json.dumps(msj)

    return HttpResponse(respuesta,mimetype='application/json')