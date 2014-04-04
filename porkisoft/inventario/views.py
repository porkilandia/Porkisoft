from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

from inventario.Forms.forms import ProductoForm
from inventario.models import Producto




# Create your views here.

def listaProductos(request):
    productos = Producto.objects.all().order_by('nombreProducto')
    return render_to_response('listaProducto.html',{'productos':productos },
                              context_instance = RequestContext(request))

def agregar_producto(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario =ProductoForm()

    return render_to_response('nuevoProducto.html',{'formulario':formulario},
                              context_instance = RequestContext(request))

def borrar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    producto.delete()
    return  HttpResponseRedirect('/listaProd')

def editar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario = ProductoForm(instance=producto)
    return  render_to_response('modificaProducto.html',{'formulario':formulario},
                               context_instance = RequestContext(request))