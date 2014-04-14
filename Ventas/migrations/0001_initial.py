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
            ('fechaVentav', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('TotalVenta', self.gf('django.db.models.fields.IntegerField')()),
            ('descuento', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('empleado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Telemercadeo.Cliente'])),
            ('bodega', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
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
        ))
        db.send_create_signal(u'Ventas', ['DetalleVenta'])


    def backwards(self, orm):
        # Deleting model 'Venta'
        db.delete_table(u'Ventas_venta')

        # Deleting model 'DetalleVenta'
        db.delete_table(u'Ventas_detalleventa')


    models = {
        u'Inventario.bodega': {
            'Meta': {'object_name': 'Bodega'},
            'codigoBodega': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'direccionBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nombreBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoBodega': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Inventario.producto': {
            'Meta': {'object_name': 'Producto'},
            'codigoProducto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'congelado': ('django.db.models.fields.BooleanField', [], {}),
            'costoProducto': ('django.db.models.fields.IntegerField', [], {}),
            'excento': ('django.db.models.fields.BooleanField', [], {}),
            'excluido': ('django.db.models.fields.BooleanField', [], {}),
            'gravado': ('django.db.models.fields.BooleanField', [], {}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'refrigerado': ('django.db.models.fields.BooleanField', [], {}),
            'rentabilidadProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'utilidadProducto': ('django.db.models.fields.IntegerField', [], {}),
            'vrCompraProducto': ('django.db.models.fields.IntegerField', [], {}),
            'vrVentaProducto': ('django.db.models.fields.IntegerField', [], {})
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
        u'Ventas.detalleventa': {
            'Meta': {'object_name': 'DetalleVenta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True'}),
            'subproducto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.SubProducto']", 'null': 'True'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'venta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ventas.Venta']"})
        },
        u'Ventas.venta': {
            'Meta': {'object_name': 'Venta'},
            'TotalVenta': ('django.db.models.fields.IntegerField', [], {}),
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Telemercadeo.Cliente']"}),
            'descuento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaVentav': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numeroVenta': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Ventas']