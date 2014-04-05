from django.conf.urls import patterns, url

from inventario.views import *


urlpatterns = patterns('',
    # Examples:
    #url(r'^',index ),
    url(r'^listaProd/$', listaProductos),
    url(r'^verSubProductos/$',listaSubProductos),
    url(r'^addprod/',agregar_producto),
    url(r'^addSprod/',AgregarSubProducto),
    url(r'^addDSprod/',AgregarDetSubProducto),
    url(r'^borrar/(?P<id_producto>\d+)',borrar_producto),
    url(r'^editar/(?P<id_producto>\d+)',editar_producto),
    url(r'^prueba/(?P<id_subproducto>\d+)',prueba),

)
