# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterAccount'
        db.create_table('brightonfemcol_twitteraccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
        ))
        db.send_create_signal('brightonfemcol', ['TwitterAccount'])

        # Adding model 'Tweet'
        db.create_table('brightonfemcol_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tweets', to=orm['brightonfemcol.TwitterAccount'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('brightonfemcol', ['Tweet'])


    def backwards(self, orm):
        # Deleting model 'TwitterAccount'
        db.delete_table('brightonfemcol_twitteraccount')

        # Deleting model 'Tweet'
        db.delete_table('brightonfemcol_tweet')


    models = {
        'brightonfemcol.tweet': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Tweet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweets'", 'to': "orm['brightonfemcol.TwitterAccount']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'brightonfemcol.twitteraccount': {
            'Meta': {'object_name': 'TwitterAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brightonfemcol']