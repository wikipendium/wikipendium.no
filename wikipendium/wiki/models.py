from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import urllib2, urllib
import simplejson as json

# Create your models here.

class Article(models.Model):
    slug = models.SlugField(max_length=256, unique=True)
    def __unicode__(self):
        return self.slug

    def save(self):
        self.slug = self.slug.upper()
        super(Article,self).save()

    def clean(self):
        if '/' in self.slug:
            raise ValidationError('Course code cannot contain slashes')
    
    def get_newest_content(self, lang='en'):
        return ArticleContent.objects.filter(article=self, lang=lang).order_by('-updated')[:1].get()

    def get_sorted_contents(self, lang='en'):
        return ArticleContent.objects.filter(article=self, lang=lang).order_by('-updated')


class ArticleContent(models.Model):
    article = models.ForeignKey('Article')
    content = models.TextField() 
    title = models.CharField(max_length=1024)
    lang = models.CharField(max_length=2, default='en')
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    edited_by = models.ForeignKey(User, blank=True, null=True)

    def clean(self):
        if '/' in self.title:
            raise ValidationError('Title cannot contain slashes')
    
    def get_full_title(self):
        return self.article.slug+': '+self.title

    def get_url(self):
        return '/'+self.article.slug + ":" + self.title.replace(' ','_')

    def get_edit_url(self):
        return self.get_url() + "/" + self.lang + '/edit/'
    
    def get_history_url(self):
        return self.get_url() + "/" + self.lang + '/history/'

    def get_history_single_url(self):
        return self.get_url() + '/history/'+str(self.pk)+'/'

    def get_language(self):
        data = {
            'q': self.content.encode('utf-8'),
            'key': '21f18e409617475159ef7d5a7084d40c'
            }
        language_json = urllib2.urlopen('http://ws.detectlanguage.com/0.2/detect', urllib.urlencode(data))
        language_info = json.loads(language_json.read())
        print language_info
        language_code = language_info["data"]["detections"][0]["language"]
        return language_code

    def save(self, lang=None):
        if not self.pk and not lang:
            self.lang = self.get_language()
        super(ArticleContent,self).save()

    def __unicode__(self):
        return self.title
