# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Grupo'
        db.create_table(u'Inventario_grupo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombreGrupo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('refrigerado', self.gf('django.db.models.fields.BooleanField')()),
            ('congelado', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'Inventario', ['Grupo'])

        # Adding model 'Bodega'
        db.create_table(u'Inventario_bodega', (
            ('codigoBodega', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombreBodega', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccionBodega', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telefonoBodega', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'Inventario', ['Bodega'])

        # Adding model 'Producto'
        db.create_table(u'Inventario_producto', (
            ('codigoProducto', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Grupo'])),
            ('porcentajeCalidad', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('nombreProducto', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('costoProducto', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('vrVentaProducto', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('utilidadProducto', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rentabilidadProducto', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('gravado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('excento', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('excluido', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Inventario', ['Producto'])

        # Adding model 'SubProducto'
        db.create_table(u'Inventario_subproducto', (
            ('codigoSubProducto', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombreSubProducto', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('costoSubProducto', self.gf('django.db.models.fields.IntegerField')()),
            ('vrVentaSubProducto', self.gf('django.db.models.fields.IntegerField')()),
            ('utilidadSubProducto', self.gf('django.db.models.fields.IntegerField')()),
            ('rentabilidadSubProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('gravado', self.gf('django.db.models.fields.BooleanField')()),
            ('excento', self.gf('django.db.models.fields.BooleanField')()),
            ('excluido', self.gf('django.db.models.fields.BooleanField')()),
            ('refrigerado', self.gf('django.db.models.fields.BooleanField')()),
            ('congelado', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'Inventario', ['SubProducto'])

        # Adding model 'DetalleSubProducto'
        db.create_table(u'Inventario_detallesubproducto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subproducto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.SubProducto'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoUnitProducto', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('unidades', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'Inventario', ['DetalleSubProducto'])

        # Adding model 'ProductoBodega'
        db.create_table(u'Inventario_productobodega', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('bodega', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
            ('pesoProductoStock', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pesoProductoKilos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('unidadesStock', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Inventario', ['ProductoBodega'])

        # Adding model 'SubProductoBodega'
        db.create_table(u'Inventario_subproductobodega', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subProducto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.SubProducto'])),
            ('bodega', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
            ('pesoSubProductoStock', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal(u'Inventario', ['SubProductoBodega'])

        # Adding model 'Traslado'
        db.create_table(u'Inventario_traslado', (
            ('codigoTraslado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bodegaActual', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
            ('bodegaDestino', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('empleado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('fechaTraslado', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('estadoTraslado', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('descripcionTraslado', self.gf('django.db.models.fields.TextField')(max_length=200)),
        ))
        db.send_create_signal(u'Inventario', ['Traslado'])

        # Adding model 'DetalleTraslado'
        db.create_table(u'Inventario_detalletraslado', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('traslado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Traslado'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'], null=True, blank=True)),
            ('SubProducto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.SubProducto'], null=True, blank=True)),
            ('pesoTraslado', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('unidadesTraslado', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('pesoEnvio', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoLlegada', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Inventario', ['DetalleTraslado'])

        # Adding model 'Proveedor'
        db.create_table(u'Inventario_proveedor', (
            ('codigoProveedor', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nit', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('nombreProv', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccionProv', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telefonoProv', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contacto', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('departamento', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'Inventario', ['Proveedor'])

        # Adding model 'Compra'
        db.create_table(u'Inventario_compra', (
            ('codigoCompra', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Grupo'])),
            ('encargado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('proveedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Proveedor'])),
            ('fechaCompra', self.gf('django.db.models.fields.DateField')(auto_now=True, null=True, blank=True)),
            ('vrCompra', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrTransporte', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Inventario', ['Compra'])

        # Adding model 'Ganado'
        db.create_table(u'Inventario_ganado', (
            ('codigoGanado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('piel', self.gf('django.db.models.fields.IntegerField')()),
            ('pesoEnPie', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('precioKiloEnPie', self.gf('django.db.models.fields.IntegerField')()),
            ('precioTotal', self.gf('django.db.models.fields.IntegerField')()),
            ('fechaIngreso', self.gf('django.db.models.fields.DateField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'Inventario', ['Ganado'])

        # Adding model 'DetalleCompra'
        db.create_table(u'Inventario_detallecompra', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Compra'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'], null=True, blank=True)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Ganado'], null=True, blank=True)),
            ('pesoProducto', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=15, decimal_places=3)),
            ('unidades', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('vrCompraProducto', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('subtotal', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('estado', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'Inventario', ['DetalleCompra'])

        # Adding model 'PlanillaRecepcion'
        db.create_table(u'Inventario_planillarecepcion', (
            ('codigoRecepcion', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Compra'])),
            ('empleado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('tipoGanado', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fechaRecepcion', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('cantCabezas', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('provedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Proveedor'])),
            ('transporte', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('difPieCanal', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Inventario', ['PlanillaRecepcion'])

        # Adding model 'Sacrificio'
        db.create_table(u'Inventario_sacrificio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recepcion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.PlanillaRecepcion'])),
            ('cantReses', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('piel', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrMenudo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrDeguello', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrTransporte', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cola', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('rinones', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('creadillas', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('recortes', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('ubre', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('desecho', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('fechaSacrificio', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'Inventario', ['Sacrificio'])


    def backwards(self, orm):
        # Deleting model 'Grupo'
        db.delete_table(u'Inventario_grupo')

        # Deleting model 'Bodega'
        db.delete_table(u'Inventario_bodega')

        # Deleting model 'Producto'
        db.delete_table(u'Inventario_producto')

        # Deleting model 'SubProducto'
        db.delete_table(u'Inventario_subproducto')

        # Deleting model 'DetalleSubProducto'
        db.delete_table(u'Inventario_detallesubproducto')

        # Deleting model 'ProductoBodega'
        db.delete_table(u'Inventario_productobodega')

        # Deleting model 'SubProductoBodega'
        db.delete_table(u'Inventario_subproductobodega')

        # Deleting model 'Traslado'
        db.delete_table(u'Inventario_traslado')

        # Deleting model 'DetalleTraslado'
        db.delete_table(u'Inventario_detalletraslado')

        # Deleting model 'Proveedor'
        db.delete_table(u'Inventario_proveedor')

        # Deleting model 'Compra'
        db.delete_table(u'Inventario_compra')

        # Deleting model 'Ganado'
        db.delete_table(u'Inventario_ganado')

        # Deleting model 'DetalleCompra'
        db.delete_table(u'Inventario_detallecompra')

        # Deleting model 'PlanillaRecepcion'
        db.delete_table(u'Inventario_planillarecepcion')

        # Deleting model 'Sacrificio'
        db.delete_table(u'Inventario_sacrificio')


    models = {
        u'Inventario.bodega': {
            'Meta': {'object_name': 'Bodega'},
            'codigoBodega': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'direccionBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nombreBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoBodega': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Inventario.compra': {
            'Meta': {'object_name': 'Compra'},
            'codigoCompra': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'encargado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaCompra': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'proveedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Proveedor']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'vrCompra': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrTransporte': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Inventario.detallecompra': {
            'Meta': {'object_name': 'DetalleCompra'},
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']"}),
            'estado': ('django.db.models.fields.BooleanField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Ganado']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '15', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True', 'blank': 'True'}),
            'subtotal': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'vrCompraProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'Inventario.detallesubproducto': {
            'Meta': {'object_name': 'DetalleSubProducto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoUnitProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'subproducto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.SubProducto']"}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        u'Inventario.detalletraslado': {
            'Meta': {'object_name': 'DetalleTraslado'},
            'SubProducto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.SubProducto']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoEnvio': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoLlegada': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTraslado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True', 'blank': 'True'}),
            'traslado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Traslado']"}),
            'unidadesTraslado': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        u'Inventario.ganado': {
            'Meta': {'object_name': 'Ganado'},
            'codigoGanado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'fechaIngreso': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'pesoEnPie': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'piel': ('django.db.models.fields.IntegerField', [], {}),
            'precioKiloEnPie': ('django.db.models.fields.IntegerField', [], {}),
            'precioTotal': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Inventario.grupo': {
            'Meta': {'object_name': 'Grupo'},
            'congelado': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreGrupo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'refrigerado': ('django.db.models.fields.BooleanField', [], {})
        },
        u'Inventario.planillarecepcion': {
            'Meta': {'object_name': 'PlanillaRecepcion'},
            'cantCabezas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoRecepcion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']"}),
            'difPieCanal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'fechaRecepcion': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'provedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Proveedor']"}),
            'tipoGanado': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'transporte': ('django.db.models.fields.CharField', [], {'max_length': '11'})
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
        u'Inventario.productobodega': {
            'Meta': {'object_name': 'ProductoBodega'},
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProductoKilos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoProductoStock': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'unidadesStock': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Inventario.proveedor': {
            'Meta': {'object_name': 'Proveedor'},
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'codigoProveedor': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'contacto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'departamento': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'direccionProv': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'nit': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'nombreProv': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoProv': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Inventario.sacrificio': {
            'Meta': {'object_name': 'Sacrificio'},
            'cantReses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cola': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'creadillas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'desecho': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaSacrificio': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'piel': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recepcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.PlanillaRecepcion']"}),
            'recortes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'rinones': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'ubre': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'vrDeguello': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrMenudo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrTransporte': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        u'Inventario.subproductobodega': {
            'Meta': {'object_name': 'SubProductoBodega'},
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoSubProductoStock': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'subProducto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.SubProducto']"})
        },
        u'Inventario.traslado': {
            'Meta': {'object_name': 'Traslado'},
            'bodegaActual': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'bodegaDestino': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'codigoTraslado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'descripcionTraslado': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'empleado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'estadoTraslado': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'fechaTraslado': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['Inventario']