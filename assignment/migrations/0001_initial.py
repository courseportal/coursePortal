# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionInstance'
        db.create_table(u'assignment_questioninstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'assignment', ['QuestionInstance'])

        # Adding model 'Choice'
        db.create_table(u'assignment_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'assignment', ['Choice'])

        # Adding model 'Question'
        db.create_table(u'assignment_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('numChoices', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'assignment', ['Question'])

        # Adding model 'QuestionChoice'
        db.create_table(u'assignment_questionchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['assignment.Question'])),
        ))
        db.send_create_signal(u'assignment', ['QuestionChoice'])

        # Adding model 'QuestionVariable'
        db.create_table(u'assignment_questionvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variables', to=orm['assignment.Question'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('varType', self.gf('django.db.models.fields.CharField')(default='custom', max_length=15)),
            ('lowerBound', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('upperBound', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'assignment', ['QuestionVariable'])


    def backwards(self, orm):
        # Deleting model 'QuestionInstance'
        db.delete_table(u'assignment_questioninstance')

        # Deleting model 'Choice'
        db.delete_table(u'assignment_choice')

        # Deleting model 'Question'
        db.delete_table(u'assignment_question')

        # Deleting model 'QuestionChoice'
        db.delete_table(u'assignment_questionchoice')

        # Deleting model 'QuestionVariable'
        db.delete_table(u'assignment_questionvariable')


    models = {
        u'assignment.choice': {
            'Meta': {'object_name': 'Choice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {})
        },
        u'assignment.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numChoices': ('django.db.models.fields.IntegerField', [], {}),
            'solution': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'assignment.questionchoice': {
            'Meta': {'object_name': 'QuestionChoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['assignment.Question']"}),
            'solution': ('django.db.models.fields.TextField', [], {})
        },
        u'assignment.questioninstance': {
            'Meta': {'object_name': 'QuestionInstance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'assignment.questionvariable': {
            'Meta': {'object_name': 'QuestionVariable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowerBound': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': u"orm['assignment.Question']"}),
            'upperBound': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'varType': ('django.db.models.fields.CharField', [], {'default': "'custom'", 'max_length': '15'})
        }
    }

    complete_apps = ['assignment']