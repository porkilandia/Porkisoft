from django.conf.urls import patterns, url
from Fabricacion.views import *

urlpatterns = patterns('',
    # Examples:

    url(r'^costeoDesposte/$',costeoDesposte),


    url(r'^canal/(?P<idrecepcion>\d+)',GestionCanal),
    url(r'^marcarcanal/(?P<idcanal>\d+)',MarcarCanalDesposte),

    url(r'^desposte/$',GestionDesposte),
    url(r'^sacrificio/(?P<idrecepcion>\d+)',GestionSacrificio),

    url(r'^detalleDesposte/(?P<idplanilla>\d+)',GestionDesposteActualizado),
    #url(r'^detalleDesposte/(?P<idplanilla>\d+)',GestionCanalDetalleDesposte),
    url(r'^costoDesposte/(?P<idplanilla>\d+)',CostoDesposte),

    url(r'^ensalinados/(?P<idproducto>\d+)', GestionEnsalinado),
    url(r'^verduras/(?P<idDetcompra>\d+)', GestionVerduras),
    url(r'^condimento/$', GestionCondimento),
    url(r'^detallecondimento/(?P<idcondimento>\d+)', GestionDetalleCondimento),
    url(r'^costoCond/(?P<idcondimento>\d+)',CostoCondimento),
    url(r'^condtaj/(?P<idprodbod>\d+)',GestionCondTajado),
    url(r'^miga/$', GestionMiga),
    url(r'^detallemiga/(?P<idmiga>\d+)', GestionDetalleMiga),
    url(r'^costoMiga/(?P<idmiga>\d+)',CostoMiga),
    url(r'^apanado/(?P<idprodbod>\d+)',GestionApanado),

    url(r'^pechugas/(?P<idprodbod>\d+)',GestionarTajadoCondPechugas),

)
