# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BugReport'
        db.create_table(u'knoatom_bugreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('cc_myself', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'knoatom', ['BugReport'])


    def backwards(self, orm):
        # Deleting model 'BugReport'
        db.delete_table(u'knoatom_bugreport')


    models = {
        u'knoatom.bugreport': {
            'Meta': {'ordering': "['subject']", 'object_name': 'BugReport'},
            'cc_myself': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['knoatom']