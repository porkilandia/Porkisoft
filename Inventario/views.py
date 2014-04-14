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

    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario =ProductoForm()

    return render_to_response('listaProducto.html',{'formulario':formulario,'productos':productos },
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
    return  render_to_response('listaProducto.html',{'formulario':formulario,'productos':productos },
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

    return render_to_response('listaSubProducto.html',{'formulario':formulario,'subproductos':subproductos },
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

    return  render_to_response('listaSubProducto.html',{'formulario':formulario,'subproductos':subproductos},
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

    return render_to_response('GestionSubProducto.html',{'Tunds':totalUnd,'TPeso':totalPeso,'formulario':formulario,
                                                         'subrpoductos': subrpoductos,
                                                         'desubproductos': desubproductos},
                                                        context_instance = RequestContext(request))

def borrarDetalleSp(request, idDetalle):
    detsubproducto = DetalleSubProducto.objects.get(pk=idDetalle)
    detsubproducto.delete()
    return  HttpResponseRedirect('/verSubProductos')