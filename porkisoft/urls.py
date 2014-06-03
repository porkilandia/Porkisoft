from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from Inventario.views import home
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',home),
    url(r'^inventario/', include('Inventario.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
