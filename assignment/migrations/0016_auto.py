# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field atoms on 'Question'
        m2m_table_name = db.shorten_name(u'assignment_question_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'assignment.question'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'atom_id'])


    def backwards(self, orm):
        # Removing M2M table for field atoms on 'Question'
        db.delete_table(db.shorten_name(u'assignment_question_atoms'))


    models = {
        u'assignment.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'owned_assignments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_to'", 'symmetrical': 'False', 'to': u"orm['assignment.Question']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        u'assignment.assignmentinstance': {
            'Meta': {'object_name': 'AssignmentInstance'},
            'can_edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
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
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assignments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'owned_questions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'assignment.questioninstance': {
            'Meta': {'object_name': 'QuestionInstance'},
            'assignmentInstance': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'questions'", 'to': u"orm['assignment.AssignmentInstance']"}),
            'can_edit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {}),
            'student_answer': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
        },
        u'web.atom': {
            'Meta': {'ordering': "['name']", 'object_name': 'Atom'},
            'base_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_atoms'", 'to': u"orm['web.BaseCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is no summary added at this time.'"})
        },
        u'web.basecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'BaseCategory'},
            'child_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'parent_categories'", 'blank': 'True', 'to': u"orm['web.BaseCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is no summary added at this time.'"})
        }
    }

    complete_apps = ['assignment']