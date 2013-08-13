# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table(u'rating_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('atom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Atom'])),
            ('vote', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Video'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vote_set', null=True, to=orm['web.Note'])),
            ('exposition', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vote_set', null=True, to=orm['web.Exposition'])),
            ('example', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vote_set', null=True, to=orm['web.Example'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vote_set', null=True, to=orm['pybb.Topic'])),
        ))
        db.send_create_signal(u'rating', ['Vote'])

        # Adding model 'UserRating'
        db.create_table(u'rating_userrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rating_set', to=orm['auth.User'])),
            ('ExpoRating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('LecNoteRating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ExampleRating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('VideoRating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('TopicRating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('VoteUp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('VoteDown', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'rating', ['UserRating'])


    def backwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table(u'rating_vote')

        # Deleting model 'UserRating'
        db.delete_table(u'rating_userrating')


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
        u'pybb.category': {
            'Meta': {'ordering': "['position', 'name']", 'object_name': 'Category'},
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'pybb.forum': {
            'Meta': {'ordering': "['position', 'name']", 'object_name': 'Forum'},
            'atom': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'forum'", 'unique': 'True', 'null': 'True', 'to': u"orm['web.Atom']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forums'", 'to': u"orm['pybb.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'readed_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'readed_forums'", 'symmetrical': 'False', 'through': u"orm['pybb.ForumReadTracker']", 'to': u"orm['auth.User']"}),
            'topic_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pybb.forumreadtracker': {
            'Meta': {'unique_together': "(('user', 'forum'),)", 'object_name': 'ForumReadTracker'},
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pybb.Forum']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'pybb.topic': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Topic'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': u"orm['pybb.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'on_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'poll_question': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'poll_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'readed_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'readed_topics'", 'symmetrical': 'False', 'through': u"orm['pybb.TopicReadTracker']", 'to': u"orm['auth.User']"}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'subscriptions'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'pybb.topicreadtracker': {
            'Meta': {'unique_together': "(('user', 'topic'),)", 'object_name': 'TopicReadTracker'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pybb.Topic']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'rating.userrating': {
            'ExampleRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ExpoRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'LecNoteRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'Meta': {'object_name': 'UserRating'},
            'TopicRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'VideoRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'VoteDown': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'VoteUp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rating_set'", 'to': u"orm['auth.User']"})
        },
        u'rating.vote': {
            'Meta': {'object_name': 'Vote'},
            'atom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Atom']"}),
            'example': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vote_set'", 'null': 'True', 'to': u"orm['web.Example']"}),
            'exposition': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vote_set'", 'null': 'True', 'to': u"orm['web.Exposition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vote_set'", 'null': 'True', 'to': u"orm['web.Note']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vote_set'", 'null': 'True', 'to': u"orm['pybb.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Video']", 'null': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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

    complete_apps = ['rating']