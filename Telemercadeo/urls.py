from django.conf.urls import patterns, url

from Telemercadeo.views import *



urlpatterns = patterns('',

    url(r'^cliente/$',GestionCliente),

)
