from datetime import *

from django import forms
from django.forms import ModelForm
from django.db.models import F

from Ventas.models import *

class PedidoForm(ModelForm):

    def __init__(self,idBodega,*args,**kwargs):
        super(PedidoForm,self).__init__(*args,**kwargs)
        if idBodega != 0:
            self.fields['listaPrecioPedido'].queryset = ListaDePrecios.objects.select_related().filter(bodega = idBodega)
        else:
            self.fields['listaPrecioPedido'].queryset = ListaDePrecios.objects.select_related().all()

    class Meta:
        model = Pedido
        exclude = ('TotalVenta','descuento','NombreCliente','nitCliente','guardado',)

class DetallePedidoForm(ModelForm):
    '''def __init__(self, *args, **kwargs):
        super(DetallePedidoForm,self).__init__(*args, **kwargs)

        #SE LIMITA EL NUMERO DE REGISTROS QUE SE RENDERIZAN PARA AUMENTAR LA VELOCIDAD DE CARGA
        Hoy = date.today()
        consulta = Pedido.objects.filter(fechaPedido = Hoy)
        self.fields['pedido'].queryset = consulta

        q1 = Producto.objects.select_related().filter(grupo__nombreGrupo = "Reses")
        q2 = Producto.objects.select_related().filter(grupo__nombreGrupo = "Cerdos")
        q3 = Producto.objects.select_related().filter(grupo__nombreGrupo = "Cerdas")
        q4 = Producto.objects.select_related().filter(grupo__nombreGrupo = "Pollos")
        q5 = Producto.objects.select_related().filter(grupo__nombreGrupo = "Compra/Venta")

        self.fields['productoPedido'].queryset = q1|q2|q3|q4|q5'''
    class Meta:
        model = DetallePedido
        exclude = ('subproducto','estado','unidadesPedido',)

class VentaForm(ModelForm):
    class Meta:
        model = Venta
        exclude = ('TotalVenta',"TotalCredito","TotalContado","descuadre","residuo","guardado",)

class VentaDetalleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VentaDetalleForm,self).__init__(*args, **kwargs)
        q1 = Producto.objects.filter(grupo__nombreGrupo = 'Reses')
        q2 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdos')
        q3 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdas')
        q4 = Producto.objects.filter(grupo__nombreGrupo = 'Compra/Venta')
        q5 = Producto.objects.filter(grupo__nombreGrupo = 'Pollos')

        self.fields['productoVenta'].queryset = q1 | q2 | q3 | q4 | q5

    class Meta:
        model = DetalleVenta

class ListaDePreciosForm(ModelForm):
    class Meta:
        model = ListaDePrecios


class DetalleListaForm(ModelForm):
    class Meta:
        model = DetalleLista


class VentaPuntoForm(ModelForm):
    class Meta:
        model = VentaPunto
        exclude = ("TotalVenta","guardado","factura","anulado","cliente","restaurante",)


class DetalleVentaPuntoForm(ModelForm):
    def __init__(self,idVenta, *args, **kwargs):
        super(DetalleVentaPuntoForm,self).__init__(*args, **kwargs)

        #SE LIMITA EL NUMERO DE REGISTROS QUE SE RENDERIZAN PARA AUMENTAR LA VELOCIDAD DE CARGA
        Hoy = date.today()
        venta = VentaPunto.objects.get(pk = idVenta)
        consulta = VentaPunto.objects.filter(jornada = venta.jornada,puntoVenta = venta.puntoVenta.codigoBodega,
                                             encargado = venta.encargado.codigoEmpleado,fechaVenta = Hoy)
        self.fields['venta'].queryset = consulta


        '''q1 = Producto.objects.filter(grupo__nombreGrupo = 'Reses').filter(numeroProducto__gt = 0).order_by('numeroProducto')
        q2 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdos').filter(numeroProducto__gt = 0).order_by('numeroProducto')
        #q3 = Producto.objects.filter(grupo__nombreGrupo = 'Cerdas').filter(numeroProducto__gt = 0).order_by('numeroProducto')
        q4 = Producto.objects.filter(grupo__nombreGrupo = 'Compra/Venta').filter(numeroProducto__gt = 0).order_by('numeroProducto')
        q5 = Producto.objects.filter(grupo__nombreGrupo = 'Pollos').filter(numeroProducto__gt = 0).order_by('numeroProducto')

        q6 = Producto.objects.filter(nombreProducto = 'Pierna de Cerda').order_by('numeroProducto')
        q7 = Producto.objects.filter(nombreProducto = 'Lomo Canon Cerda').order_by('numeroProducto')
        q8 = Producto.objects.filter(nombreProducto = 'Picadillo').order_by('numeroProducto')
        self.fields['productoVenta'].queryset = q1 | q2 | q4 | q5 | q6 | q7 | q8'''

    class Meta:
        model = DetalleVentaPunto
        exclude = ('unidades','productoVenta',)
class CajaForm(ModelForm):
    class Meta:
        model = Caja
        exclude = ("TotalVenta","TotalResiduo","TotalCaja","TotalRetiro","TotalRestaurante",)

class RetirosForm(ModelForm):
    class Meta:
        model = Retiros
        exclude = ("guardado","nombreEncargado",)

class DevolucionesForm(ModelForm):
    class Meta:
        model = Devolucion
        exclude = ("guardado",)
class DetalleDevolucionForm(ModelForm):
    class Meta:
        model = DetalleDevolucion

class ConfigPuntosForm(ModelForm):
    class Meta :
        model = ConfiguracionPuntos
