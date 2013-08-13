# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'pybb_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pybb', ['Category'])

        # Adding model 'Forum'
        db.create_table(u'pybb_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forums', to=orm['pybb.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('topic_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('headline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('atom', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='forum', unique=True, null=True, to=orm['web.Atom'])),
        ))
        db.send_create_signal(u'pybb', ['Forum'])

        # Adding M2M table for field moderators on 'Forum'
        m2m_table_name = db.shorten_name(u'pybb_forum_moderators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('forum', models.ForeignKey(orm[u'pybb.forum'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['forum_id', 'user_id'])

        # Adding model 'Topic'
        db.create_table(u'pybb_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topics', to=orm['pybb.Forum'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('on_moderation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('poll_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('poll_question', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pybb', ['Topic'])

        # Adding M2M table for field subscribers on 'Topic'
        m2m_table_name = db.shorten_name(u'pybb_topic_subscribers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topic', models.ForeignKey(orm[u'pybb.topic'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['topic_id', 'user_id'])

        # Adding model 'Post'
        db.create_table(u'pybb_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
            ('body_text', self.gf('django.db.models.fields.TextField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['pybb.Topic'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user_ip', self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15, blank=True)),
            ('on_moderation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pybb', ['Post'])

        # Adding model 'Profile'
        db.create_table(u'pybb_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signature', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('signature_html', self.gf('django.db.models.fields.TextField')(max_length=1054, blank=True)),
            ('time_zone', self.gf('django.db.models.fields.FloatField')(default=3.0)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=10, blank=True)),
            ('show_signatures', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('avatar', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('autosubscribe', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('annoying.fields.AutoOneToOneField')(related_name='pybb_profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'pybb', ['Profile'])

        # Adding model 'Attachment'
        db.create_table(u'pybb_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attachments', to=orm['pybb.Post'])),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'pybb', ['Attachment'])

        # Adding model 'TopicReadTracker'
        db.create_table(u'pybb_topicreadtracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pybb.Topic'], null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pybb', ['TopicReadTracker'])

        # Adding unique constraint on 'TopicReadTracker', fields ['user', 'topic']
        db.create_unique(u'pybb_topicreadtracker', ['user_id', 'topic_id'])

        # Adding model 'ForumReadTracker'
        db.create_table(u'pybb_forumreadtracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pybb.Forum'], null=True, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pybb', ['ForumReadTracker'])

        # Adding unique constraint on 'ForumReadTracker', fields ['user', 'forum']
        db.create_unique(u'pybb_forumreadtracker', ['user_id', 'forum_id'])

        # Adding model 'PollAnswer'
        db.create_table(u'pybb_pollanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poll_answers', to=orm['pybb.Topic'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pybb', ['PollAnswer'])

        # Adding model 'PollAnswerUser'
        db.create_table(u'pybb_pollansweruser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll_answer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users', to=orm['pybb.PollAnswer'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poll_answers', to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'pybb', ['PollAnswerUser'])

        # Adding unique constraint on 'PollAnswerUser', fields ['poll_answer', 'user']
        db.create_unique(u'pybb_pollansweruser', ['poll_answer_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PollAnswerUser', fields ['poll_answer', 'user']
        db.delete_unique(u'pybb_pollansweruser', ['poll_answer_id', 'user_id'])

        # Removing unique constraint on 'ForumReadTracker', fields ['user', 'forum']
        db.delete_unique(u'pybb_forumreadtracker', ['user_id', 'forum_id'])

        # Removing unique constraint on 'TopicReadTracker', fields ['user', 'topic']
        db.delete_unique(u'pybb_topicreadtracker', ['user_id', 'topic_id'])

        # Deleting model 'Category'
        db.delete_table(u'pybb_category')

        # Deleting model 'Forum'
        db.delete_table(u'pybb_forum')

        # Removing M2M table for field moderators on 'Forum'
        db.delete_table(db.shorten_name(u'pybb_forum_moderators'))

        # Deleting model 'Topic'
        db.delete_table(u'pybb_topic')

        # Removing M2M table for field subscribers on 'Topic'
        db.delete_table(db.shorten_name(u'pybb_topic_subscribers'))

        # Deleting model 'Post'
        db.delete_table(u'pybb_post')

        # Deleting model 'Profile'
        db.delete_table(u'pybb_profile')

        # Deleting model 'Attachment'
        db.delete_table(u'pybb_attachment')

        # Deleting model 'TopicReadTracker'
        db.delete_table(u'pybb_topicreadtracker')

        # Deleting model 'ForumReadTracker'
        db.delete_table(u'pybb_forumreadtracker')

        # Deleting model 'PollAnswer'
        db.delete_table(u'pybb_pollanswer')

        # Deleting model 'PollAnswerUser'
        db.delete_table(u'pybb_pollansweruser')


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
        u'pybb.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': u"orm['pybb.Post']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
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
        u'pybb.pollanswer': {
            'Meta': {'object_name': 'PollAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_answers'", 'to': u"orm['pybb.Topic']"})
        },
        u'pybb.pollansweruser': {
            'Meta': {'unique_together': "(('poll_answer', 'user'),)", 'object_name': 'PollAnswerUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll_answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'to': u"orm['pybb.PollAnswer']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_answers'", 'to': u"orm['auth.User']"})
        },
        u'pybb.post': {
            'Meta': {'ordering': "['created']", 'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'body_text': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['pybb.Topic']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['auth.User']"}),
            'user_ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15', 'blank': 'True'})
        },
        u'pybb.profile': {
            'Meta': {'object_name': 'Profile'},
            'autosubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '10', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'signature_html': ('django.db.models.fields.TextField', [], {'max_length': '1054', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'related_name': "'pybb_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
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

    complete_apps = ['pybb']