# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('suave_calendar_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True, db_index=True)),
            ('body', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('suave_calendar', ['Category'])

        # Adding field 'Event.category'
        db.add_column('suave_calendar_event', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='primary_events', null=True, to=orm['suave_calendar.Category']),
                      keep_default=False)

        # Adding M2M table for field categories on 'Event'
        db.create_table('suave_calendar_event_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['suave_calendar.event'], null=False)),
            ('category', models.ForeignKey(orm['suave_calendar.category'], null=False))
        ))
        db.create_unique('suave_calendar_event_categories', ['event_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('suave_calendar_category')

        # Deleting field 'Event.category'
        db.delete_column('suave_calendar_event', 'category_id')

        # Removing M2M table for field categories on 'Event'
        db.delete_table('suave_calendar_event_categories')


    models = {
        'suave_calendar.category': {
            'Meta': {'object_name': 'Category'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'body': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave_calendar.event': {
            'Meta': {'object_name': 'Event'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'body': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_events'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['suave_calendar.Category']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_events'", 'null': 'True', 'to': "orm['suave_calendar.Category']"}),
            'dark_bg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'header_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'suave_calendar.eventimage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EventImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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