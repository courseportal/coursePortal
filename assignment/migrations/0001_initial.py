# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'assignment_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'assignment', ['Question'])

        # Adding model 'Assignment'
        db.create_table(u'assignment_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal(u'assignment', ['Assignment'])

        # Adding M2M table for field questions on 'Assignment'
        m2m_table_name = db.shorten_name(u'assignment_assignment_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('assignment', models.ForeignKey(orm[u'assignment.assignment'], null=False)),
            ('question', models.ForeignKey(orm[u'assignment.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['assignment_id', 'question_id'])

        # Adding M2M table for field users on 'Assignment'
        m2m_table_name = db.shorten_name(u'assignment_assignment_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('assignment', models.ForeignKey(orm[u'assignment.assignment'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['assignment_id', 'user_id'])

        # Adding model 'AssignmentInstance'
        db.create_table(u'assignment_assignmentinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignmentInstances', to=orm['auth.User'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['assignment.Assignment'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('max_score', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'assignment', ['AssignmentInstance'])

        # Adding model 'QuestionInstance'
        db.create_table(u'assignment_questioninstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('assignmentInstance', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='questions', to=orm['assignment.AssignmentInstance'])),
        ))
        db.send_create_signal(u'assignment', ['QuestionInstance'])

        # Adding model 'ChoiceInstance'
        db.create_table(u'assignment_choiceinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choiceInstances', to=orm['assignment.QuestionInstance'])),
        ))
        db.send_create_signal(u'assignment', ['ChoiceInstance'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'assignment_question')

        # Deleting model 'Assignment'
        db.delete_table(u'assignment_assignment')

        # Removing M2M table for field questions on 'Assignment'
        db.delete_table(db.shorten_name(u'assignment_assignment_questions'))

        # Removing M2M table for field users on 'Assignment'
        db.delete_table(db.shorten_name(u'assignment_assignment_users'))

        # Deleting model 'AssignmentInstance'
        db.delete_table(u'assignment_assignmentinstance')

        # Deleting model 'QuestionInstance'
        db.delete_table(u'assignment_questioninstance')

        # Deleting model 'ChoiceInstance'
        db.delete_table(u'assignment_choiceinstance')


    models = {
        u'assignment.assignment': {
            'Meta': {'object_name': 'Assignment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['assignment.Question']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'templates'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'assignment.assignmentinstance': {
            'Meta': {'object_name': 'AssignmentInstance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['assignment.Assignment']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignmentInstances'", 'to': u"orm['auth.User']"})
        },
        u'assignment.choiceinstance': {
            'Meta': {'object_name': 'ChoiceInstance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choiceInstances'", 'to': u"orm['assignment.QuestionInstance']"}),
            'solution': ('django.db.models.fields.TextField', [], {})
        },
        u'assignment.question': {
            'Meta': {'object_name': 'Question'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'assignment.questioninstance': {
            'Meta': {'object_name': 'QuestionInstance'},
            'assignmentInstance': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'questions'", 'to': u"orm['assignment.AssignmentInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assignment']