# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Condimento.guardado'
        db.add_column(u'Fabricacion_condimento', 'guardado',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Condimento.guardado'
        db.delete_column(u'Fabricacion_condimento', 'guardado')


    models = {
        u'Fabricacion.auxiliarpromedios': {
            'Meta': {'object_name': 'auxiliarPromedios'},
            'costo': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'Fabricacion.canal': {
            'Meta': {'object_name': 'Canal'},
            'codigoCanal': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'difPesos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genero': ('django.db.models.fields.CharField', [], {'default': "'Macho'", 'max_length': '7'}),
            'nroCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoFrigovito': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoPorkilandia': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'planilla': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.PlanillaDesposte']", 'null': 'True', 'blank': 'True'}),
            'recepcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.PlanillaRecepcion']"}),
            'vrArrobaCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.condimentado': {
            'Meta': {'object_name': 'Condimentado'},
            'ablandaCarnes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigo': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'condimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'costoCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoFilete': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoFileteCond': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoACondimentar': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoFileteCond': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'resPollo': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'saborLonganiza': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.condimento': {
            'Meta': {'object_name': 'Condimento'},
            'cantFormulas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoCondimento': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoLitroCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoCondimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.conversiones': {
            'Meta': {'object_name': 'Conversiones'},
            'costoP1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoP2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaConversion': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoConversion': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoDos': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'productoUno': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'puntoConversion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.descarnecabeza': {
            'Meta': {'object_name': 'DescarneCabeza'},
            'cantRecosrtes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'caretas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lenguas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoCabezas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'procesos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'recortes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'vrKiloCareta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloLengua': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloProceso': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloRecorte': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.detallecondimento': {
            'Meta': {'object_name': 'DetalleCondimento'},
            'condimento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Condimento']"}),
            'costoProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoTotalProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'productoCondimento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.detalleenlagunado': {
            'Meta': {'object_name': 'DetalleEnlagunado'},
            'costoProducto': ('django.db.models.fields.IntegerField', [], {}),
            'enlagunado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Enlagunado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoPorducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.detallemiga': {
            'Meta': {'object_name': 'DetalleMiga'},
            'PesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'costoProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoTotalProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miga': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Miga']"}),
            'productoMiga': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.detalleplanilla': {
            'Meta': {'object_name': 'DetallePlanilla'},
            'PesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'costoAdtvo': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'costoProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'grupo': ('django.db.models.fields.CharField', [], {'default': "'Grupo Carnes'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoCarne': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'pesoCostilla': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'pesoDesecho': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'pesoHueso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'pesoSubProd': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'planilla': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.PlanillaDesposte']"}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCarnes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCarnes2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCarnes3': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCarnes4': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCostilla': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloDesecho': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloHuesos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloSubProd': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.detalletajado': {
            'Meta': {'object_name': 'DetalleTajado'},
            'costoKilo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'tajado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Tajado']"}),
            'unidades': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.empacadoapanados': {
            'Meta': {'object_name': 'EmpacadoApanados'},
            'cantBandejas': ('django.db.models.fields.IntegerField', [], {}),
            'costoKiloChuleta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costobandeja': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaEmpacado': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoBandeja': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoChuelta': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'produccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.ProcesoApanado']", 'null': 'True', 'blank': 'True'}),
            'productoAEmpacar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'stikers': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Fabricacion.enlagunado': {
            'Meta': {'object_name': 'Enlagunado'},
            'codigoEnlagunado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoEnlagunado': ('django.db.models.fields.IntegerField', [], {}),
            'fechaEnlagunado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pesoAntesLaguna': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.ensalinado': {
            'Meta': {'object_name': 'Ensalinado'},
            'codigoEnsalinado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoKilo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fechaEnsalinado': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoPapaina': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoAntes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoDespues': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoSal': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'productoEnsalinado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.limpiezaverduras': {
            'Meta': {'object_name': 'LimpiezaVerduras'},
            'cif': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']"}),
            'fechaLimpieza': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 7, 7, 0, 0)'}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoDespues': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoLimpiar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'valorProducto': ('django.db.models.fields.IntegerField', [], {}),
            'valorTransporte': ('django.db.models.fields.IntegerField', [], {}),
            'vrKilo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.menudos': {
            'Meta': {'object_name': 'Menudos'},
            'cantMenudos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoEscaldado': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKiloPicadillo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoMenudo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaMenudo': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoPicadillo': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.miga': {
            'Meta': {'object_name': 'Miga'},
            'PesoFormulaMiga': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'cantidadFormulas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoMiga': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoFormulaMiga': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKiloMigaProcesada': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaFabricacion': ('django.db.models.fields.DateField', [], {}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.molida': {
            'Meta': {'object_name': 'Molida'},
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKilo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKiloMolido': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaMolido': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoAmoler': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoMolido': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'totalMolido': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.planilladesposte': {
            'Meta': {'object_name': 'PlanillaDesposte'},
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoPlanilla': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'difCanalADespostado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '3'}),
            'fechaDesposte': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resesADespostar': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tipoDesposte': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'totalCanal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '3'}),
            'totalDespostado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '13', 'decimal_places': '3'})
        },
        u'Fabricacion.procesoapanado': {
            'Meta': {'object_name': 'ProcesoApanado'},
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKiloApanado': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaApanado': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'huevos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miga': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoFilete': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoApanado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'totalApanado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.sacrificio': {
            'Meta': {'object_name': 'Sacrificio'},
            'cantReses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cola': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'creadillas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'desecho': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaSacrificio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
        u'Fabricacion.tajado': {
            'Meta': {'object_name': 'Tajado'},
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoTajado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoKiloFilete': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'desposteHistorico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.PlanillaDesposte']", 'null': 'True', 'blank': 'True'}),
            'fechaTajado': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'polloHistorico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']", 'null': 'True', 'blank': 'True'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'responsable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
            'totalTajado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.tallerbolaensalinada': {
            'Meta': {'object_name': 'TallerBolaEnsalinada'},
            'costoKiloEns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaBolaCondimentada': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'papaina': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoBola': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoDespues': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTotal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'puntoBodega': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'sal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.tallercarnecondimentada': {
            'Meta': {'object_name': 'TallerCarneCondimentada'},
            'condimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'costoKiloCond': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaCarCond': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTotalCond': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoCond': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'puntoCond': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"})
        },
        u'Fabricacion.tallerchicharron': {
            'Meta': {'object_name': 'TallerChicharron'},
            'Sal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'Tocino': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'chicharron': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoUndChicharron': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoUndGrasa': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaChicharron': ('django.db.models.fields.DateField', [], {}),
            'grasa': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'productoCh': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'undChicharron': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'undGrasa': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.tallercroquetas': {
            'Meta': {'object_name': 'TallerCroquetas'},
            'condimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'costoKiloCroqueta': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'croqueta': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaCroqueta': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miga': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTotalCroqueta': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'puntoCroq': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"})
        },
        u'Fabricacion.tallerfrito': {
            'Meta': {'object_name': 'TallerFrito'},
            'condimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'costoKiloFrito': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaFrito': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTotalFrito': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'productoFrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'punto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"})
        },
        u'Fabricacion.tallerlenguas': {
            'Meta': {'object_name': 'TallerLenguas'},
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKiloPicadillo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaLenguas': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoAntes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoDespues': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.tallerreapanado': {
            'Meta': {'object_name': 'TallerReapanado'},
            'chuelta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'fechaReApanado': ('django.db.models.fields.DateField', [], {}),
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miga': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoChuleta': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoTotalReApanado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'puntoReApanado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"})
        },
        u'Fabricacion.valorescostos': {
            'Meta': {'object_name': 'ValoresCostos'},
            'codigoCosto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nombreCosto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'valorCif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valorKiloPie': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valorMod': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Inventario.bodega': {
            'Meta': {'object_name': 'Bodega'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'guardado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'proveedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Proveedor']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'vrCompra': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrTransporte': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'fechaRecepcion': ('django.db.models.fields.DateField', [], {}),
            'pesoCanales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'provedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Proveedor']"}),
            'tipoGanado': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'transporte': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'vrKiloCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrTransporte': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Inventario.producto': {
            'Meta': {'ordering': "['numeroProducto']", 'object_name': 'Producto'},
            'codigoProducto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoProducto': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'excento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'excluido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gravado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gravado2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'noPesables': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeroProducto': ('django.db.models.fields.BigIntegerField', [], {}),
            'pesables': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'precioSugerido': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'punto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'usuario': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['Fabricacion']