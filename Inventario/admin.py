from django.contrib import admin

from Inventario.models import *

admin.site.register(Bodega)
admin.site.register(Producto)
admin.site.register(SubProducto)
admin.site.register(DetalleSubProducto)
admin.site.register(ProductoBodega)
admin.site.register(SubProductoBodega)
admin.site.register(Traslado)
admin.site.register(DetalleTraslado)
admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(Ganado)
admin.site.register(DetalleCompra)
