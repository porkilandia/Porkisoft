# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cliente.nit'
        db.add_column(u'Telemercadeo_cliente', 'nit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cliente.nit'
        db.delete_column(u'Telemercadeo_cliente', 'nit')


    models = {
        u'Telemercadeo.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'codigoCliente': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'direccionCliente': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nombreCliente': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefonoCliente': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['Telemercadeo']