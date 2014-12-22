from django.conf.urls import patterns, url

from Nomina.views import *


urlpatterns = patterns('',

    url(r'^cargo/$',GestionCargos),
    url(r'^empleado/$',GestionEmpleados),
    url(r'^editaEmpleado/(?P<idEmpleado>\d+)',EditaEmpleados),
    url(r'^login/$',Login,name='login'),
    url(r'^usuarios/$',GestionUsuario),
    url(r'^logOut/$',logOut),

)
