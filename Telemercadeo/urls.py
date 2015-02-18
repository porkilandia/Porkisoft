from django.conf.urls import patterns, url

from Telemercadeo.views import *



urlpatterns = patterns('',

    url(r'^cliente/$',GestionCliente),
    url(r'^editacliente/(?P<idCliente>\d+)',EditaCliente),

)
