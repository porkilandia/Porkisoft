from django.conf.urls import patterns, url
from Ventas.views import *


urlpatterns = patterns('',

    url(r'^ventas/$',GestionVentas),
    url(r'^detalleVentas/(?P<idVenta>\d+)',GestionDetalleVentas),
    url(r'^consultaPrecioProducto/$',consultaValorProducto),
    url(r'^guardaVenta/$',GuardarVenta),
    url(r'^consultaCosto/$',consultaCostoProducto),
    url(r'^editaDetVenta/(?P<idDetVenta>\d+)',EditaDetalleVentas),

    url(r'^pedido/(?P<idcliente>\d+)',GestionPedidos),

    url(r'^detallePedido/(?P<idpedido>\d+)',GestionDetallePedido),
    url(r'^BorrardetallePedido/(?P<idpedido>\d+)',BorrarDetallePedido),
    url(r'^guardarPedido/$',GuaradarPedido),
    url(r'^verificarPrecioPedido/$',VerificarPrecioPedido),


    #url(r'^pedidoPdf/(?P<idpedido>\d+)',ReportePedido),
    url(r'^listaPrecios/$',GestionLista),
    url(r'^detalleLista/(?P<idLista>\d+)',GestionDetalleLista),
    url(r'^editaLista/(?P<idDetLista>\d+)',EditaListas),

    url(r'^ventaPunto/$',PuntoVenta),
    url(r'^detalleVentaPunto/(?P<idVenta>\d+)',DetallePuntoVenta),
    url(r'^editaVentaPunto/(?P<idDetVenta>\d+)',EditaPuntoVenta),
    url(r'^eliminaVentaPunto/(?P<idDetVenta>\d+)',EliminaPuntoVenta),
    url(r'^valorProdVenta/$',ValorProdVenta),
    url(r'^anulaVenta/$',AnulaVentas),

    url(r'^caja/$',GestionCaja),
    url(r'^editaCaja/(?P<idCaja>\d+)',EditaCaja),

    url(r'^cobrar/$',CobrarVenta),

    url(r'^retiro/$',GestionRetiros),
    url(r'^ImprimirRetiro/$',ImprimirRetiro),

    url(r'^devoluciones/$',GestionarDevolucion),
    url(r'^detalleDevoluciones/(?P<idDev>\d+)',GestionDetalleDevolucion),
    url(r'^GuardarDevolucion/$',GuardarDevolucion),

    url(r'^templateAZ/$',TemplateAZ),
    url(r'^reporteAZ/$',ReporteAZ),

    url(r'^templateReporteVentaNorte/$',TemplateReporteVentaNorte),
    url(r'^reporteVentaNorte/$',ReporteVentaNorte),

    url(r'^configPuntos/$',GestionConfigPuntos),
    url(r'^editaConfigPuntos/(?P<idConfig>\d+)',EditaConfigPuntos),

    url(r'^TemplateListaVentaNorte/$',TemplateRepListVentasNorte),
    url(r'^reporteListaVentaNorte/$',RepListVentasNorte),
)
