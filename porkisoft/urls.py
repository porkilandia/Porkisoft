from django.conf.urls import patterns, include, url

from django.contrib import admin
from Inventario.views import home
from  Ventas.views import PuntoVenta
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',home),
    url(r'^VentasNorte/',PuntoVenta),

    url(r'^inventario/', include('Inventario.urls')),
    url(r'^telemercadeo/', include('Telemercadeo.urls')),
    url(r'^nomina/', include('Nomina.urls')),
    url(r'^ventas/', include('Ventas.urls')),
    url(r'^fabricacion/', include('Fabricacion.urls')),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
