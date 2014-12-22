from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponseRedirect
from Forms import *


from Nomina.Forms import *
from Ventas.models import ConfiguracionPuntos


def GestionEmpleados(request):

    empleados = Empleado.objects.all()

    if request.method == 'POST':

        formulario = EmpleadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/nomina/empleado')
    else:
        formulario =EmpleadoForm()

    return render_to_response('Nomina/GestionEmpleados.html',{'formulario':formulario,'empleados':empleados },
                              context_instance = RequestContext(request))

def EditaEmpleados(request,idEmpleado):
    empleado = Empleado.objects.get(pk = idEmpleado)
    empleados = Empleado.objects.all()

    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST,instance=empleado)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/nomina/empleado')
    else:
        formulario =EmpleadoForm(instance = empleado)

    return render_to_response('Nomina/GestionEmpleados.html',{'formulario':formulario,'empleados':empleados },
                              context_instance = RequestContext(request))


def GestionCargos(request):

    cargos = Cargo.objects.all()

    if request.method == 'POST':

        formulario = CargoForm(request.POST)

        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/nomina/cargo')
    else:
        formulario = CargoForm()

    return render_to_response('Nomina/Cargo.html',{'formulario':formulario,'cargos':cargos },
                              context_instance = RequestContext(request))

def GestionUsuario(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            empleado = formulario.cleaned_data['empleado']
            usuario = formulario.cleaned_data['usuario']
            clave = formulario.cleaned_data['clave']

            encargado = Empleado.objects.get(pk = empleado.codigoEmpleado)
            encargado.usuario = usuario
            encargado.save()

            user = User.objects.create_user(username=usuario,email=None,password=clave)
            user.save()
            return HttpResponseRedirect('/nomina/usuarios')
    else:
        formulario = UsuarioForm()
    return render_to_response('Nomina/GestionUsuarios.html',{'formulario':formulario,'usuarios':usuarios},
                              context_instance = RequestContext(request))

def Login(request):
    mensaje = None
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username = usuario,password = clave)
            print(acceso)
            if acceso is not None:
                if acceso.is_active:
                    login(request,acceso)
                    empleado = Empleado.objects.get(usuario = usuario)
                    valorInicial = ConfiguracionPuntos.objects.get(bodega = empleado.punto.codigoBodega)

                    usuario = request.user
                    #empleado.cargo.nombreCargo == 'Cajero'
                    if usuario.is_staff:
                        return HttpResponseRedirect('/')
                    else:
                        valorInicial.jornada = request.POST['jornada']
                        valorInicial.save()
                        return HttpResponseRedirect('/ventas/ventaPunto')

                else:
                    mensaje = 'Tu usuario esta inactivo'
            else:
                mensaje = 'El usuario y la contrtasena no existen o son incorrectos'
    else:
        formulario = AuthenticationForm()
    return render_to_response('Login.html',{'formulario':formulario,'mensaje':mensaje},
                              context_instance = RequestContext(request))

def logOut(request):
    logout(request)
    return HttpResponseRedirect('/nomina/login')



