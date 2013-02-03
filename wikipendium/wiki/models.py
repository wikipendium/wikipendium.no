from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    slug = models.SlugField(max_length=256, unique=True)
    def __unicode__(self):
        return self.slug

    def save(self):
        self.slug = self.slug.upper()
        super(Article,self).save()

class ArticleContent(models.Model):
    article = models.ForeignKey('Article')
    content = models.TextField() 
    title = models.CharField(max_length=1024)
    lang = models.CharField(max_length=2)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    edited_by = models.ForeignKey(User, blank=True, null=True)
    
    def get_full_title(self):
        return self.article.slug+': '+self.title

    def get_url(self):
        return '/'+self.article.slug + ":" + self.title.replace(' ','_')

    def get_edit_url(self):
        return self.get_url() + '/edit/'
    
    def get_history_url(self):
        return self.get_url() + '/history/'

    def __unicode__(self):
        return self.title
