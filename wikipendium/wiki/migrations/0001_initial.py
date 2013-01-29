# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table('wiki_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
        ))
        db.send_create_signal('wiki', ['Article'])

        # Adding model 'ArticleContent'
        db.create_table('wiki_articlecontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('wiki', ['ArticleContent'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table('wiki_article')

        # Deleting model 'ArticleContent'
        db.delete_table('wiki_articlecontent')


    models = {
        'wiki.article': {
            'Meta': {'object_name': 'Article'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'})
        },
        'wiki.articlecontent': {
            'Meta': {'object_name': 'ArticleContent'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wiki']