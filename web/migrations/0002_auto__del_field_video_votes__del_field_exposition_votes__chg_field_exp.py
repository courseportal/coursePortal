# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Video.votes'
        db.delete_column(u'web_video', 'votes')

        # Deleting field 'Exposition.votes'
        db.delete_column(u'web_exposition', 'votes')


        # Changing field 'Exposition.title'
        db.alter_column(u'web_exposition', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Adding M2M table for field stickied_assignments on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_stickied_assignments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('assignment', models.ForeignKey(orm[u'assignment.assignment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'assignment_id'])


        # Changing field 'Class.title'
        db.alter_column(u'web_class', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Adding field 'Atom.date_created'
        db.add_column(u'web_atom', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Atom.date_modified'
        db.add_column(u'web_atom', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True),
                      keep_default=False)

        # Deleting field 'Note.votes'
        db.delete_column(u'web_note', 'votes')

        # Deleting field 'Example.votes'
        db.delete_column(u'web_example', 'votes')

        # Adding field 'ClassCategory.summary'
        db.add_column(u'web_classcategory', 'summary',
                      self.gf('django.db.models.fields.TextField')(default=u'There is currently no summary.'),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Video.votes'
        db.add_column(u'web_video', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Exposition.votes'
        db.add_column(u'web_exposition', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Exposition.title'
        db.alter_column(u'web_exposition', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Removing M2M table for field stickied_assignments on 'Class'
        db.delete_table(db.shorten_name(u'web_class_stickied_assignments'))


        # Changing field 'Class.title'
        db.alter_column(u'web_class', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Deleting field 'Atom.date_created'
        db.delete_column(u'web_atom', 'date_created')

        # Deleting field 'Atom.date_modified'
        db.delete_column(u'web_atom', 'date_modified')

        # Adding field 'Note.votes'
        db.add_column(u'web_note', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Example.votes'
        db.add_column(u'web_example', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ClassCategory.summary'
        db.delete_column(u'web_classcategory', 'summary')


    models = {
        u'assignment.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCopy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'owned_assignments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_to'", 'symmetrical': 'False', 'to': u"orm['assignment.Question']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
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
        },
        u'web.class': {
            'Meta': {'ordering': "['title']", 'object_name': 'Class'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'allowed_classes'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes_authored'", 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'stickied_assignments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'classes_stickied_in'", 'blank': 'True', 'to': u"orm['assignment.Assignment']"}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'enrolled_classes'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u'There is currently no summary.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.classcategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'ClassCategory'},
            'child_atoms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'categories'", 'blank': 'True', 'to': u"orm['web.Atom']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'child_categories'", 'blank': 'True', 'to': u"orm['web.ClassCategory']"}),
            'parent_class': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'category_set'", 'null': 'True', 'blank': 'True', 'to': u"orm['web.Class']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u'There is currently no summary.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.example': {
            'Meta': {'ordering': "['title']", 'object_name': 'Example'},
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'example_set'", 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'classes_stickied_in': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stickied_examples'", 'blank': 'True', 'to': u"orm['web.Class']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'example_set'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.exposition': {
            'Meta': {'ordering': "['title']", 'object_name': 'Exposition'},
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'exposition_set'", 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'classes_stickied_in': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stickied_expositions'", 'blank': 'True', 'to': u"orm['web.Class']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "'http://'", 'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exposition_set'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.note': {
            'Meta': {'ordering': "['title']", 'object_name': 'Note'},
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'note_set'", 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'classes_stickied_in': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stickied_notes'", 'blank': 'True', 'to': u"orm['web.Class']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'note_set'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.video': {
            'Meta': {'ordering': "['title']", 'object_name': 'Video'},
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_set'", 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'classes_stickied_in': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stickied_videos'", 'blank': 'True', 'to': u"orm['web.Class']"}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'-'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_owner'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        }
    }

    complete_apps = ['web']