from django.conf.urls import patterns, url

from Ventas.views import *


urlpatterns = patterns('',

    url(r'^pedido/(?P<idcliente>\d+)',GestionPedidos),
    url(r'^detallePedido/(?P<idpedido>\d+)',GestionDetallePedido),
    url(r'^pedidoPdf/(?P<idpedido>\d+)',ReportePedido),

)
