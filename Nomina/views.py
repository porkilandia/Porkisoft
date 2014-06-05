from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext

from Nomina.Forms import *


def GestionEmpleados(request):

    empleados = Empleado.objects.all()

    if request.method == 'POST':

        formulario = EmpleadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/nomina/empleado')
    else:
        formulario =EmpleadoForm()

    return render_to_response('Inventario/../porkisoft/templates/Nomina/GestionEmpleados.html',{'formulario':formulario,'empleados':empleados },
                              context_instance = RequestContext(request))

def GestionCargos(request):

    cargos = Cargo.objects.all()

    if request.method == 'POST':

        formulario = CargoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/nomina/cargo')
    else:
        formulario = CargoForm()

    return render_to_response('Inventario/../porkisoft/templates/Nomina/Cargo.html',{'formulario':formulario,'cargos':cargos },
                              context_instance = RequestContext(request))
