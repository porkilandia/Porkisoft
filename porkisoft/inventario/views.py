from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

from inventario.Forms.forms import *
from inventario.models import *


# Create your views here.

def listaProductos(request):
    productos = Producto.objects.all().order_by('nombreProducto')
    return render_to_response('listaProducto.html',{'productos':productos },
                              context_instance = RequestContext(request))

def listaSubProductos(request):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    return render_to_response('listaSubProducto.html',{'subproductos':subproductos },
                              context_instance = RequestContext(request))

def index(request):
    titulo = 'tabla de contenido'
    return  render_to_response('index.html',{'titulo':titulo},
                              context_instance = RequestContext(request))

def agregar_producto(request):
    if request.method == 'POST':
        formulario = Producto(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario =Producto()

    return render_to_response('nuevoProducto.html',{'formulario':formulario},
                              context_instance = RequestContext(request))

def borrar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    producto.delete()
    return  HttpResponseRedirect('/listaProd')

def editar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    if request.method == 'POST':
        formulario = Producto(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario = Producto(instance=producto)
    return  render_to_response('modificaProducto.html',{'formulario':formulario},
                               context_instance = RequestContext(request))

def AgregarSubProducto(request):
    subproductos = SubProducto.objects.all()
    if request.method == 'POST':
        formulario = SubProductoForm(request.POST)
        if formulario.is_valid():
            for subproducto in subproductos:
                if formulario.nombreSubProducto == subproducto.nombreSubProducto:
                    formulario =SubProductoForm()

                else:
                    formulario.save()
                    return HttpResponseRedirect('/prueba'+ formulario.id)
    else:
        formulario =SubProductoForm()

    return render_to_response('nuevoSubProducto.html',{'formulario':formulario},
                              context_instance = RequestContext(request))

def AgregarDetSubProducto(request):
    detsubproductos = DetalleSubProducto.objects.all().order_by('id')
    if request.method == 'POST':
        formulario = DetSubProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            #return HttpResponseRedirect('/addDSprod')
    else:
        formulario = DetSubProductoForm()

    return render_to_response('nuevoDetSubProducto.html',{'formulario':formulario , 'detsubproductos':detsubproductos},
                              context_instance = RequestContext(request))

def prueba(request,id_subproducto):
    subrpoductos = SubProducto.objects.get(pk = id_subproducto)
    desubproductos = DetalleSubProducto.objects.filter(subproducto = id_subproducto)

    return render_to_response('index.html',{'subrpoductos': subrpoductos, 'desubproductos': desubproductos},
                              context_instance = RequestContext(request))
