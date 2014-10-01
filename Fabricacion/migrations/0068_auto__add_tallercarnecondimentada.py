# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TallerCarneCondimentada'
        db.create_table(u'Fabricacion_tallercarnecondimentada', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaCarCond', self.gf('django.db.models.fields.DateField')()),
            ('pesoProducto', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('condimento', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('punto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Bodega'])),
            ('productoCond', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoTotalCond', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('costoKiloCond', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('guardado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Fabricacion', ['TallerCarneCondimentada'])


    def backwards(self, orm):
        # Deleting model 'TallerCarneCondimentada'
        db.delete_table(u'Fabricacion_tallercarnecondimentada')


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
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.condimento': {
            'Meta': {'object_name': 'Condimento'},
            'cantFormulas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoCondimento': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoLitroCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'mod': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pesoCondimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
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
            'grupo': ('django.db.models.fields.CharField', [], {'default': "'Macho'", 'max_length': '20'}),
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
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.DetalleCompra']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
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
            'punto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Bodega']"})
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
        u'Fabricacion.valorescostos': {
            'Meta': {'object_name': 'ValoresCostos'},
            'codigoCosto': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nombreCosto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'valorCif': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valorKiloPie': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valorMod': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'codigoCompra': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'encargado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"}),
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
        u'Inventario.ganado': {
            'Meta': {'object_name': 'Ganado'},
            'codigoGanado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Compra']", 'null': 'True', 'blank': 'True'}),
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
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Grupo']"}),
            'nombreProducto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['Fabricacion']