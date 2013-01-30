from django.db import models

# Create your models here.

class Article(models.Model):
    slug = models.SlugField(max_length=256)
    def __unicode__(self):
        return self.slug

class ArticleContent(models.Model):
    article = models.ForeignKey('Article')
    content = models.TextField() 
    title = models.CharField(max_length=1024)
    lang = models.CharField(max_length=2)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    def get_full_title(self):
        return self.article.slug+': '+self.title

    def get_url(self):
        return '/'+self.get_full_title().replace(' ','_')

    def get_edit_url(self):
        return self.get_url() + '/edit/'
    
    def __unicode__(self):
        return self.title
