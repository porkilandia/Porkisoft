from django.conf.urls import patterns, url

from Ventas.views import *


urlpatterns = patterns('',

    url(r'^ventas/$',GestionVentas),
    url(r'^detalleVentas/(?P<idVenta>\d+)',GestionDetalleVentas),
    url(r'^consultaPrecioProducto/$',consultaValorProducto),
    url(r'^guardaVenta/$',GuardarVenta),
    url(r'^consultaCosto/$',consultaCostoProducto),

    url(r'^pedido/(?P<idcliente>\d+)',GestionPedidos),
    url(r'^detallePedido/(?P<idpedido>\d+)',GestionDetallePedido),
    url(r'^pedidoPdf/(?P<idpedido>\d+)',ReportePedido),
    url(r'^listaPrecios/$',GestionLista),
    url(r'^detalleLista/(?P<idLista>\d+)',GestionDetalleLista),
    url(r'^editaLista/(?P<idDetLista>\d+)',EditaListas),

)
