# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BaseCategory'
        db.create_table(u'web_basecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('summary', self.gf('django.db.models.fields.TextField')(default='There is currently no summary.')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['BaseCategory'])

        # Adding M2M table for field parent_categories on 'BaseCategory'
        m2m_table_name = db.shorten_name(u'web_basecategory_parent_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_basecategory', models.ForeignKey(orm[u'web.basecategory'], null=False)),
            ('to_basecategory', models.ForeignKey(orm[u'web.basecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_basecategory_id', 'to_basecategory_id'])

        # Adding model 'Atom'
        db.create_table(u'web_atom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('summary', self.gf('django.db.models.fields.TextField')(default=u'There is no summary added at this time.')),
            ('base_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_atoms', to=orm['web.BaseCategory'])),
        ))
        db.send_create_signal(u'web', ['Atom'])

        # Adding model 'Video'
        db.create_table(u'web_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video_owner', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Video'])

        # Adding M2M table for field atoms on 'Video'
        m2m_table_name = db.shorten_name(u'web_video_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm[u'web.video'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['video_id', 'atom_id'])

        # Adding M2M table for field classes_stickied_in on 'Video'
        m2m_table_name = db.shorten_name(u'web_video_classes_stickied_in')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm[u'web.video'], null=False)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False))
        ))
        db.create_unique(m2m_table_name, ['video_id', 'class_id'])

        # Adding model 'Exposition'
        db.create_table(u'web_exposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.CharField')(default='http://', max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exposition_set', to=orm['auth.User'])),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Exposition'])

        # Adding M2M table for field atoms on 'Exposition'
        m2m_table_name = db.shorten_name(u'web_exposition_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exposition', models.ForeignKey(orm[u'web.exposition'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['exposition_id', 'atom_id'])

        # Adding M2M table for field classes_stickied_in on 'Exposition'
        m2m_table_name = db.shorten_name(u'web_exposition_classes_stickied_in')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exposition', models.ForeignKey(orm[u'web.exposition'], null=False)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False))
        ))
        db.create_unique(m2m_table_name, ['exposition_id', 'class_id'])

        # Adding model 'Note'
        db.create_table(u'web_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='note_set', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Note'])

        # Adding M2M table for field atoms on 'Note'
        m2m_table_name = db.shorten_name(u'web_note_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('note', models.ForeignKey(orm[u'web.note'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['note_id', 'atom_id'])

        # Adding M2M table for field classes_stickied_in on 'Note'
        m2m_table_name = db.shorten_name(u'web_note_classes_stickied_in')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('note', models.ForeignKey(orm[u'web.note'], null=False)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False))
        ))
        db.create_unique(m2m_table_name, ['note_id', 'class_id'])

        # Adding model 'Example'
        db.create_table(u'web_example', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='example_set', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Example'])

        # Adding M2M table for field atoms on 'Example'
        m2m_table_name = db.shorten_name(u'web_example_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('example', models.ForeignKey(orm[u'web.example'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['example_id', 'atom_id'])

        # Adding M2M table for field classes_stickied_in on 'Example'
        m2m_table_name = db.shorten_name(u'web_example_classes_stickied_in')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('example', models.ForeignKey(orm[u'web.example'], null=False)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False))
        ))
        db.create_unique(m2m_table_name, ['example_id', 'class_id'])

        # Adding model 'Class'
        db.create_table(u'web_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classes_authored', to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('summary', self.gf('django.db.models.fields.TextField')(default='There is no summary added at this time.')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Class'])

        # Adding M2M table for field instructors on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'user_id'])

        # Adding M2M table for field students on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'user_id'])

        # Adding model 'ClassCategory'
        db.create_table(u'web_classcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent_class', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='category_set', null=True, blank=True, to=orm['web.Class'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['ClassCategory'])

        # Adding M2M table for field parent_categories on 'ClassCategory'
        m2m_table_name = db.shorten_name(u'web_classcategory_parent_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_classcategory', models.ForeignKey(orm[u'web.classcategory'], null=False)),
            ('to_classcategory', models.ForeignKey(orm[u'web.classcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_classcategory_id', 'to_classcategory_id'])

        # Adding M2M table for field child_atoms on 'ClassCategory'
        m2m_table_name = db.shorten_name(u'web_classcategory_child_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classcategory', models.ForeignKey(orm[u'web.classcategory'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classcategory_id', 'atom_id'])


    def backwards(self, orm):
        # Deleting model 'BaseCategory'
        db.delete_table(u'web_basecategory')

        # Removing M2M table for field parent_categories on 'BaseCategory'
        db.delete_table(db.shorten_name(u'web_basecategory_parent_categories'))

        # Deleting model 'Atom'
        db.delete_table(u'web_atom')

        # Deleting model 'Video'
        db.delete_table(u'web_video')

        # Removing M2M table for field atoms on 'Video'
        db.delete_table(db.shorten_name(u'web_video_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Video'
        db.delete_table(db.shorten_name(u'web_video_classes_stickied_in'))

        # Deleting model 'Exposition'
        db.delete_table(u'web_exposition')

        # Removing M2M table for field atoms on 'Exposition'
        db.delete_table(db.shorten_name(u'web_exposition_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Exposition'
        db.delete_table(db.shorten_name(u'web_exposition_classes_stickied_in'))

        # Deleting model 'Note'
        db.delete_table(u'web_note')

        # Removing M2M table for field atoms on 'Note'
        db.delete_table(db.shorten_name(u'web_note_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Note'
        db.delete_table(db.shorten_name(u'web_note_classes_stickied_in'))

        # Deleting model 'Example'
        db.delete_table(u'web_example')

        # Removing M2M table for field atoms on 'Example'
        db.delete_table(db.shorten_name(u'web_example_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Example'
        db.delete_table(db.shorten_name(u'web_example_classes_stickied_in'))

        # Deleting model 'Class'
        db.delete_table(u'web_class')

        # Removing M2M table for field instructors on 'Class'
        db.delete_table(db.shorten_name(u'web_class_instructors'))

        # Removing M2M table for field students on 'Class'
        db.delete_table(db.shorten_name(u'web_class_students'))

        # Deleting model 'ClassCategory'
        db.delete_table(u'web_classcategory')

        # Removing M2M table for field parent_categories on 'ClassCategory'
        db.delete_table(db.shorten_name(u'web_classcategory_parent_categories'))

        # Removing M2M table for field child_atoms on 'ClassCategory'
        db.delete_table(db.shorten_name(u'web_classcategory_child_atoms'))


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
        u'web.atom': {
            'Meta': {'ordering': "['title']", 'object_name': 'Atom'},
            'base_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_atoms'", 'to': u"orm['web.BaseCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "u'There is no summary added at this time.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'web.basecategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'BaseCategory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'child_categories'", 'blank': 'True', 'to': u"orm['web.BaseCategory']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is currently no summary.'"}),
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
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'enrolled_classes'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is no summary added at this time.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.classcategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'ClassCategory'},
            'child_atoms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'categories'", 'blank': 'True', 'to': u"orm['web.Atom']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'child_categories'", 'blank': 'True', 'to': u"orm['web.ClassCategory']"}),
            'parent_class': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'category_set'", 'null': 'True', 'blank': 'True', 'to': u"orm['web.Class']"}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.video': {
            'Meta': {'ordering': "['title']", 'object_name': 'Video'},
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_set'", 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'classes_stickied_in': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'stickied_videos'", 'blank': 'True', 'to': u"orm['web.Class']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_owner'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['web']