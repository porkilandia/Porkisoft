from django.conf.urls import patterns, url
from Fabricacion.views import *

urlpatterns = patterns('',
    # Examples:

    url(r'^existencias/$',existencias),
    url(r'^guardaDescarne/$',GuardaDescarne),
    url(r'^traercosto/$',TraerCosto),
    url(r'^traercostopollo/$',TraerCostoPollo),
    url(r'^traercostoFilete/$',TraerCostoFilete),
    url(r'^costearTajado/$',costearTajado),
    url(r'^guardarTajado/$',GuardarTajado),
    url(r'^guardarCondimentado/$',GuardarCondimentado),
    url(r'^guardarEnsalinado/$',GuardaEnsalinado),

    url(r'^condimentado/$',GestionCondimentado),

    url(r'^canalPendiente/$',InformeCanalesPendientes),
    url(r'^descarne/$',GestionDescarneCabeza),
    url(r'^costos/$',GestionValorCostos),
    url(r'^editacosto/(?P<idcosto>\d+)',EditaCostos),
    url(r'^editaensalinado/(?P<idEnsalinado>\d+)',EditaEnsalinado),

    url(r'^canal/(?P<idrecepcion>\d+)',GestionCanal),
    url(r'^marcarcanal/(?P<idcanal>\d+)',MarcarCanalDesposte),

    url(r'^desposte/$',GestionDesposte),
    url(r'^sacrificio/(?P<idrecepcion>\d+)',GestionSacrificio),

    url(r'^detalleDesposte/(?P<idplanilla>\d+)',GestionDesposteActualizado),
    url(r'^costeoDesposte/$',costeoDesposte),
    url(r'^guardarDesposte/$',GuardarDesposte),
    url(r'^editaDesposte/(?P<idDetalle>\d+)',EditaDetPlanilla),

    #url(r'^detalleDesposte/(?P<idplanilla>\d+)',GestionCanalDetalleDesposte),
    #url(r'^costoDesposte/(?P<idplanilla>\d+)',CostoDesposte),

    url(r'^ensalinados/$', GestionEnsalinado),
    url(r'^tajado/$', GestionTajado),
    url(r'^detalleTajado/(?P<idTajado>\d+)', GestionDetalleTajado),
    url(r'^verduras/(?P<idDetcompra>\d+)', GestionVerduras),
    url(r'^condimento/$', GestionCondimento),
    url(r'^detallecondimento/(?P<idcondimento>\d+)', GestionDetalleCondimento),
    url(r'^costoCond/(?P<idcondimento>\d+)',CostoCondimento),
    url(r'^miga/$', GestionMiga),
    url(r'^detallemiga/(?P<idmiga>\d+)', GestionDetalleMiga),
    url(r'^costoMiga/(?P<idmiga>\d+)',CostoMiga),
    url(r'^apanados/$',GestionApanado),



)
