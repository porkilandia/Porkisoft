from django.contrib import admin

from inventario.models import *


admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(SubProducto)
admin.site.register(DetalleSubProducto)
admin.site.register(ProductoBodega)
admin.site.register(SubProductoBodega)

