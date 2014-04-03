from django.shortcuts import render_to_response, HttpResponseRedirect

from django.core.context_processors import csrf
from django.template import RequestContext

from inventario.Forms.forms import ProductoForm

from inventario.models import Producto


# Create your views here.

def listaProductos(request):
    productos = Producto.objects.all()
    return render_to_response('listaProducto.html',{'productos':productos }, context_instance = RequestContext(request))


def productosFRM(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario = ProductoForm()

    args = {}
    args.update(csrf(request))
    args['form'] = formulario
    return render_to_response('nuevoProducto.html',args, context_instance = RequestContext(request))

