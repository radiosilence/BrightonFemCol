# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TwitterAccount.image_url'
        db.delete_column('brightonfemcol_twitteraccount', 'image_url')

        # Adding field 'TwitterAccount.image'
        db.add_column('brightonfemcol_twitteraccount', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TwitterAccount.image_url'
        db.add_column('brightonfemcol_twitteraccount', 'image_url',
                      self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'TwitterAccount.image'
        db.delete_column('brightonfemcol_twitteraccount', 'image')


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
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brightonfemcol']