from django.forms import ModelForm, ValidationError
import django.forms as forms
from wikipendium.wiki.models import Article, ArticleContent
from wikipendium.wiki.merge3 import MergeError, merge


class ArticleForm(ModelForm):
    slug = forms.CharField(label='')
    title = forms.CharField(label='')
    content = forms.CharField(label='', widget=forms.Textarea())
    pk = forms.IntegerField(label='', widget=forms.HiddenInput())

    class Meta:
        model = ArticleContent
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        self.lang = kwargs.pop('lang', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['placeholder'] = 'Course code'
        self.fields['pk'].widget.attrs['value'] = 0

        try:
            if self.instance.article:
                slug = self.instance.article.slug
                self.fields['slug'].widget.attrs['value'] = slug
                if self.instance.article.pk:
                    self.fields['slug'].widget.attrs['readonly'] = True
                if self.instance.pk:
                    self.fields['pk'].widget.attrs['value'] = self.instance.pk
        except:
            pass

        self.fields['title'].widget.attrs['placeholder'] = 'Course title'
        self.fields.keyOrder = ['pk', 'slug', 'title', 'content']

    def clean(self):
        super(ArticleForm, self)
        self.merge_contents_if_needed()
        return self.cleaned_data

    def merge_contents_if_needed(self):
        parentId = self.cleaned_data['pk']
        article = None
        articleContent = None
        slug = self.cleaned_data['slug']
        lang = self.lang
        try:
            article = Article.objects.get(slug=slug)
        except:
            article = Article(slug=slug)
        try:
            articleContent = article.get_newest_content(lang)
        except:
            articleContent = ArticleContent(article=article, lang=lang)

        if parentId and parentId != articleContent.pk:
            parent = ArticleContent.objects.get(id=parentId)
            a = parent
            b = articleContent
            ancestors = set()
            commonAncestor = None
            while True:
                if a.pk in ancestors:
                    commonAncestor = a
                    break
                if b.pk in ancestors:
                    commonAncestor = b
                    break
                ancestors.add(a.pk)
                ancestors.add(b.pk)
                a = a.parent
                b = b.parent
                if a.parent is None and b.parent is None:
                    break

            try:
                merged = merge(self.cleaned_data['content'],
                               commonAncestor.content, articleContent.content)
                self.cleaned_data['content'] = merged
            except MergeError as e:
                raise ValidationError("Merge conflict", params=e.diff)

        return True
