# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LectureNote'
        db.delete_table(u'web_lecturenote')

        # Deleting model 'Submission'
        db.delete_table(u'web_submission')

        # Removing M2M table for field tags on 'Submission'
        db.delete_table(db.shorten_name(u'web_submission_tags'))

        # Deleting model 'VoteCategory'
        db.delete_table(u'web_votecategory')

        # Deleting model 'Vote'
        db.delete_table(u'web_vote')

        # Deleting model 'AtomCategory'
        db.delete_table(u'web_atomcategory')

        # Removing M2M table for field child_categories on 'AtomCategory'
        db.delete_table(db.shorten_name(u'web_atomcategory_child_categories'))

        # Removing M2M table for field child_atoms on 'AtomCategory'
        db.delete_table(db.shorten_name(u'web_atomcategory_child_atoms'))

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

        # Deleting field 'Exposition.atom'
        db.delete_column(u'web_exposition', 'atom_id')

        # Adding field 'Exposition.date_created'
        db.add_column(u'web_exposition', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Exposition.date_modified'
        db.add_column(u'web_exposition', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True),
                      keep_default=False)

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

        # Deleting field 'Class.name'
        db.delete_column(u'web_class', 'name')

        # Deleting field 'Class.author'
        db.delete_column(u'web_class', 'author_id')

        # Adding field 'Class.title'
        db.add_column(u'web_class', 'title',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'Class.owner'
        db.add_column(u'web_class', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='classes_authored', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Class.date_created'
        db.add_column(u'web_class', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Class.date_modified'
        db.add_column(u'web_class', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field stickied_examples on 'Class'
        db.delete_table(db.shorten_name(u'web_class_stickied_examples'))

        # Removing M2M table for field stickied_videos on 'Class'
        db.delete_table(db.shorten_name(u'web_class_stickied_videos'))

        # Removing M2M table for field stickied_notes on 'Class'
        db.delete_table(db.shorten_name(u'web_class_stickied_notes'))

        # Removing M2M table for field allowed_users on 'Class'
        db.delete_table(db.shorten_name(u'web_class_allowed_users'))

        # Removing M2M table for field stickied_expos on 'Class'
        db.delete_table(db.shorten_name(u'web_class_stickied_expos'))

        # Adding M2M table for field instructors on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'user_id'])

        # Deleting field 'Atom.name'
        db.delete_column(u'web_atom', 'name')

        # Adding field 'Atom.title'
        db.add_column(u'web_atom', 'title',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)

        # Deleting field 'BaseCategory.name'
        db.delete_column(u'web_basecategory', 'name')

        # Adding field 'BaseCategory.title'
        db.add_column(u'web_basecategory', 'title',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)

        # Adding field 'BaseCategory.date_created'
        db.add_column(u'web_basecategory', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseCategory.date_modified'
        db.add_column(u'web_basecategory', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field child_categories on 'BaseCategory'
        db.delete_table(db.shorten_name(u'web_basecategory_child_categories'))

        # Adding M2M table for field parent_categories on 'BaseCategory'
        m2m_table_name = db.shorten_name(u'web_basecategory_parent_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_basecategory', models.ForeignKey(orm[u'web.basecategory'], null=False)),
            ('to_basecategory', models.ForeignKey(orm[u'web.basecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_basecategory_id', 'to_basecategory_id'])

        # Deleting field 'Example.atom'
        db.delete_column(u'web_example', 'atom_id')

        # Deleting field 'Example.filename'
        db.delete_column(u'web_example', 'filename')

        # Adding field 'Example.title'
        db.add_column(u'web_example', 'title',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)

        # Adding field 'Example.date_modified'
        db.add_column(u'web_example', 'date_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True),
                      keep_default=False)

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


        # Changing field 'Example.date_created'
        db.alter_column(u'web_example', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Adding model 'LectureNote'
        db.create_table(u'web_lecturenote', (
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('atom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lecturenote_set', to=orm['web.Atom'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lecturenote_set', to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'web', ['LectureNote'])

        # Adding model 'Submission'
        db.create_table(u'web_submission', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video_owner', to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Submission'])

        # Adding M2M table for field tags on 'Submission'
        m2m_table_name = db.shorten_name(u'web_submission_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('submission', models.ForeignKey(orm[u'web.submission'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['submission_id', 'atom_id'])

        # Adding model 'VoteCategory'
        db.create_table(u'web_votecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'web', ['VoteCategory'])

        # Adding model 'Vote'
        db.create_table(u'web_vote', (
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes_s', to=orm['web.Submission'])),
            ('v_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes_s', to=orm['web.VoteCategory'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'web', ['Vote'])

        # Adding model 'AtomCategory'
        db.create_table(u'web_atomcategory', (
            ('parent_class', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='category_set', null=True, to=orm['web.Class'], blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'web', ['AtomCategory'])

        # Adding M2M table for field child_categories on 'AtomCategory'
        m2m_table_name = db.shorten_name(u'web_atomcategory_child_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_atomcategory', models.ForeignKey(orm[u'web.atomcategory'], null=False)),
            ('to_atomcategory', models.ForeignKey(orm[u'web.atomcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_atomcategory_id', 'to_atomcategory_id'])

        # Adding M2M table for field child_atoms on 'AtomCategory'
        m2m_table_name = db.shorten_name(u'web_atomcategory_child_atoms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('atomcategory', models.ForeignKey(orm[u'web.atomcategory'], null=False)),
            ('atom', models.ForeignKey(orm[u'web.atom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['atomcategory_id', 'atom_id'])

        # Deleting model 'Video'
        db.delete_table(u'web_video')

        # Removing M2M table for field atoms on 'Video'
        db.delete_table(db.shorten_name(u'web_video_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Video'
        db.delete_table(db.shorten_name(u'web_video_classes_stickied_in'))

        # Deleting model 'Note'
        db.delete_table(u'web_note')

        # Removing M2M table for field atoms on 'Note'
        db.delete_table(db.shorten_name(u'web_note_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Note'
        db.delete_table(db.shorten_name(u'web_note_classes_stickied_in'))

        # Deleting model 'ClassCategory'
        db.delete_table(u'web_classcategory')

        # Removing M2M table for field parent_categories on 'ClassCategory'
        db.delete_table(db.shorten_name(u'web_classcategory_parent_categories'))

        # Removing M2M table for field child_atoms on 'ClassCategory'
        db.delete_table(db.shorten_name(u'web_classcategory_child_atoms'))

        # Adding field 'Exposition.atom'
        db.add_column(u'web_exposition', 'atom',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['web.Atom']),
                      keep_default=False)

        # Deleting field 'Exposition.date_created'
        db.delete_column(u'web_exposition', 'date_created')

        # Deleting field 'Exposition.date_modified'
        db.delete_column(u'web_exposition', 'date_modified')

        # Removing M2M table for field atoms on 'Exposition'
        db.delete_table(db.shorten_name(u'web_exposition_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Exposition'
        db.delete_table(db.shorten_name(u'web_exposition_classes_stickied_in'))

        # Adding field 'Class.name'
        db.add_column(u'web_class', 'name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'Class.author'
        db.add_column(u'web_class', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='classes_authored', to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Class.title'
        db.delete_column(u'web_class', 'title')

        # Deleting field 'Class.owner'
        db.delete_column(u'web_class', 'owner_id')

        # Deleting field 'Class.date_created'
        db.delete_column(u'web_class', 'date_created')

        # Deleting field 'Class.date_modified'
        db.delete_column(u'web_class', 'date_modified')

        # Adding M2M table for field stickied_examples on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_stickied_examples')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('example', models.ForeignKey(orm[u'web.example'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'example_id'])

        # Adding M2M table for field stickied_videos on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_stickied_videos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('submission', models.ForeignKey(orm[u'web.submission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'submission_id'])

        # Adding M2M table for field stickied_notes on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_stickied_notes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('lecturenote', models.ForeignKey(orm[u'web.lecturenote'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'lecturenote_id'])

        # Adding M2M table for field allowed_users on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_allowed_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'user_id'])

        # Adding M2M table for field stickied_expos on 'Class'
        m2m_table_name = db.shorten_name(u'web_class_stickied_expos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'web.class'], null=False)),
            ('exposition', models.ForeignKey(orm[u'web.exposition'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'exposition_id'])

        # Removing M2M table for field instructors on 'Class'
        db.delete_table(db.shorten_name(u'web_class_instructors'))

        # Adding field 'Atom.name'
        db.add_column(u'web_atom', 'name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)

        # Deleting field 'Atom.title'
        db.delete_column(u'web_atom', 'title')

        # Adding field 'BaseCategory.name'
        db.add_column(u'web_basecategory', 'name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)

        # Deleting field 'BaseCategory.title'
        db.delete_column(u'web_basecategory', 'title')

        # Deleting field 'BaseCategory.date_created'
        db.delete_column(u'web_basecategory', 'date_created')

        # Deleting field 'BaseCategory.date_modified'
        db.delete_column(u'web_basecategory', 'date_modified')

        # Adding M2M table for field child_categories on 'BaseCategory'
        m2m_table_name = db.shorten_name(u'web_basecategory_child_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_basecategory', models.ForeignKey(orm[u'web.basecategory'], null=False)),
            ('to_basecategory', models.ForeignKey(orm[u'web.basecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_basecategory_id', 'to_basecategory_id'])

        # Removing M2M table for field parent_categories on 'BaseCategory'
        db.delete_table(db.shorten_name(u'web_basecategory_parent_categories'))

        # Adding field 'Example.atom'
        db.add_column(u'web_example', 'atom',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='example_set', to=orm['web.Atom']),
                      keep_default=False)

        # Adding field 'Example.filename'
        db.add_column(u'web_example', 'filename',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)

        # Deleting field 'Example.title'
        db.delete_column(u'web_example', 'title')

        # Deleting field 'Example.date_modified'
        db.delete_column(u'web_example', 'date_modified')

        # Removing M2M table for field atoms on 'Example'
        db.delete_table(db.shorten_name(u'web_example_atoms'))

        # Removing M2M table for field classes_stickied_in on 'Example'
        db.delete_table(db.shorten_name(u'web_example_classes_stickied_in'))


        # Changing field 'Example.date_created'
        db.alter_column(u'web_example', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

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
        u'assignment.question': {
            'Meta': {'object_name': 'Question'},
            'atoms': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assignments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'stickied_assignments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'classes_stickied_in'", 'blank': 'True', 'to': u"orm['assignment.Assignment']"}),
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