# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('suave_calendar_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True, db_index=True)),
            ('body', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('suave_calendar', ['Event'])

        # Adding model 'EventLink'
        db.create_table('suave_calendar_eventlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['suave_calendar.Event'])),
        ))
        db.send_create_signal('suave_calendar', ['EventLink'])

        # Adding model 'EventImage'
        db.create_table('suave_calendar_eventimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=511, null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['suave_calendar.Event'])),
            ('gallery', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('suave_calendar', ['EventImage'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('suave_calendar_event')

        # Deleting model 'EventLink'
        db.delete_table('suave_calendar_eventlink')

        # Deleting model 'EventImage'
        db.delete_table('suave_calendar_eventimage')


    models = {
        'suave_calendar.event': {
            'Meta': {'object_name': 'Event'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'body': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave_calendar.eventimage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EventImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['suave_calendar.Event']"}),
            'gallery': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'})
        },
        'suave_calendar.eventlink': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EventLink'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['suave_calendar.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['suave_calendar']