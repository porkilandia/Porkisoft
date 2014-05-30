# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ensalinado'
        db.create_table(u'Fabricacion_ensalinado', (
            ('codigoEnsalinado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaEnsalinado', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoSal', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoPapaina', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoProductoAntes', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('pesoProductoDespues', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('costoKilo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('costoTotal', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['Ensalinado'])

        # Adding model 'LimpiezaVerduras'
        db.create_table(u'Fabricacion_limpiezaverduras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.DetalleCompra'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('cif', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('mod', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('pesoProducto', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('vrKilo', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['LimpiezaVerduras'])

        # Adding model 'Enlagunado'
        db.create_table(u'Fabricacion_enlagunado', (
            ('codigoEnlagunado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoAntesLaguna', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('fechaEnlagunado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('costoEnlagunado', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Fabricacion', ['Enlagunado'])

        # Adding model 'DetalleEnlagunado'
        db.create_table(u'Fabricacion_detalleenlagunado', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enlagunado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Enlagunado'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoPorducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('costoProducto', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Fabricacion', ['DetalleEnlagunado'])

        # Adding model 'CondimentadoTajado'
        db.create_table(u'Fabricacion_condimentadotajado', (
            ('codigoTajado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoProductoEnsalinado', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('condimento', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('filete', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('recortes', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('procesos', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['CondimentadoTajado'])

        # Adding model 'PlanillaDesposte'
        db.create_table(u'Fabricacion_planilladesposte', (
            ('codigoPlanilla', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaDesposte', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('resesADespostar', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('totalDespostado', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('totalCanal', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=3)),
            ('difCanalADespostado', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=3)),
            ('costoProduccionTotal', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['PlanillaDesposte'])

        # Adding model 'Canal'
        db.create_table(u'Fabricacion_canal', (
            ('recepcion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.PlanillaRecepcion'])),
            ('codigoCanal', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('planilla', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.PlanillaDesposte'], null=True, blank=True)),
            ('pesoFrigovito', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('pesoPorkilandia', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3)),
            ('difPesos', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('vrKiloCanal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vrArrobaCanal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('genero', self.gf('django.db.models.fields.CharField')(default='Macho', max_length=7)),
            ('estado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Fabricacion', ['Canal'])

        # Adding model 'DetallePlanilla'
        db.create_table(u'Fabricacion_detalleplanilla', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('planilla', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.PlanillaDesposte'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('PesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['DetallePlanilla'])

        # Adding model 'Miga'
        db.create_table(u'Fabricacion_miga', (
            ('codigoMiga', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cantidadFormulas', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('fechaFabricacion', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('PesoFormulaMiga', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('costoFormulaMiga', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('costoKiloMigaProcesada', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['Miga'])

        # Adding model 'DetalleMiga'
        db.create_table(u'Fabricacion_detallemiga', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('miga', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Miga'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('PesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('costoProducto', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('costoTotalProducto', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['DetalleMiga'])

        # Adding model 'Apanado'
        db.create_table(u'Fabricacion_apanado', (
            ('codigoApanado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('huevos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('miga', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('pesoFilete', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('totalApanado', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('costoKiloApanado', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['Apanado'])

        # Adding model 'Condimento'
        db.create_table(u'Fabricacion_condimento', (
            ('codigoCondimento', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('cantFormulas', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pesoCondimento', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('costoCondimento', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('costoLitroCondimento', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['Condimento'])

        # Adding model 'DetalleCondimento'
        db.create_table(u'Fabricacion_detallecondimento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condimento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Condimento'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('costoProducto', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('costoTotalProducto', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Fabricacion', ['DetalleCondimento'])

        # Adding model 'CondimentadoTajadoPechuga'
        db.create_table(u'Fabricacion_condimentadotajadopechuga', (
            ('codigo', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('compra', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('PesoDescongelado', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('fileteACond', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('condimento', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('fileteAApanar', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('condimentoAP', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('huesos', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('piel', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('procesos', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['CondimentadoTajadoPechuga'])


    def backwards(self, orm):
        # Deleting model 'Ensalinado'
        db.delete_table(u'Fabricacion_ensalinado')

        # Deleting model 'LimpiezaVerduras'
        db.delete_table(u'Fabricacion_limpiezaverduras')

        # Deleting model 'Enlagunado'
        db.delete_table(u'Fabricacion_enlagunado')

        # Deleting model 'DetalleEnlagunado'
        db.delete_table(u'Fabricacion_detalleenlagunado')

        # Deleting model 'CondimentadoTajado'
        db.delete_table(u'Fabricacion_condimentadotajado')

        # Deleting model 'PlanillaDesposte'
        db.delete_table(u'Fabricacion_planilladesposte')

        # Deleting model 'Canal'
        db.delete_table(u'Fabricacion_canal')

        # Deleting model 'DetallePlanilla'
        db.delete_table(u'Fabricacion_detalleplanilla')

        # Deleting model 'Miga'
        db.delete_table(u'Fabricacion_miga')

        # Deleting model 'DetalleMiga'
        db.delete_table(u'Fabricacion_detallemiga')

        # Deleting model 'Apanado'
        db.delete_table(u'Fabricacion_apanado')

        # Deleting model 'Condimento'
        db.delete_table(u'Fabricacion_condimento')

        # Deleting model 'DetalleCondimento'
        db.delete_table(u'Fabricacion_detallecondimento')

        # Deleting model 'CondimentadoTajadoPechuga'
        db.delete_table(u'Fabricacion_condimentadotajadopechuga')


    models = {
        u'Fabricacion.apanado': {
            'Meta': {'object_name': 'Apanado'},
            'codigoApanado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoKiloApanado': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'huevos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'miga': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoFilete': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'totalApanado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.canal': {
            'Meta': {'object_name': 'Canal'},
            'codigoCanal': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'difPesos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genero': ('django.db.models.fields.CharField', [], {'default': "'Macho'", 'max_length': '7'}),
            'pesoFrigovito': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoPorkilandia': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'planilla': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.PlanillaDesposte']", 'null': 'True', 'blank': 'True'}),
            'recepcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.PlanillaRecepcion']"}),
            'vrArrobaCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vrKiloCanal': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'Fabricacion.condimentadotajado': {
            'Meta': {'object_name': 'CondimentadoTajado'},
            'codigoTajado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'condimento': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'filete': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoEnsalinado': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'procesos': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'recortes': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.condimentadotajadopechuga': {
            'Meta': {'object_name': 'CondimentadoTajadoPechuga'},
            'PesoDescongelado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'codigo': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'compra': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'condimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'condimentoAP': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fileteAApanar': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fileteACond': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'huesos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'piel': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'procesos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.condimento': {
            'Meta': {'object_name': 'Condimento'},
            'cantFormulas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'codigoCondimento': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoLitroCondimento': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pesoCondimento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
        },
        u'Fabricacion.detallecondimento': {
            'Meta': {'object_name': 'DetalleCondimento'},
            'condimento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Condimento']"}),
            'costoProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoTotalProducto': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
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
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.detalleplanilla': {
            'Meta': {'object_name': 'DetallePlanilla'},
            'PesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'planilla': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.PlanillaDesposte']"}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
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
            'fechaEnsalinado': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pesoPapaina': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoAntes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoDespues': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'pesoSal': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
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
        u'Fabricacion.miga': {
            'Meta': {'object_name': 'Miga'},
            'PesoFormulaMiga': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'cantidadFormulas': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'codigoMiga': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoFormulaMiga': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'costoKiloMigaProcesada': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaFabricacion': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'Fabricacion.planilladesposte': {
            'Meta': {'object_name': 'PlanillaDesposte'},
            'codigoPlanilla': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoProduccionTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'difCanalADespostado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '3'}),
            'fechaDesposte': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'resesADespostar': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'totalCanal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '3'}),
            'totalDespostado': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'})
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