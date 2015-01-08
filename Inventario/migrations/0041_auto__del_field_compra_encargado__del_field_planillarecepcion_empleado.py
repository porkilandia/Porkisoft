# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Compra.encargado'
        db.delete_column(u'Inventario_compra', 'encargado_id')

        # Deleting field 'PlanillaRecepcion.empleado'
        db.delete_column(u'Inventario_planillarecepcion', 'empleado_id')

        # Deleting field 'Traslado.empleado'
        db.delete_column(u'Inventario_traslado', 'empleado_id')


    def backwards(self, orm):
        # Adding field 'Compra.encargado'
        db.add_column(u'Inventario_compra', 'encargado',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['Nomina.Empleado']),
                      keep_default=False)

        # Adding field 'PlanillaRecepcion.empleado'
        db.add_column(u'Inventario_planillarecepcion', 'empleado',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['Nomina.Empleado']),
                      keep_default=False)

        # Adding field 'Traslado.empleado'
        db.add_column(u'Inventario_traslado', 'empleado',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['Nomina.Empleado']),
                      keep_default=False)


    models = {
        u'Inventario.ajustes': {
            'Meta': {'object_name': 'Ajustes'},
            'bodegaAjuste': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'cantidadActual': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaAjuste': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'max_length': '150'}),
            'pesoAjuste': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoAjuste': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'restar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sumar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unidadActual': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        u'Inventario.bodega': {
            'Meta': {'object_name': 'Bodega'},
            'codigoBodega': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'direccionBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nombreBodega': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoBodega': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Inventario.compra': {
            'Meta': {'object_name': 'Compra'},
            'bodegaCompra': ('django.db.models.fields.related.ForeignKey', [], {'default': '5', 'to': u"orm['Inventario.Bodega']", 'blank': 'True'}),
            'cantCabezas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoCompra': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'fechaCompra': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'pesoDescongelado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '15', 'decimal_places': '3'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '15', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True', 'blank': 'True'}),
            'subtotal': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'vrCompraProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'vrKiloDescongelado': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'Inventario.detallefaltantes': {
            'Meta': {'object_name': 'DetalleFaltantes'},
            'diferencia': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'faltante': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Faltantes']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoActual': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoFisico': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoFaltante': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'unidadActual': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'unidadFisica': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
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
            'pesoEnvio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoLlegada': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTraslado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'productoTraslado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']", 'null': 'True', 'blank': 'True'}),
            'traslado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Traslado']"}),
            'unidadesTraslado': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        u'Inventario.faltantes': {
            'Meta': {'object_name': 'Faltantes'},
            'bodegaFaltante': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'fechaFaltante': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Inventario.ganado': {
            'Meta': {'object_name': 'Ganado'},
            'TotalpesoEnPie': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'codigoGanado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']", 'null': 'True', 'blank': 'True'}),
            'fechaIngreso': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'pesoEnPie': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
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
        u'Inventario.movimientos': {
            'Hasta': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'Meta': {'object_name': 'Movimientos'},
            'desde': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'entrada': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaMov': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreProd': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'productoMov': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'salida': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'Inventario.planillarecepcion': {
            'Meta': {'object_name': 'PlanillaRecepcion'},
            'cantCabezas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoRecepcion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']"}),
            'difPieCanal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaRecepcion': ('django.db.models.fields.DateField', [], {}),
            'pesoCanales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'provedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Proveedor']"}),
            'tipoGanado': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'transporte': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'vrKiloCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrTransporte': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Inventario.producto': {
            'Meta': {'ordering': "['nombreProducto']", 'object_name': 'Producto'},
            'codigoProducto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'excento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'excluido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gravado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gravado2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeroProducto': ('django.db.models.fields.BigIntegerField', [], {}),
            'precioSugerido': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Inventario.productobodega': {
            'Meta': {'object_name': 'ProductoBodega'},
            'bodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pesoProductoKilos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoProductoStock': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '2'}),
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
            'Meta': {'ordering': "['-fechaTraslado']", 'object_name': 'Traslado'},
            'bodegaActual': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'bodegaDestino': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'codigoTraslado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'descripcionTraslado': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'estadoTraslado': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'fechaTraslado': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['Inventario']