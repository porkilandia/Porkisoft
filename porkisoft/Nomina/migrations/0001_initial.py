# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cargo'
        db.create_table(u'Nomina_cargo', (
            ('codigoCargo', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombreCargo', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'Nomina', ['Cargo'])

        # Adding model 'Empleado'
        db.create_table(u'Nomina_empleado', (
            ('codigoEmpleado', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('cargo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Nomina.Cargo'])),
        ))
        db.send_create_signal(u'Nomina', ['Empleado'])


    def backwards(self, orm):
        # Deleting model 'Cargo'
        db.delete_table(u'Nomina_cargo')

        # Deleting model 'Empleado'
        db.delete_table(u'Nomina_empleado')


    models = {
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

    complete_apps = ['Nomina']