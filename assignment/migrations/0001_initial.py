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
            ('numCorrect', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('numIncorrect', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('isCopy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='copy', null=True, on_delete=models.SET_NULL, to=orm['assignment.Question'])),
        ))
        db.send_create_signal(u'assignment', ['Question'])

        # Adding M2M table for field owners on 'Question'
        m2m_table_name = db.shorten_name(u'assignment_question_owners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'assignment.question'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'user_id'])

        # Adding M2M table for field atoms on 'Question'
        m2m_table_name = db.shorten_name(u'assignment_question_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'assignment.question'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'atom_id'])

        # Adding model 'Assignment'
        db.create_table(u'assignment_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('isCopy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
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

        # Adding M2M table for field owners on 'Assignment'
        m2m_table_name = db.shorten_name(u'assignment_assignment_owners')
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
            ('can_edit', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('max_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'assignment', ['AssignmentInstance'])

        # Adding model 'QuestionInstance'
        db.create_table(u'assignment_questioninstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('can_edit', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('student_answer', self.gf('django.db.models.fields.TextField')(default='')),
            ('assignmentInstance', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='questions', to=orm['assignment.AssignmentInstance'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='instances', to=orm['assignment.Question'])),
        ))
        db.send_create_signal(u'assignment', ['QuestionInstance'])

        # Adding model 'ChoiceInstance'
        db.create_table(u'assignment_choiceinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choiceInstances', to=orm['assignment.QuestionInstance'])),
        ))
        db.send_create_signal(u'assignment', ['ChoiceInstance'])

        # Adding model 'Variable'
        db.create_table(u'assignment_variable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('variables', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('validation_code', self.gf('django.db.models.fields.TextField')(default='result=0')),
            ('generated_code', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'assignment', ['Variable'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'assignment_question')

        # Removing M2M table for field owners on 'Question'
        db.delete_table(db.shorten_name(u'assignment_question_owners'))

        # Removing M2M table for field atoms on 'Question'
        db.delete_table(db.shorten_name(u'assignment_question_atoms'))

        # Deleting model 'Assignment'
        db.delete_table(u'assignment_assignment')

        # Removing M2M table for field questions on 'Assignment'
        db.delete_table(db.shorten_name(u'assignment_assignment_questions'))

        # Removing M2M table for field owners on 'Assignment'
        db.delete_table(db.shorten_name(u'assignment_assignment_owners'))

        # Deleting model 'AssignmentInstance'
        db.delete_table(u'assignment_assignmentinstance')

        # Deleting model 'QuestionInstance'
        db.delete_table(u'assignment_questioninstance')

        # Deleting model 'ChoiceInstance'
        db.delete_table(u'assignment_choiceinstance')

        # Deleting model 'Variable'
        db.delete_table(u'assignment_variable')


    models = {
        u'assignment.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCopy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'owned_assignments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assigned_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['assignment.Question']"}),
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
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_questions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCopy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numCorrect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'numIncorrect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'copy'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['assignment.Question']"}),
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
            'template': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'instances'", 'to': u"orm['assignment.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        u'assignment.variable': {
            'Meta': {'object_name': 'Variable'},
            'generated_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'validation_code': ('django.db.models.fields.TextField', [], {'default': "'result=0'"}),
            'variables': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'Meta': {'ordering': "['title']", 'object_name': 'Atom'},
            'base_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_atoms'", 'to': u"orm['web.BaseCategory']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u'There is currently no summary.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.basecategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'BaseCategory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'child_categories'", 'blank': 'True', 'to': u"orm['web.BaseCategory']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u'There is currently no summary.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['assignment']