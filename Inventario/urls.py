from django.conf.urls import patterns, url

from Inventario.views import *

urlpatterns = patterns('',

    url(r'^provedorAjax/$', listaProvedoresAjax),

    url(r'^listaProd/$', listaProductos),
    url(r'^verSubProductos/$',listaSubProductos),
    url(r'^bodega/$',GestionBodega),
    url(r'^provedor/$',GestionProvedor),
    url(r'^ganado/(?P<idcompra>\d+)',GestionGanado),
    url(r'^compra/$',GestionCompra),
    url(r'^grupo/$',GestionGrupo),

    url(r'^recepcion/(?P<idcompra>\d+)',GestionPlanillaRecepcion),

    url(r'^traslado/$',GestionTraslados),
    url(r'^dettraslado/(?P<idtraslado>\d+)',GestionDetalleTraslado),
    url(r'^reporteTraslado/(?P<idTraslado>\d+)',ReporteTraslado),

    url(r'^detcompra/(?P<idcompra>\d+)',GestionDetalleCompra),
    url(r'^productoBodega/(?P<idproducto>\d+)',GestionProductoBodega),
    url(r'^addDSprod/(?P<id_subproducto>\d+)',AgregarDetSubProducto, name='gestionSp'),
    url(r'^borrar/(?P<id_producto>\d+)',borrar_producto),
    url(r'^borrarSP/(?P<idSubproducto>\d+)',borrarSubproducto),
    url(r'^borrardetSP/(?P<idDetalle>\d+)',borrarDetalleSp),
    url(r'^borrarBodega/(?P<idbodega>\d+)',borrarBodega),
    url(r'^editar/(?P<id_producto>\d+)',editar_producto),
    url(r'^editarBodega/(?P<idBodega>\d+)',editarBodega),
    url(r'^editarSP/(?P<idSproducto>\d+)',editarSubproducto),


)
