from django.conf.urls import patterns, url

from Nomina.views import *


urlpatterns = patterns('',

    url(r'^cargo/$',GestionCargos),
    url(r'^empleado/$',GestionEmpleados),

)
