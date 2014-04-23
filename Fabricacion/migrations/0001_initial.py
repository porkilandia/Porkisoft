# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
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

        # Adding model 'LimpezaTajado'
        db.create_table(u'Fabricacion_limpezatajado', (
            ('codigoTajado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoProductoAntes', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoProductoDespues', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('recortes', self.gf('django.db.models.fields.IntegerField')()),
            ('pesoGrasa', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoProcesos', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['LimpezaTajado'])

        # Adding model 'PlanillaDesposte'
        db.create_table(u'Fabricacion_planilladesposte', (
            ('codigoPlanilla', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaDesposte', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('resesADespostar', self.gf('django.db.models.fields.IntegerField')()),
            ('totalDespostado', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('difCanalADespostado', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['PlanillaDesposte'])

        # Adding model 'Canal'
        db.create_table(u'Fabricacion_canal', (
            ('codigoCanal', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('planilla', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.PlanillaDesposte'], null=True, blank=True)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Ganado'])),
            ('pesoPiernas', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoBrazos', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('peosTotalCanal', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['Canal'])

        # Adding model 'DetallePlanilla'
        db.create_table(u'Fabricacion_detalleplanilla', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('planilla', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.PlanillaDesposte'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('CantPiezas', self.gf('django.db.models.fields.IntegerField')()),
            ('PesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['DetallePlanilla'])

        # Adding model 'Formula'
        db.create_table(u'Fabricacion_formula', (
            ('codigoFormula', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('responsable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Empleado'])),
            ('pesoFormula', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('cantidadFormulas', self.gf('django.db.models.fields.IntegerField')()),
            ('costoFormulas', self.gf('django.db.models.fields.IntegerField')()),
            ('fechaElaboracion', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('fechaCaducidad', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'Fabricacion', ['Formula'])

        # Adding model 'DetalleFormula'
        db.create_table(u'Fabricacion_detalleformula', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('formula', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Formula'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('pesoUnitProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['DetalleFormula'])

        # Adding model 'Condimentado'
        db.create_table(u'Fabricacion_condimentado', (
            ('codigoCondimentado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('formula', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Formula'])),
            ('pesoProductoACondimentar', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoFormulaUsada', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('pesoProductoCondimentado', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['Condimentado'])

        # Adding model 'Miga'
        db.create_table(u'Fabricacion_miga', (
            ('codigoMiga', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaFabricacion', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('PesoFormulaMiga', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('cantidadFormulas', self.gf('django.db.models.fields.IntegerField')()),
            ('costoFormulaMiga', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Fabricacion', ['Miga'])

        # Adding model 'DetalleMiga'
        db.create_table(u'Fabricacion_detallemiga', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('miga', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Miga'])),
            ('PesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'Fabricacion', ['DetalleMiga'])

        # Adding model 'Apanado'
        db.create_table(u'Fabricacion_apanado', (
            ('codigoApanado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('miga', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Fabricacion.Miga'])),
            ('producto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Inventario.Producto'])),
            ('PesoProducto', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('PesoMiga', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('undProducto', self.gf('django.db.models.fields.IntegerField')()),
            ('PesoPosApanado', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('costoPosApanado', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Fabricacion', ['Apanado'])


    def backwards(self, orm):
        # Deleting model 'Enlagunado'
        db.delete_table(u'Fabricacion_enlagunado')

        # Deleting model 'DetalleEnlagunado'
        db.delete_table(u'Fabricacion_detalleenlagunado')

        # Deleting model 'LimpezaTajado'
        db.delete_table(u'Fabricacion_limpezatajado')

        # Deleting model 'PlanillaDesposte'
        db.delete_table(u'Fabricacion_planilladesposte')

        # Deleting model 'Canal'
        db.delete_table(u'Fabricacion_canal')

        # Deleting model 'DetallePlanilla'
        db.delete_table(u'Fabricacion_detalleplanilla')

        # Deleting model 'Formula'
        db.delete_table(u'Fabricacion_formula')

        # Deleting model 'DetalleFormula'
        db.delete_table(u'Fabricacion_detalleformula')

        # Deleting model 'Condimentado'
        db.delete_table(u'Fabricacion_condimentado')

        # Deleting model 'Miga'
        db.delete_table(u'Fabricacion_miga')

        # Deleting model 'DetalleMiga'
        db.delete_table(u'Fabricacion_detallemiga')

        # Deleting model 'Apanado'
        db.delete_table(u'Fabricacion_apanado')


    models = {
        u'Fabricacion.apanado': {
            'Meta': {'object_name': 'Apanado'},
            'PesoMiga': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'PesoPosApanado': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'PesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'codigoApanado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoPosApanado': ('django.db.models.fields.IntegerField', [], {}),
            'miga': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Miga']"}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'undProducto': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Fabricacion.canal': {
            'Meta': {'object_name': 'Canal'},
            'codigoCanal': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Ganado']"}),
            'peosTotalCanal': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoBrazos': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoPiernas': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'planilla': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.PlanillaDesposte']", 'null': 'True', 'blank': 'True'})
        },
        u'Fabricacion.condimentado': {
            'Meta': {'object_name': 'Condimentado'},
            'codigoCondimentado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'formula': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Formula']"}),
            'pesoFormulaUsada': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoACondimentar': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoCondimentado': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
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
        u'Fabricacion.detalleformula': {
            'Meta': {'object_name': 'DetalleFormula'},
            'formula': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Formula']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoUnitProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.detallemiga': {
            'Meta': {'object_name': 'DetalleMiga'},
            'PesoProducto': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miga': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Fabricacion.Miga']"}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"})
        },
        u'Fabricacion.detalleplanilla': {
            'CantPiezas': ('django.db.models.fields.IntegerField', [], {}),
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
        u'Fabricacion.formula': {
            'Meta': {'object_name': 'Formula'},
            'cantidadFormulas': ('django.db.models.fields.IntegerField', [], {}),
            'codigoFormula': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoFormulas': ('django.db.models.fields.IntegerField', [], {}),
            'fechaCaducidad': ('django.db.models.fields.DateTimeField', [], {}),
            'fechaElaboracion': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pesoFormula': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'responsable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Nomina.Empleado']"})
        },
        u'Fabricacion.limpezatajado': {
            'Meta': {'object_name': 'LimpezaTajado'},
            'codigoTajado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pesoGrasa': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProcesos': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoAntes': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'pesoProductoDespues': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'producto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Inventario.Producto']"}),
            'recortes': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Fabricacion.miga': {
            'Meta': {'object_name': 'Miga'},
            'PesoFormulaMiga': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'cantidadFormulas': ('django.db.models.fields.IntegerField', [], {}),
            'codigoMiga': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'costoFormulaMiga': ('django.db.models.fields.IntegerField', [], {}),
            'fechaFabricacion': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'Fabricacion.planilladesposte': {
            'Meta': {'object_name': 'PlanillaDesposte'},
            'codigoPlanilla': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'difCanalADespostado': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'fechaDesposte': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'resesADespostar': ('django.db.models.fields.IntegerField', [], {}),
            'totalDespostado': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'})
        },
        u'Inventario.ganado': {
            'Meta': {'object_name': 'Ganado'},
            'codigoGanado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'difPieCanal': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'fechaIngreso': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'genero': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'pesoEnPie': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'precioKiloEnPie': ('django.db.models.fields.IntegerField', [], {}),
            'precioTotal': ('django.db.models.fields.IntegerField', [], {})
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
            'vrVentaProducto': ('django.db.models.fields.IntegerField', [], {})
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