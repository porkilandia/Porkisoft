from django.conf.urls import patterns, url

from Inventario.views import *


urlpatterns = patterns('',
    # Examples:
    url(r'^home/$',home),
    url(r'^listaProd/$', listaProductos),
    url(r'^verSubProductos/$',listaSubProductos),
    url(r'^bodega/$',GestionBodega),


    url(r'^addDSprod/(?P<id_subproducto>\d+)',AgregarDetSubProducto, name='gestionSp'),
    url(r'^borrar/(?P<id_producto>\d+)',borrar_producto),
    url(r'^borrarSP/(?P<idSubproducto>\d+)',borrarSubproducto),
    url(r'^borrardetSP/(?P<idDetalle>\d+)',borrarDetalleSp),
    url(r'^borrarBodega/(?P<idbodega>\d+)',borrarBodega),
    url(r'^editar/(?P<id_producto>\d+)',editar_producto),
    url(r'^editarBodega/(?P<idBodega>\d+)',editarBodega),
    url(r'^editarSP/(?P<idSproducto>\d+)',editarSubproducto),


)
