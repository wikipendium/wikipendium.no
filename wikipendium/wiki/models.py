from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
        return ArticleContent.objects.filter(article=self).order_by('-updated')[:1].get()

    def get_sorted_contents(self):
        return ArticleContent.objects.filter(article=self).order_by('-updated')


class ArticleContent(models.Model):
    article = models.ForeignKey('Article')
    content = models.TextField() 
    title = models.CharField(max_length=1024)
    lang = models.CharField(max_length=2)
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
        return self.get_url() + '/edit/'
    
    def get_history_url(self):
        return self.get_url() + '/history/'

    def __unicode__(self):
        return self.title
