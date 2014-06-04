# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Venta'
        db.create_table(u'Ventas_venta', (
            ('numeroVenta', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaVenta', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('empleado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Telemercadeo.Cliente'])),
            ('bodega', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
            ('descuento', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('TotalVenta', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Ventas', ['Venta'])

        # Adding model 'DetalleVenta'
        db.create_table(u'Ventas_detalleventa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('venta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ventas.Venta'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'], null=True)),
            ('subproducto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.SubProducto'], null=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('unidades', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('vrUnitario', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrTotal', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Ventas', ['DetalleVenta'])

        # Adding model 'Pedido'
        db.create_table(u'Ventas_pedido', (
            ('numeroPedido', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaPedido', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('empleado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Telemercadeo.Cliente'])),
            ('bodega', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
            ('descuento', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('TotalVenta', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Ventas', ['Pedido'])

        # Adding model 'DetallePedido'
        db.create_table(u'Ventas_detallepedido', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pedido', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ventas.Pedido'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'], null=True)),
            ('subproducto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.SubProducto'], null=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('unidades', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('vrUnitario', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrTotal', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Ventas', ['DetallePedido'])


    def backwards(self, orm):
        # Deleting model 'Venta'
        db.delete_table(u'Ventas_venta')

        # Deleting model 'DetalleVenta'
        db.delete_table(u'Ventas_detalleventa')

        # Deleting model 'Pedido'
        db.delete_table(u'Ventas_pedido')

        # Deleting model 'DetallePedido'
        db.delete_table(u'Ventas_detallepedido')


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
            'Meta': {'object_name': 'Producto'},
            'codigoProducto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'excento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'excluido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gravado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'porcentajeCalidad': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'rentabilidadProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'utilidadProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrVentaProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'nombreCliente': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoCliente': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Ventas.detallepedido': {
            'Meta': {'object_name': 'DetallePedido'},
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True'}),
            'subproducto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.SubProducto']", 'null': 'True'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'venta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.Venta']"}),
            'vrTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrUnitario': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Ventas.pedido': {
            'Meta': {'object_name': 'Pedido'},
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Telemercadeo.Cliente']"}),
            'descuento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaPedido': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numeroPedido': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Ventas.venta': {
            'Meta': {'object_name': 'Venta'},
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Telemercadeo.Cliente']"}),
            'descuento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaVenta': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numeroVenta': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Ventas']