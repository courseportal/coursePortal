# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'web_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'web', ['Category'])

        # Adding M2M table for field prereq on 'Category'
        m2m_table_name = db.shorten_name(u'web_category_prereq')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_category', models.ForeignKey(orm[u'web.category'], null=False)),
            ('to_category', models.ForeignKey(orm[u'web.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_category_id', 'to_category_id'])

        # Adding M2M table for field parent on 'Category'
        m2m_table_name = db.shorten_name(u'web_category_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_category', models.ForeignKey(orm[u'web.category'], null=False)),
            ('to_category', models.ForeignKey(orm[u'web.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_category_id', 'to_category_id'])

        # Adding model 'Exposition'
        db.create_table(u'web_exposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Category'])),
        ))
        db.send_create_signal(u'web', ['Exposition'])

        # Adding model 'Submission'
        db.create_table(u'web_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Submission'])

        # Adding M2M table for field tags on 'Submission'
        m2m_table_name = db.shorten_name(u'web_submission_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('submission', models.ForeignKey(orm[u'web.submission'], null=False)),
            ('category', models.ForeignKey(orm[u'web.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['submission_id', 'category_id'])

        # Adding model 'VoteCategory'
        db.create_table(u'web_votecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'web', ['VoteCategory'])

        # Adding model 'Vote'
        db.create_table(u'web_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['web.Submission'])),
            ('v_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['web.VoteCategory'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Vote'])

        # Adding model 'Class'
        db.create_table(u'web_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'web', ['Class'])

        # Adding M2M table for field allowed_users on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_allowed_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'user_id'])

        # Adding M2M table for field categories on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('category', models.ForeignKey(orm[u'web.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'category_id'])

        # Adding model 'QuestionInstance'
        db.create_table(u'web_questioninstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'web', ['QuestionInstance'])

        # Adding model 'Choice'
        db.create_table(u'web_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'web', ['Choice'])

        # Adding model 'Question'
        db.create_table(u'web_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('numChoices', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'web', ['Question'])

        # Adding model 'QuestionChoice'
        db.create_table(u'web_questionchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['web.Question'])),
        ))
        db.send_create_signal(u'web', ['QuestionChoice'])

        # Adding model 'QuestionVariable'
        db.create_table(u'web_questionvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variables', to=orm['web.Question'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('varType', self.gf('django.db.models.fields.CharField')(default='custom', max_length=15)),
            ('lowerBound', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('upperBound', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'web', ['QuestionVariable'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'web_category')

        # Removing M2M table for field prereq on 'Category'
        db.delete_table(db.shorten_name(u'web_category_prereq'))

        # Removing M2M table for field parent on 'Category'
        db.delete_table(db.shorten_name(u'web_category_parent'))

        # Deleting model 'Exposition'
        db.delete_table(u'web_exposition')

        # Deleting model 'Submission'
        db.delete_table(u'web_submission')

        # Removing M2M table for field tags on 'Submission'
        db.delete_table(db.shorten_name(u'web_submission_tags'))

        # Deleting model 'VoteCategory'
        db.delete_table(u'web_votecategory')

        # Deleting model 'Vote'
        db.delete_table(u'web_vote')

        # Deleting model 'Class'
        db.delete_table(u'web_class')

        # Removing M2M table for field allowed_users on 'Class'
        db.delete_table(db.shorten_name(u'web_class_allowed_users'))

        # Removing M2M table for field categories on 'Class'
        db.delete_table(db.shorten_name(u'web_class_categories'))

        # Deleting model 'QuestionInstance'
        db.delete_table(u'web_questioninstance')

        # Deleting model 'Choice'
        db.delete_table(u'web_choice')

        # Deleting model 'Question'
        db.delete_table(u'web_question')

        # Deleting model 'QuestionChoice'
        db.delete_table(u'web_questionchoice')

        # Deleting model 'QuestionVariable'
        db.delete_table(u'web_questionvariable')


    models = {
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
        u'web.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'child'", 'blank': 'True', 'to': u"orm['web.Category']"}),
            'prereq': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'postreq'", 'blank': 'True', 'to': u"orm['web.Category']"})
        },
        u'web.choice': {
            'Meta': {'object_name': 'Choice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {})
        },
        u'web.class': {
            'Meta': {'ordering': "['name']", 'object_name': 'Class'},
            'allowed_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'can_edit'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.exposition': {
            'Meta': {'ordering': "['title']", 'object_name': 'Exposition'},
            'cat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numChoices': ('django.db.models.fields.IntegerField', [], {}),
            'solution': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.questionchoice': {
            'Meta': {'object_name': 'QuestionChoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['web.Question']"}),
            'solution': ('django.db.models.fields.TextField', [], {})
        },
        u'web.questioninstance': {
            'Meta': {'object_name': 'QuestionInstance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.questionvariable': {
            'Meta': {'object_name': 'QuestionVariable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowerBound': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': u"orm['web.Question']"}),
            'upperBound': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'varType': ('django.db.models.fields.CharField', [], {'default': "'custom'", 'max_length': '15'})
        },
        u'web.submission': {
            'Meta': {'object_name': 'Submission'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Category']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        },
        u'web.vote': {
            'Meta': {'object_name': 'Vote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['web.Submission']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'v_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['web.VoteCategory']"})
        },
        u'web.votecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'VoteCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['web']