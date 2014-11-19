# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Caja'
        db.create_table(u'Ventas_caja', (
            ('numeroCaja', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaCaja', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('jornada', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('encargado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('base', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('TotalVenta', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('TotalEfectivo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('TotalResiduo', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Ventas', ['Caja'])

        # Adding model 'Retiros'
        db.create_table(u'Ventas_retiros', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaRetiro', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('encargado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('observacion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Ventas', ['Retiros'])

        # Adding model 'DetalleVentaPunto'
        db.create_table(u'Ventas_detalleventapunto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('venta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ventas.Venta'])),
            ('productoVenta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'], null=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('unidades', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('vrUnitario', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrTotal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('credito', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Ventas', ['DetalleVentaPunto'])

        # Adding model 'VentaPunto'
        db.create_table(u'Ventas_ventapunto', (
            ('numeroVenta', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaVenta', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('TotalVenta', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('restaurante', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('guardado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Ventas', ['VentaPunto'])


    def backwards(self, orm):
        # Deleting model 'Caja'
        db.delete_table(u'Ventas_caja')

        # Deleting model 'Retiros'
        db.delete_table(u'Ventas_retiros')

        # Deleting model 'DetalleVentaPunto'
        db.delete_table(u'Ventas_detalleventapunto')

        # Deleting model 'VentaPunto'
        db.delete_table(u'Ventas_ventapunto')


    models = {
        u'Inventario.bodega': {
            'Meta': {'object_name': 'Bodega'},
            'codigoBodega': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'direccionBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nombreBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoBodega': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Inventario.grupo': {
            'Meta': {'object_name': 'Grupo'},
            'congelado': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreGrupo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'refrigerado': ('django.db.models.fields.BooleanField', [], {})
        },
        u'Inventario.producto': {
            'Meta': {'ordering': "['nombreProducto']", 'object_name': 'Producto'},
            'codigoProducto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'excento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'excluido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gravado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'precioSugerido': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Inventario.subproducto': {
            'Meta': {'object_name': 'SubProducto'},
            'codigoSubProducto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'congelado': ('django.db.models.fields.BooleanField', [], {}),
            'costoSubProducto': ('django.db.models.fields.IntegerField', [], {}),
            'excento': ('django.db.models.fields.BooleanField', [], {}),
            'excluido': ('django.db.models.fields.BooleanField', [], {}),
            'gravado': ('django.db.models.fields.BooleanField', [], {}),
            'nombreSubProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'refrigerado': ('django.db.models.fields.BooleanField', [], {}),
            'rentabilidadSubProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'utilidadSubProducto': ('django.db.models.fields.IntegerField', [], {}),
            'vrVentaSubProducto': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Nomina.cargo': {
            'Meta': {'object_name': 'Cargo'},
            'codigoCargo': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreCargo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'Nomina.empleado': {
            'Meta': {'object_name': 'Empleado'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Cargo']"}),
            'codigoEmpleado': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Telemercadeo.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'codigoCliente': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'direccionCliente': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nit': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '15'}),
            'nombreCliente': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoCliente': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Ventas.caja': {
            'Meta': {'object_name': 'Caja'},
            'TotalEfectivo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'TotalResiduo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'base': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'encargado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaCaja': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'jornada': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'numeroCaja': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Ventas.detallelista': {
            'Meta': {'object_name': 'DetalleLista'},
            'costoKilo': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lista': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.ListaDePrecios']"}),
            'precioVenta': ('django.db.models.fields.IntegerField', [], {}),
            'productoLista': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Ventas.detallepedido': {
            'Meta': {'object_name': 'DetallePedido'},
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pedido': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.Pedido']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True'}),
            'subproducto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.SubProducto']", 'null': 'True'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'vrTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrUnitario': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Ventas.detalleventa': {
            'Meta': {'object_name': 'DetalleVenta'},
            'contado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'credito': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'productoVenta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'venta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.Venta']"}),
            'vrTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrUnitario': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Ventas.detalleventapunto': {
            'Meta': {'object_name': 'DetalleVentaPunto'},
            'contado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'credito': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'productoVenta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'venta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.Venta']"}),
            'vrTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrUnitario': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Ventas.listadeprecios': {
            'Meta': {'object_name': 'ListaDePrecios'},
            'codigoLista': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'nombreLista': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'Ventas.pedido': {
            'Meta': {'object_name': 'Pedido'},
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Telemercadeo.Cliente']"}),
            'descuento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaPedido': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numeroFactura': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'numeroPedido': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Ventas.retiros': {
            'Meta': {'object_name': 'Retiros'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'encargado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaRetiro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {})
        },
        u'Ventas.venta': {
            'Meta': {'object_name': 'Venta'},
            'TotalContado': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'TotalCredito': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'TotalRegistradora': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'descuadre': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'efectivo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaVenta': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jornada': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'lista': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.ListaDePrecios']", 'null': 'True', 'blank': 'True'}),
            'numeroVenta': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'residuo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'restaurante': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Ventas.ventapunto': {
            'Meta': {'object_name': 'VentaPunto'},
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaVenta': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numeroVenta': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'restaurante': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['Ventas']