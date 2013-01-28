from django.db import models

# Create your models here.

class Article(models.Model):
    slug = models.SlugField(max_length=256)

class ArticleContent(models.Model):
    article = models.ForeignKey('Article')
    content = models.TextField() 
    title = models.CharField(max_length=1024)
    lang = models.CharField(max_length=2)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)
